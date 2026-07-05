// 100만 토큰(MTok)당 가격 (USD, 2026-07 기준 정가). 참고용 추정치이며 실제 청구 금액과 다를 수 있음.
export const MODEL_PRICING: Record<string, { inputPerMTok: number; outputPerMTok: number }> = {
  "claude-haiku-4-5": { inputPerMTok: 1.0, outputPerMTok: 5.0 },
  "claude-sonnet-5": { inputPerMTok: 3.0, outputPerMTok: 15.0 },
};

export function estimateCostUsd(model: string | null, inputTokens: number | null, outputTokens: number | null) {
  if (!model || inputTokens == null || outputTokens == null) return null;
  const pricing = MODEL_PRICING[model];
  if (!pricing) return null;
  return (inputTokens / 1_000_000) * pricing.inputPerMTok + (outputTokens / 1_000_000) * pricing.outputPerMTok;
}
