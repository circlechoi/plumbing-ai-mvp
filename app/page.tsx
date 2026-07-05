"use client";

import { useRouter } from "next/navigation";
import { useRef, useState } from "react";
import OrderStepper from "@/app/components/OrderStepper";
import type { ConfidenceLevel, RecognitionResult } from "@/app/lib/types";

type Part = {
  id: string;
  name: string;
  size: string;
  material: string;
};

type RecognizeResponse = {
  recognitionLogId: string;
  imageUrl: string;
  result: RecognitionResult;
  matchedParts: Part[];
  fallbackUsed: boolean;
};

const CONFIDENCE_BADGE: Record<ConfidenceLevel, { label: string; className: string; desc: string }> = {
  high: {
    label: "신뢰도 높음",
    className: "bg-green-100 text-green-800 border-green-300",
    desc: "AI가 부품 종류·규격·재질을 사진만으로 명확하게 판단했습니다.",
  },
  medium: {
    label: "신뢰도 중간 — 확인 필요",
    className: "bg-yellow-100 text-yellow-800 border-yellow-300",
    desc: "부품 종류는 확실하지만 규격이나 재질 일부는 추정입니다. 담당자가 한 번 더 확인합니다.",
  },
  low: {
    label: "신뢰도 낮음 — 수동 확인 필요",
    className: "bg-red-100 text-red-800 border-red-300",
    desc: "사진만으로 확신하기 어려운 경우입니다. 담당자가 직접 확인 후 연락드립니다.",
  },
};

const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"];
const MAX_SIZE_BYTES = 10 * 1024 * 1024;

