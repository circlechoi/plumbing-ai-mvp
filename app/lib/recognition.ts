import Anthropic from "@anthropic-ai/sdk";
import sharp from "sharp";
import { prisma } from "@/app/lib/prisma";
import type { ConfidenceLevel, RecognitionResult } from "@/app/lib/types";

// 단순 분류/매칭 작업이므로 Haiku로 충분 (Sonnet 대비 비용 절감)
const MODEL = "claude-haiku-4-5";
// Claude에게 보내기 전 이미지 리사이즈 상한 (긴 변 기준, px) — 이미지 토큰 비용 절감
const MAX_IMAGE_DIMENSION = 1024;

const CONFIDENCE_LEVELS: ConfidenceLevel[] = ["high", "medium", "low"];

export interface RecognitionUsage {
  model: string;
  inputTokens: number | null;
  outputTokens: number | null;
}

function buildSystemPrompt(dbParts: { id: string; name: string; size: string; material: string }[]) {
  return `너는 대한민국 배관·설비 자재 전문가다. 업로드된 사진을 보고 부품 종류, 추정 규격(mm 또는 인치/A 호칭), 재질을 판단하라.

아래는 우리 데이터베이스에 등록된 부품 목록이다. 사진 속 부품과 동일하거나 호환 가능한 대체품이 목록 안에 있다면 그 id를 matched_db_ids 배열에 담아라. 목록에 없는 id는 절대로 만들어내지 마라. 일치하거나 호환되는 항목이 없다면 빈 배열로 두어라.

데이터베이스 목록:
${JSON.stringify(dbParts)}

반드시 아래 스키마 형식의 JSON 객체 하나만 출력하라. 다른 설명, 인사말, 마크다운, 코드블록 없이 순수 JSON만 출력하라:
{
  "part_name_guess": "string",
  "size_guess": "string",
  "material_guess": "string",
  "confidence": "high | medium | low",
  "reasoning": "string (짧은 판단 근거, 1~2문장)",
  "matched_db_ids": ["string"]
}

confidence 판단 기준:
- high: 부품 종류, 규격, 재질을 사진만으로 명확히 판단 가능
- medium: 부품 종류는 확실하지만 규격이나 재질 중 일부는 추정에 가까움
- low: 사진이 흐릿하거나 각도가 애매하거나 생소한 부품이라 확신할 수 없음

절대로 확신 없는 답을 지어내지 마라. 조금이라도 애매하면 반드시 confidence를 low로 낮추고, reasoning에 왜 확신할 수 없는지 적어라.`;
}

function fallbackResult(reasoning: string): RecognitionResult {
  return {
    part_name_guess: "인식 실패",
    size_guess: "알 수 없음",
    material_guess: "알 수 없음",
    confidence: "low",
    reasoning,
    matched_db_ids: [],
  };
}

function parseAndValidate(raw: string): RecognitionResult {
  const cleaned = raw.trim().replace(/^```(json)?/i, "").replace(/```$/, "").trim();
  const parsed = JSON.parse(cleaned);

  if (
    typeof parsed.part_name_guess !== "string" ||
    typeof parsed.size_guess !== "string" ||
    typeof parsed.material_guess !== "string" ||
    typeof parsed.reasoning !== "string" ||
    !CONFIDENCE_LEVELS.includes(parsed.confidence) ||
    !Array.isArray(parsed.matched_db_ids)
  ) {
    throw new Error("AI 응답이 예상된 스키마와 일치하지 않습니다.");
  }

  return {
    part_name_guess: parsed.part_name_guess,
    size_guess: parsed.size_guess,
    material_guess: parsed.material_guess,
    confidence: parsed.confidence,
    reasoning: parsed.reasoning,
    matched_db_ids: parsed.matched_db_ids.filter((id: unknown) => typeof id === "string"),
  };
}

export async function recognizePart(params: {
  imageBuffer: Buffer;
}): Promise<{ result: RecognitionResult; fallbackUsed: boolean; usage: RecognitionUsage }> {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    throw new Error("ANTHROPIC_API_KEY 환경변수가 설정되어 있지 않습니다. .env 파일을 확인하세요.");
  }

  const dbParts = await prisma.part.findMany({
    select: { id: true, name: true, size: true, material: true },
  });

  const anthropic = new Anthropic({ apiKey });

  const resizedBuffer = await sharp(params.imageBuffer)
    .resize({ width: MAX_IMAGE_DIMENSION, height: MAX_IMAGE_DIMENSION, fit: "inside", withoutEnlargement: true })
    .jpeg({ quality: 82 })
    .toBuffer();
  const base64Data = resizedBuffer.toString("base64");

  let usage: RecognitionUsage = { model: MODEL, inputTokens: null, outputTokens: null };

  try {
    const message = await anthropic.messages.create({
      model: MODEL,
      max_tokens: 1024,
      system: buildSystemPrompt(dbParts),
      messages: [
        {
          role: "user",
          content: [
            {
              type: "image",
              source: { type: "base64", media_type: "image/jpeg", data: base64Data },
            },
            {
              type: "text",
              text: "이 사진 속 배관/설비 부품을 분석해서 지정된 JSON 스키마로만 응답해줘.",
            },
          ],
        },
      ],
    });

    usage = {
      model: MODEL,
      inputTokens: message.usage.input_tokens,
      outputTokens: message.usage.output_tokens,
    };

    const textBlock = message.content.find((block) => block.type === "text");
    if (!textBlock || textBlock.type !== "text") {
      return {
        result: fallbackResult("AI가 텍스트 응답을 반환하지 않았습니다. 담당자가 사진을 직접 확인합니다."),
        fallbackUsed: true,
        usage,
      };
    }

    const result = parseAndValidate(textBlock.text);
    // matched_db_ids 중 실제 DB에 없는 id는 걸러낸다 (환각 방지 2차 검증)
    const validIds = new Set(dbParts.map((p) => p.id));
    result.matched_db_ids = result.matched_db_ids.filter((id) => validIds.has(id));

    return { result, fallbackUsed: false, usage };
  } catch (error) {
    const message = error instanceof Error ? error.message : "알 수 없는 오류";
    return {
      result: fallbackResult(`AI 인식 중 오류가 발생했습니다 (${message}). 담당자가 사진을 직접 확인 후 연락드립니다.`),
      fallbackUsed: true,
      usage,
    };
  }
}
