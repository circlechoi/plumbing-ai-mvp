import { NextResponse } from "next/server";
import { prisma } from "@/app/lib/prisma";
import type { ConfidenceLevel } from "@/app/lib/types";

const CONFIDENCE_MAP: Record<ConfidenceLevel, "HIGH" | "MEDIUM" | "LOW"> = {
  high: "HIGH",
  medium: "MEDIUM",
  low: "LOW",
};

export async function GET() {
  const orders = await prisma.order.findMany({
    orderBy: { createdAt: "desc" },
    include: { recognizedPart: true, recognitionLogs: true },
  });
  return NextResponse.json({ orders });
}

export async function POST(req: Request) {
  const body = await req.json();
  const {
    customerContact,
    deliveryAddress,
    quantity,
    recognizedPartId,
    confidence,
    recognitionLogId,
  } = body as {
    customerContact?: string;
    deliveryAddress?: string;
    quantity?: number;
    recognizedPartId?: string | null;
    confidence?: ConfidenceLevel | null;
    recognitionLogId?: string | null;
  };

  if (!customerContact?.trim() || !deliveryAddress?.trim() || !quantity || quantity < 1) {
    return NextResponse.json(
      { error: "연락처, 배송지, 수량(1 이상)을 모두 입력해주세요." },
      { status: 400 }
    );
  }

  const confidenceLevel = confidence ? CONFIDENCE_MAP[confidence] : null;
  const needsManualCheck = !recognizedPartId || confidenceLevel !== "HIGH";

  // AI가 최초로 추천한 1순위 부품 id를 스냅샷으로 저장 (이후 관리자가 recognizedPartId를 바꿔도 보존됨 — 정확도 분석용)
  let aiTopPickId: string | null = null;
  let matchedIdsCount = 0;
  if (recognitionLogId) {
    const log = await prisma.recognitionLog.findUnique({ where: { id: recognitionLogId } });
    if (log) {
      const parsed = JSON.parse(log.aiResponseJson) as { matched_db_ids?: string[] };
      matchedIdsCount = parsed.matched_db_ids?.length ?? 0;
      aiTopPickId = parsed.matched_db_ids?.[0] ?? null;
    }
  }

  // 신뢰도 기반 자동화: 신뢰도가 높고(HIGH) 후보가 단 하나뿐이며(모호함 없음) 그 후보 그대로
  // 주문된 경우에만 관리자 개입 없이 RECEIVED -> CHECKING까지 자동 진행한다.
  const settings = await prisma.settings.upsert({ where: { id: 1 }, update: {}, create: { id: 1 } });
  const isUnambiguousHighConfidence =
    confidenceLevel === "HIGH" && matchedIdsCount === 1 && recognizedPartId === aiTopPickId;
  const autoProcessed = settings.autoApproveEnabled && isUnambiguousHighConfidence;

  const order = await prisma.order.create({
    data: {
      customerContact: customerContact.trim(),
      deliveryAddress: deliveryAddress.trim(),
      quantity,
      recognizedPartId: recognizedPartId ?? null,
      aiTopPickId,
      confidenceLevel,
      needsManualCheck,
      autoProcessed,
      status: autoProcessed ? "CHECKING" : "RECEIVED",
    },
    include: { recognizedPart: true },
  });

  if (recognitionLogId) {
    await prisma.recognitionLog.update({
      where: { id: recognitionLogId },
      data: { orderId: order.id },
    });
  }

  return NextResponse.json({ order }, { status: 201 });
}
