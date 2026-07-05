"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

type Part = {
  id: string;
  name: string;
  size: string;
  material: string;
};

type Order = {
  id: string;
  customerContact: string;
  deliveryAddress: string;
  quantity: number;
  status: "RECEIVED" | "CHECKING" | "COMPLETED";
  confidenceLevel: "HIGH" | "MEDIUM" | "LOW" | null;
  needsManualCheck: boolean;
  autoProcessed: boolean;
  createdAt: string;
  recognizedPart: Part | null;
  recognitionLogs: { id: string; rawImageUrl: string; aiResponseJson: string }[];
};

const STATUS_LABEL: Record<Order["status"], string> = {
  RECEIVED: "접수",
  CHECKING: "확인중",
  COMPLETED: "완료",
};

const CONFIDENCE_LABEL: Record<string, string> = { HIGH: "높음", MEDIUM: "중간", LOW: "낮음" };

export default function AdminPage() {
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [parts, setParts] = useState<Part[]>([]);
  const [loading, setLoading] = useState(true);
  const [updatingId, setUpdatingId] = useState<string | null>(null);

  async function loadData() {
    const [ordersRes, partsRes] = await Promise.all([fetch("/api/orders"), fetch("/api/parts")]);
    const ordersJson = await ordersRes.json();
    const partsJson = await partsRes.json();
    setOrders(ordersJson.orders);
    setParts(partsJson.parts);
    setLoading(false);
  }

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- 최초 마운트 시 데이터 fetch (표준 패턴)
    loadData();
  }, []);

  async function updateOrder(id: string, patch: Record<string, unknown>) {
    setUpdatingId(id);
    await fetch(`/api/orders/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(patch),
    });
    await loadData();
    setUpdatingId(null);
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">관리자 대시보드</h1>
          <p className="mt-1 text-gray-600">접수된 주문과 AI 인식 결과를 확인하고, 필요 시 부품을 재지정합니다.</p>
        </div>
        <div className="flex gap-2">
          <Link
            href="/admin/analytics"
            className="whitespace-nowrap rounded-md bg-gray-900 px-4 py-2 font-medium text-white hover:bg-gray-700"
          >
            정확도 분석
          </Link>
          <Link
            href="/admin/parts"
            className="whitespace-nowrap rounded-md bg-gray-900 px-4 py-2 font-medium text-white hover:bg-gray-700"
          >
            부품 DB 관리
          </Link>
          <button
            type="button"
            onClick={async () => {
              await fetch("/api/admin-logout", { method: "POST" });
              router.push("/admin/login");
              router.refresh();
            }}
            className="whitespace-nowrap rounded-md border border-gray-300 px-4 py-2 font-medium text-gray-700 hover:bg-gray-50"
          >
            로그아웃
          </button>
        </div>
      </div>

      {loading ? (
        <p className="text-gray-500">불러오는 중...</p>
      ) : orders.length === 0 ? (
        <p className="text-gray-500">접수된 주문이 없습니다.</p>
      ) : (
        <div className="flex flex-col gap-4">
          {orders.map((order) => (
            <div
              key={order.id}
              className={`flex flex-col gap-3 rounded-lg border p-5 shadow-sm ${
                order.needsManualCheck ? "border-yellow-300 bg-yellow-50" : "border-gray-200 bg-white"
              }`}
            >
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-gray-500">{order.id}</span>
                  {order.needsManualCheck && (
                    <span className="rounded-full bg-yellow-200 px-2 py-0.5 text-xs font-semibold text-yellow-900">
                      수동 확인 필요
                    </span>
                  )}
                  {order.autoProcessed && (
                    <span className="rounded-full bg-blue-200 px-2 py-0.5 text-xs font-semibold text-blue-900">
                      자동 처리됨
                    </span>
                  )}
                </div>
                <span className="text-xs text-gray-400">{new Date(order.createdAt).toLocaleString("ko-KR")}</span>
              </div>

              <div className="grid grid-cols-2 gap-x-6 gap-y-1 text-sm sm:grid-cols-4">
                <div>
                  <span className="text-gray-500">연락처</span>
                  <p className="font-medium">{order.customerContact}</p>
                </div>
                <div>
                  <span className="text-gray-500">배송지</span>
                  <p className="font-medium">{order.deliveryAddress}</p>
                </div>
                <div>
                  <span className="text-gray-500">수량</span>
                  <p className="font-medium">{order.quantity}개</p>
                </div>
                <div>
                  <span className="text-gray-500">AI 신뢰도</span>
                  <p className="font-medium">
                    {order.confidenceLevel ? CONFIDENCE_LABEL[order.confidenceLevel] : "-"}
                  </p>
                </div>
              </div>

              <div className="flex flex-wrap items-end gap-4 border-t border-gray-100 pt-3">
                <label className="flex flex-col gap-1 text-sm">
                  <span className="text-gray-500">인식/지정된 부품</span>
                  <select
                    value={order.recognizedPart?.id ?? ""}
                    disabled={updatingId === order.id}
                    onChange={(e) => updateOrder(order.id, { recognizedPartId: e.target.value || null })}
                    className="min-w-[220px] rounded-md border border-gray-300 px-3 py-2"
                  >
                    <option value="">(부품 없음)</option>
                    {parts.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.name} — {p.size} / {p.material}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="flex flex-col gap-1 text-sm">
                  <span className="text-gray-500">주문 상태</span>
                  <select
                    value={order.status}
                    disabled={updatingId === order.id}
                    onChange={(e) => updateOrder(order.id, { status: e.target.value })}
                    className="rounded-md border border-gray-300 px-3 py-2"
                  >
                    {Object.entries(STATUS_LABEL).map(([value, label]) => (
                      <option key={value} value={value}>
                        {label}
                      </option>
                    ))}
                  </select>
                </label>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
