"use client";

import { useEffect, useState } from "react";

type Part = {
  id: string;
  name: string;
  size: string;
  material: string;
  compatibleWith: { id: string; name: string; size: string }[];
};

export default function AdminPartsPage() {
  const [parts, setParts] = useState<Part[]>([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState("");
  const [size, setSize] = useState("");
  const [material, setMaterial] = useState("");
  const [compatibleWithIds, setCompatibleWithIds] = useState<string[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function loadParts() {
    const res = await fetch("/api/parts");
    const json = await res.json();
    setParts(json.parts);
    setLoading(false);
  }

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- 최초 마운트 시 데이터 fetch (표준 패턴)
    loadParts();
  }, []);

  function toggleCompatible(id: string) {
    setCompatibleWithIds((prev) => (prev.includes(id) ? prev.filter((v) => v !== id) : [...prev, id]));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const res = await fetch("/api/parts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, size, material, compatibleWithIds }),
      });
      const json = await res.json();
      if (!res.ok) {
        setError(json.error ?? "부품 추가 중 오류가 발생했습니다.");
        return;
      }
      setName("");
      setSize("");
      setMaterial("");
      setCompatibleWithIds([]);
      await loadParts();
    } catch {
      setError("서버에 연결할 수 없습니다.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h1 className="text-2xl font-bold">부품 DB 관리</h1>
        <p className="mt-1 text-gray-600">등록된 부품 목록을 확인하고, 새 부품과 호환 정보를 추가합니다.</p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4 rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <h2 className="font-semibold text-gray-800">새 부품 추가</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-gray-600">부품명</span>
            <input
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="예: PVC 소켓 이음관"
              className="rounded-md border border-gray-300 px-3 py-2"
            />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-gray-600">규격</span>
            <input
              required
              value={size}
              onChange={(e) => setSize(e.target.value)}
              placeholder="예: 20mm 또는 15A"
              className="rounded-md border border-gray-300 px-3 py-2"
            />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-gray-600">재질</span>
            <input
              required
              value={material}
              onChange={(e) => setMaterial(e.target.value)}
              placeholder="예: PVC, 황동, STS304"
              className="rounded-md border border-gray-300 px-3 py-2"
            />
          </label>
        </div>

        {parts.length > 0 && (
          <div className="flex flex-col gap-2">
            <span className="text-sm text-gray-600">호환 가능한 기존 부품 선택 (선택 사항)</span>
            <div className="flex max-h-40 flex-col gap-1 overflow-y-auto rounded-md border border-gray-200 p-3">
              {parts.map((p) => (
                <label key={p.id} className="flex items-center gap-2 text-sm">
                  <input
                    type="checkbox"
                    checked={compatibleWithIds.includes(p.id)}
                    onChange={() => toggleCompatible(p.id)}
                  />
                  {p.name} — {p.size} / {p.material}
                </label>
              ))}
            </div>
          </div>
        )}

        {error && <div className="rounded-md border border-red-300 bg-red-50 p-3 text-red-800">{error}</div>}

        <button
          type="submit"
          disabled={submitting}
          className="w-fit rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400"
        >
          {submitting ? "추가 중..." : "부품 추가"}
        </button>
      </form>

      <div>
        <h2 className="mb-3 font-semibold text-gray-800">등록된 부품 ({parts.length}개)</h2>
        {loading ? (
          <p className="text-gray-500">불러오는 중...</p>
        ) : (
          <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white">
            <table className="w-full text-left text-sm">
              <thead className="bg-gray-50 text-gray-600">
                <tr>
                  <th className="px-4 py-3">부품명</th>
                  <th className="px-4 py-3">규격</th>
                  <th className="px-4 py-3">재질</th>
                  <th className="px-4 py-3">호환 부품</th>
                </tr>
              </thead>
              <tbody>
                {parts.map((p) => (
                  <tr key={p.id} className="border-t border-gray-100">
                    <td className="px-4 py-3 font-medium">{p.name}</td>
                    <td className="px-4 py-3">{p.size}</td>
                    <td className="px-4 py-3">{p.material}</td>
                    <td className="px-4 py-3 text-gray-500">
                      {p.compatibleWith.length > 0
                        ? p.compatibleWith.map((c) => `${c.name} (${c.size})`).join(", ")
                        : "-"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
