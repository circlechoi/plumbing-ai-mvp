import { prisma } from "@/app/lib/prisma";
import { notFound } from "next/navigation";
import Link from "next/link";
import OrderStepper from "@/app/components/OrderStepper";
import CopyButton from "@/app/components/CopyButton";

const STATUS_LABEL: Record<string, string> = {
  RECEIVED: "접수",
  CHECKING: "확인중",
  COMPLETED: "완료",
};

const CONFIDENCE_LABEL: Record<string, string> = {
  HIGH: "높음",
  MEDIUM: "중간",
  LOW: "낮음",
};

export default async function OrderDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const order = await prisma.order.findUnique({
    where: { id },
    include: { recognizedPart: true },
  });

  if (!order) {
    notFound();
  }

  return (
    <div className="mx-auto flex max-w-lg flex-col gap-6">
      <OrderStepper current={4} />

      <div className="rounded-lg border border-green-200 bg-green-50 p-6 text-center">
        <p className="text-3xl">✅</p>
        <h1 className="mt-2 text-xl font-bold text-green-900">주문이 접수되었습니다</h1>
        <p className="mt-1 text-green-800">
          영업일 기준 1일 이내 담당자가 확인 후 연락드립니다. 문의 시 아래 주문번호를 알려주시면
          빠르게 도와드릴 수 있습니다.
        </p>
      </div>

      <div className="flex flex-col gap-4 rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">주문 정보</h2>
          <span className="rounded-full bg-gray-100 px-3 py-1 text-sm font-medium text-gray-700">
            {STATUS_LABEL[order.status] ?? order.status}
          </span>
        </div>

        <dl className="flex flex-col gap-3 text-sm">
          <div className="flex justify-between border-b border-gray-100 pb-2">
            <dt className="text-gray-500">주문 번호</dt>
            <dd className="flex items-center gap-2">
              <span className="font-mono">{order.id}</span>
              <CopyButton value={order.id} />
            </dd>
          </div>
          <div className="flex justify-between border-b border-gray-100 pb-2">
            <dt className="text-gray-500">연락처</dt>
            <dd>{order.customerContact}</dd>
          </div>
          <div className="flex justify-between border-b border-gray-100 pb-2">
            <dt className="text-gray-500">배송지</dt>
            <dd>{order.deliveryAddress}</dd>
          </div>
          <div className="flex justify-between border-b border-gray-100 pb-2">
            <dt className="text-gray-500">수량</dt>
            <dd>{order.quantity}개</dd>
          </div>
          <div className="flex justify-between border-b border-gray-100 pb-2">
            <dt className="text-gray-500">AI 인식 부품</dt>
            <dd>
              {order.recognizedPart
                ? `${order.recognizedPart.name} (${order.recognizedPart.size}, ${order.recognizedPart.material})`
                : "인식된 부품 없음 — 관리자 확인 필요"}
            </dd>
          </div>
          {order.confidenceLevel && (
            <div className="flex justify-between">
              <dt className="text-gray-500">AI 신뢰도</dt>
              <dd>{CONFIDENCE_LABEL[order.confidenceLevel] ?? order.confidenceLevel}</dd>
            </div>
          )}
        </dl>

        {order.needsManualCheck && (
          <div className="rounded-md border border-yellow-200 bg-yellow-50 p-3 text-sm text-yellow-800">
            이 주문은 관리자의 수동 확인이 필요한 건으로 표시되었습니다.
          </div>
        )}
      </div>

      <Link
        href="/"
        className="w-full rounded-lg bg-blue-600 px-6 py-3 text-center text-lg font-semibold text-white transition-colors hover:bg-blue-700"
      >
        새 부품 인식하러 가기
      </Link>

      <p className="text-center text-sm text-gray-500">
        나중에 주문 상태가 궁금하시면{" "}
        <Link href="/order-lookup" className="font-medium text-blue-600 hover:underline">
          주문 조회
        </Link>
        에서 연락처와 주문번호로 다시 확인하실 수 있습니다.
      </p>
    </div>
  );
}
