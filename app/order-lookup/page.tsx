"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export default function OrderLookupPage() {
  const router = useRouter();
  const [orderId, setOrderId] = useState("");
  const [phone, setPhone] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const res = await fetch("/api/orders/lookup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ orderId, phone }),
      });
      const json = await res.json();
      if (!res.ok) {
        setError(json.error ?? "조회에 실패했습니다.");
        return;
      }
      router.push(`/order/${json.orderId}`);
    } catch {
      setError("서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto flex max-w-lg flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold">주문 조회</h1>
        <p className="mt-1 text-gray-600">
          접수하신 연락처와 주문번호를 입력하면 현재 주문 상태를 확인할 수 있습니다. 주문번호는 접수
          완료 화면에서 확인 및 복사하실 수 있습니다.
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-5 rounded-lg border border-gray-200 bg-white p-6 shadow-sm"
      >
        <label className="flex flex-col gap-1">
          <span className="font-medium text-gray-800">연락처</span>
          <input
            type="tel"
            required
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="010-0000-0000"
            className="rounded-md border border-gray-300 px-4 py-3 text-lg focus:border-blue-500 focus:outline-none"
          />
        </label>

        <label className="flex flex-col gap-1">
          <span className="font-medium text-gray-800">주문번호</span>
          <input
            type="text"
            required
            value={orderId}
            onChange={(e) => setOrderId(e.target.value)}
            placeholder="주문 접수 완료 화면에서 복사한 주문번호"
            className="rounded-md border border-gray-300 px-4 py-3 font-mono text-sm focus:border-blue-500 focus:outline-none"
          />
        </label>

        {error && <div className="rounded-md border border-red-300 bg-red-50 p-3 text-red-800">{error}</div>}

        <button
          type="submit"
          disabled={submitting}
          className="w-full rounded-lg bg-blue-600 px-6 py-4 text-lg font-semibold text-white transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400"
        >
          {submitting ? "조회 중..." : "주문 조회하기"}
        </button>
      </form>
    </div>
  );
}