export default function HomePage() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fileError, setFileError] = useState<string | null>(null);
  const [data, setData] = useState<RecognizeResponse | null>(null);

  function selectFile(f: File) {
    if (!ALLOWED_TYPES.includes(f.type)) {
      setFileError("jpg, png, gif, webp 형식의 이미지만 업로드할 수 있습니다.");
      return;
    }
    if (f.size > MAX_SIZE_BYTES) {
      setFileError("이미지 파일은 10MB를 넘을 수 없습니다.");
      return;
    }
    setFileError(null);
    setFile(f);
    setPreviewUrl(URL.createObjectURL(f));
    setData(null);
    setError(null);
  }

  function clearFile() {
    setFile(null);
    setPreviewUrl(null);
    setData(null);
    setError(null);
    setFileError(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  function handleDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setIsDragging(false);
    const f = e.dataTransfer.files?.[0];
    if (f) selectFile(f);
  }

  async function handleRecognize() {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("image", file);
      const res = await fetch("/api/recognize", { method: "POST", body: formData });
      const json = await res.json();
      if (!res.ok) {
        setError(json.error ?? "인식 중 오류가 발생했습니다.");
        return;
      }
      setData(json);
    } catch {
      setError("서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.");
    } finally {
      setLoading(false);
    }
  }

  function goToOrder(partId: string | null) {
    if (!data) return;
    const params = new URLSearchParams();
    if (partId) params.set("partId", partId);
    params.set("confidence", data.result.confidence);
    params.set("recognitionLogId", data.recognitionLogId);
    router.push(`/order/new?${params.toString()}`);
  }

  const badge = data ? CONFIDENCE_BADGE[data.result.confidence] : null;

  return (
    <div className="flex flex-col gap-8">
      <OrderStepper current={data ? 2 : 1} />

      <div>
        <h1 className="text-2xl font-bold">부품 사진으로 규격 인식하기</h1>
        <p className="mt-1 text-gray-600">
          배관·설비 부속(밸브, 니플, 소켓, 앵커볼트 등) 사진을 올리면 AI가 부품명과 규격을 추정하고,
          호환 가능한 대체 부품을 추천해드립니다.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-3 rounded-lg border border-gray-200 bg-white p-4 text-sm sm:grid-cols-3">
        <div className="flex items-start gap-2">
          <span className="font-bold text-blue-600">1</span>
          <span className="text-gray-600">부품 사진을 찍어 업로드하세요</span>
        </div>
        <div className="flex items-start gap-2">
          <span className="font-bold text-blue-600">2</span>
          <span className="text-gray-600">AI가 규격을 추정하고 호환 부품을 추천해드려요</span>
        </div>
        <div className="flex items-start gap-2">
          <span className="font-bold text-blue-600">3</span>
          <span className="text-gray-600">마음에 드는 부품으로 바로 주문을 접수하세요</span>
        </div>
      </div>

      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => !previewUrl && fileInputRef.current?.click()}
        className={`flex flex-col items-center justify-center gap-3 rounded-lg border-2 border-dashed p-10 text-center transition-colors ${
          previewUrl ? "" : "cursor-pointer"
        } ${isDragging ? "border-blue-500 bg-blue-50" : "border-gray-300 bg-white hover:border-gray-400"}`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png,image/gif,image/webp"
          className="hidden"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) selectFile(f);
          }}
        />
        {previewUrl ? (
          <div className="flex flex-col items-center gap-3">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={previewUrl} alt="업로드한 부품 사진 미리보기" className="max-h-64 rounded-md object-contain" />
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="rounded-md border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                다른 사진으로 바꾸기
              </button>
              <button
                type="button"
                onClick={clearFile}
                className="rounded-md border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-500 hover:bg-gray-50"
              >
                ✕ 제거
              </button>
            </div>
          </div>
        ) : (
          <>
            <span className="text-4xl">📷</span>
            <p className="text-lg font-medium text-gray-700">부품 사진 업로드</p>
            <p className="text-sm text-gray-500">클릭하거나 파일을 이곳에 드래그하세요 (jpg, png, gif, webp / 최대 10MB)</p>
          </>
        )}
      </div>

      {fileError && (
        <div className="rounded-lg border border-red-300 bg-red-50 p-4 text-red-800">{fileError}</div>
      )}

      {file && (
        <button
          type="button"
          onClick={handleRecognize}
          disabled={loading}
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-6 py-4 text-lg font-semibold text-white transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400"
        >
          {loading && (
            <span
              className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent"
              aria-hidden="true"
            />
          )}
          {loading ? "AI가 분석 중입니다..." : "AI로 부품 인식하기"}
        </button>
      )}

      {error && (
        <div className="rounded-lg border border-red-300 bg-red-50 p-4 text-red-800">{error}</div>
      )}

      {data && badge && (
        <div className="flex flex-col gap-4 rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold">{data.result.part_name_guess}</h2>
              <p className="mt-1 text-gray-700">
                추정 규격: <span className="font-medium">{data.result.size_guess}</span> · 추정 재질:{" "}
                <span className="font-medium">{data.result.material_guess}</span>
              </p>
            </div>
            <span
              title={badge.desc}
              className={`whitespace-nowrap rounded-full border px-3 py-1 text-sm font-semibold ${badge.className}`}
            >
              {badge.label}
            </span>
          </div>

          <p className="text-sm text-gray-500">{badge.desc}</p>
          <p className="text-sm text-gray-500">AI 판단 근거: {data.result.reasoning}</p>

          {data.result.confidence === "low" && (
            <div className="rounded-md border border-red-200 bg-red-50 p-4 text-red-800">
              정확한 매칭이 어렵습니다. 담당자가 확인 후 연락드립니다. 아래에서 그대로 주문을 접수하실 수 있습니다.
            </div>
          )}

          {data.matchedParts.length > 0 ? (
            <div className="flex flex-col gap-3">
              <h3 className="font-semibold text-gray-800">호환 가능한 부품 후보</h3>
              {data.matchedParts.map((part) => (
                <div
                  key={part.id}
                  className="flex items-center justify-between gap-4 rounded-md border border-gray-200 p-4"
                >
                  <div>
                    <p className="font-medium">{part.name}</p>
                    <p className="text-sm text-gray-500">
                      {part.size} · {part.material}
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => goToOrder(part.id)}
                    className="whitespace-nowrap rounded-md bg-gray-900 px-4 py-2 font-medium text-white hover:bg-gray-700"
                  >
                    이 부품으로 주문하기
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="flex items-center justify-between gap-4 rounded-md border border-gray-200 p-4">
              <p className="text-gray-600">DB에서 일치하는 부품을 찾지 못했습니다. 담당자 확인 후 진행됩니다.</p>
              <button
                type="button"
                onClick={() => goToOrder(null)}
                className="whitespace-nowrap rounded-md bg-gray-900 px-4 py-2 font-medium text-white hover:bg-gray-700"
              >
                그대로 주문 접수하기
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
