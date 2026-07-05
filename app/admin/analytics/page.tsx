"use client";

import { useEffect, useState } from "react";

type Outcome = "correct" | "corrected" | "noMatch";

type Analytics = {
  totalOrders: number;
  byOutcome: Record<Outcome, number>;
  byConfidence: Record<"HIGH" | "MEDIUM" | "LOW", Record<Outcome, number>>;
  topCorrectedParts: { name: string; size: string; count: number }[];
  automation: {
    autoProcessedCount: number;
    autoProcessedCorrectedCount: number;
    autoProcessedRate: number;
  };
  costs: {
    totalRecognitions: number;
    totalInputTokens: number;
    totalOutputTokens: number;
    totalCostUsd: number;
    avgCostUsd: number | null;
    model: string | null;
  };
};

const OUTCOME_LABEL: Record<Outcome, string> = { correct: "정확", corrected: "수정됨", noMatch: "매칭없음" };
const CONFIDENCE_LABEL: Record<string, string> = { HIGH: "높음", MEDIUM: "중간", LOW: "낮음" };

function pct(n: number, total: number) {
  if (total === 0) return "0%";
  return `${Math.round((n / total) * 100)}%`;
}

export default function AnalyticsPage() {
  const [data, setData] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [autoApproveEnabled, setAutoApproveEnabled] = useState(false);
  const [savingSettings, setSavingSettings] = useState(false);

  useEffect(() => {
    fetch("/api/analytics")
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        setLoading(false);
      });
    fetch("/api/settings")
      .then((res) => res.json())
      .then((json) => setAutoApproveEnabled(json.settings.autoApproveEnabled));
  }, []);

  async function toggleAutoApprove() {
    setSavingSettings(true);
    const next = !autoApproveEnabled;
    const res = await fetch("/api/settings", {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ autoApproveEnabled: next }),
    });
    const json = await res.json();
    setAutoApproveEnabled(json.settings.autoApproveEnabled);
    setSavingSettings(false);
  }

  if (loading || !data) {
    return <p className="text-gray-500">불러오는 중...</p>;
  }

  const attempted = data.totalOrders; // 매칭 시도(=recognizedPart 존재 여부와 무관하게 전체 주문)
  const matchedTotal = data.byOutcome.correct + data.byOutcome.corrected;
  const accuracyAmongMatched = matchedTotal > 0 ? pct(data.byOutcome.correct, matchedTotal) : "-";

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h1 className="text-2xl font-bold">AI 정확도 &amp; 비용 분석</h1>
        <p className="mt-1 text-gray-600">
          AI의 최초 추천과 관리자가 최종 확정한 부품을 비교해 정확도를 측정합니다.
        </p>
      </div>

      <div className="flex items-center justify-between rounded-lg border border-gray-200 bg-white p-5">
        <div>
          <h2 className="font-semibold text-gray-800">신뢰도 기반 자동화</h2>
          <p className="mt-1 text-sm text-gray-600">
            켜두면 AI 신뢰도가 &quot;높음&quot;이고 호환 후보가 단 하나뿐인(모호함 없는) 신규 주문은
            관리자 확인 없이 접수 → 확인중 상태로 자동 진행됩니다.
          </p>
        </div>
        <button
          type="button"
          onClick={toggleAutoApprove}
          disabled={savingSettings}
          className={`whitespace-nowrap rounded-full px-5 py-2 font-semibold text-white transition-colors disabled:cursor-not-allowed disabled:opacity-60 ${
            autoApproveEnabled ? "bg-green-600 hover:bg-green-700" : "bg-gray-400 hover:bg-gray-500"
          }`}
        >
          {autoApproveEnabled ? "자동화 켜짐" : "자동화 꺼짐"}
        </button>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="rounded-lg border border-gray-200 bg-white p-5">
          <p className="text-sm text-gray-500">전체 주문</p>
          <p className="mt-1 text-3xl font-bold">{attempted}건</p>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-5">
          <p className="text-sm text-gray-500">매칭 시도 중 정확도</p>
          <p className="mt-1 text-3xl font-bold text-green-700">{accuracyAmongMatched}</p>
          <p className="mt-1 text-xs text-gray-400">
            매칭 없음(추천 자체가 없던 건)은 제외 — 정확 {data.byOutcome.correct}건 / 수정됨{" "}
            {data.byOutcome.corrected}건
          </p>
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-5">
          <p className="text-sm text-gray-500">인식 1건당 평균 비용</p>
          <p className="mt-1 text-3xl font-bold">
            {data.costs.avgCostUsd != null ? `$${data.costs.avgCostUsd.toFixed(4)}` : "-"}
          </p>
          <p className="mt-1 text-xs text-gray-400">모델: {data.costs.model ?? "-"}</p>
        </div>
      </div>

      <div className="rounded-lg border border-gray-200 bg-white p-5">
        <h2 className="mb-3 font-semibold text-gray-800">결과 분포</h2>
        <div className="flex gap-6">
          {(Object.keys(OUTCOME_LABEL) as Outcome[]).map((key) => (
            <div key={key} className="flex-1 rounded-md border border-gray-100 p-4 text-center">
              <p className="text-sm text-gray-500">{OUTCOME_LABEL[key]}</p>
              <p className="mt-1 text-2xl font-bold">{data.byOutcome[key]}건</p>
              <p className="text-sm text-gray-400">{pct(data.byOutcome[key], attempted)}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-lg border border-gray-200 bg-white p-5">
        <h2 className="mb-3 font-semibold text-gray-800">자동화 효과</h2>
        <div className="flex gap-6">
          <div className="flex-1 rounded-md border border-gray-100 p-4 text-center">
            <p className="text-sm text-gray-500">자동 처리된 주문</p>
            <p className="mt-1 text-2xl font-bold text-blue-700">{data.automation.autoProcessedCount}건</p>
            <p className="text-sm text-gray-400">
              전체 주문의 {pct(data.automation.autoProcessedCount, attempted)} — 관리자 개입 없이 확인중
              단계까지 자동 진행됨
            </p>
          </div>
          <div className="flex-1 rounded-md border border-gray-100 p-4 text-center">
            <p className="text-sm text-gray-500">자동 처리 후 다시 수정된 건</p>
            <p
              className={`mt-1 text-2xl font-bold ${
                data.automation.autoProcessedCorrectedCount > 0 ? "text-red-600" : "text-gray-700"
              }`}
            >
              {data.automation.autoProcessedCorrectedCount}건
            </p>
            <p className="text-sm text-gray-400">
              0건이 아니라면 자동화 조건을 더 보수적으로 조정할 필요가 있습니다
            </p>
          </div>
        </div>
      </div>

      <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white p-5">
        <h2 className="mb-3 font-semibold text-gray-800">신뢰도별 정확도</h2>
        <table className="w-full text-left text-sm">
          <thead className="text-gray-500">
            <tr>
              <th className="py-2">신뢰도</th>
              <th className="py-2">정확</th>
              <th className="py-2">수정됨</th>
              <th className="py-2">매칭없음</th>
            </tr>
          </thead>
          <tbody>
            {(Object.keys(CONFIDENCE_LABEL) as ("HIGH" | "MEDIUM" | "LOW")[]).map((level) => (
              <tr key={level} className="border-t border-gray-100">
                <td className="py-2 font-medium">{CONFIDENCE_LABEL[level]}</td>
                <td className="py-2">{data.byConfidence[level].correct}</td>
                <td className="py-2">{data.byConfidence[level].corrected}</td>
                <td className="py-2">{data.byConfidence[level].noMatch}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="rounded-lg border border-gray-200 bg-white p-5">
        <h2 className="mb-3 font-semibold text-gray-800">자주 재지정된 부품 (AI가 자주 틀리는 유형)</h2>
        {data.topCorrectedParts.length === 0 ? (
          <p className="text-gray-500">아직 데이터가 없습니다.</p>
        ) : (
          <ol className="flex flex-col gap-2">
            {data.topCorrectedParts.map((p, i) => (
              <li key={i} className="flex justify-between text-sm">
                <span>
                  {i + 1}. {p.name} ({p.size})
                </span>
                <span className="font-medium">{p.count}건</span>
              </li>
            ))}
          </ol>
        )}
      </div>

      <div className="rounded-lg border border-gray-200 bg-white p-5">
        <h2 className="mb-3 font-semibold text-gray-800">비용 상세</h2>
        <dl className="grid grid-cols-2 gap-3 text-sm sm:grid-cols-4">
          <div>
            <dt className="text-gray-500">총 인식 건수</dt>
            <dd className="font-medium">{data.costs.totalRecognitions}건</dd>
          </div>
          <div>
            <dt className="text-gray-500">총 입력 토큰</dt>
            <dd className="font-medium">{data.costs.totalInputTokens.toLocaleString()}</dd>
          </div>
          <div>
            <dt className="text-gray-500">총 출력 토큰</dt>
            <dd className="font-medium">{data.costs.totalOutputTokens.toLocaleString()}</dd>
          </div>
          <div>
            <dt className="text-gray-500">총 예상 비용</dt>
            <dd className="font-medium">${data.costs.totalCostUsd.toFixed(4)}</dd>
          </div>
        </dl>
        <p className="mt-3 text-xs text-gray-400">
          * 공개 정가 기준 추정치이며, 실제 청구 금액과 다를 수 있습니다.
        </p>
      </div>
    </div>
  );
}
