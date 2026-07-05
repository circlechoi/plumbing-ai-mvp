import { NextResponse } from "next/server";
import { prisma } from "@/app/lib/prisma";
import { estimateCostUsd } from "@/app/lib/pricing";

type Outcome = "correct" | "corrected" | "noMatch";

function classify(order: { aiTopPickId: string | null; recognizedPartId: string | null }): Outcome {
  if (!order.aiTopPickId) return "noMatch";
  if (order.recognizedPartId === order.aiTopPickId) return "correct";
  return "corrected";
}

export async function GET() {
  const orders = await prisma.order.findMany({
    select: {
      aiTopPickId: true,
      recognizedPartId: true,
      confidenceLevel: true,
      autoProcessed: true,
      recognizedPart: { select: { id: true, name: true, size: true } },
    },
  });

  const byOutcome = { correct: 0, corrected: 0, noMatch: 0 };
  const byConfidence: Record<string, { correct: number; corrected: number; noMatch: number }> = {
    HIGH: { correct: 0, corrected: 0, noMatch: 0 },
    MEDIUM: { correct: 0, corrected: 0, noMatch: 0 },
    LOW: { correct: 0, corrected: 0, noMatch: 0 },
  };
  const correctedPartCounts = new Map<string, { name: string; size: string; count: number }>();
  let autoProcessedCount = 0;
  let autoProcessedCorrectedCount = 0;

  for (const order of orders) {
    const outcome = classify(order);
    byOutcome[outcome] += 1;

    if (order.confidenceLevel) {
      byConfidence[order.confidenceLevel][outcome] += 1;
    }

    if (order.autoProcessed) {
      autoProcessedCount += 1;
      // 자동 처리된 이후에도 관리자가 부품을 다시 바꿨다면 자동화가 틀렸다는 신호
      if (outcome === "corrected") autoProcessedCorrectedCount += 1;
    }

    if (outcome === "corrected" && order.recognizedPart) {
      const key = order.recognizedPart.id;
      const existing = correctedPartCounts.get(key);
      if (existing) {
        existing.count += 1;
      } else {
        correctedPartCounts.set(key, {
          name: order.recognizedPart.name,
          size: order.recognizedPart.size,
          count: 1,
        });
      }
    }
  }

  const topCorrectedParts = Array.from(correctedPartCounts.values())
    .sort((a, b) => b.count - a.count)
    .slice(0, 5);

  const logs = await prisma.recognitionLog.findMany({
    select: { model: true, inputTokens: true, outputTokens: true },
  });

  let totalInputTokens = 0;
  let totalOutputTokens = 0;
  let totalCostUsd = 0;
  let pricedRecognitions = 0;

  for (const log of logs) {
    if (log.inputTokens != null) totalInputTokens += log.inputTokens;
    if (log.outputTokens != null) totalOutputTokens += log.outputTokens;
    const cost = estimateCostUsd(log.model, log.inputTokens, log.outputTokens);
    if (cost != null) {
      totalCostUsd += cost;
      pricedRecognitions += 1;
    }
  }

  return NextResponse.json({
    totalOrders: orders.length,
    byOutcome,
    byConfidence,
    topCorrectedParts,
    automation: {
      autoProcessedCount,
      autoProcessedCorrectedCount,
      autoProcessedRate: orders.length ? autoProcessedCount / orders.length : 0,
    },
    costs: {
      totalRecognitions: logs.length,
      totalInputTokens,
      totalOutputTokens,
      totalCostUsd,
      avgCostUsd: pricedRecognitions ? totalCostUsd / pricedRecognitions : null,
      model: logs.find((l) => l.model)?.model ?? null,
    },
  });
}
