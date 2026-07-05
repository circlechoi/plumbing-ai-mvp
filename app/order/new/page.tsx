"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useState } from "react";
import OrderStepper from "@/app/components/OrderStepper";
import type { ConfidenceLevel } from "@/app/lib/types";

const PHONE_REGEX = /^[0-9()+\- ]{9,20}$/;

function validate(customerContact: string, deliveryAddress: string, quantity: number) {
  const errors: { customerContact?: string; deliveryAddress?: string; quantity?: string } = {};
  const digitCount = customerContact.replace(/\D/g, "").length;

  if (!customerContact.trim()) {
    errors.customerContact = "연락처를 입력해주세요.";
  } else if (!PHONE_REGEX.test(customerContact.trim()) || digitCount < 9) {
    errors.customerContact = "올바른 연락처 형식이 아닙니다. (예: 010-0000-0000)";
  }

  if (!deliveryAddress.trim()) {
    errors.deliveryAddress = "배송지를 입력해주세요.";
  }

  if (!Number.isInteger(quantity) || quantity < 1) {
    errors.quantity = "수량은 1개 이상이어야 합니다.";
  }

  return errors;
}

function OrderForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const partId = searchParams.get("partId");
  const confidence = searchParams.get("confidence") as ConfidenceLevel | null;
  const recognitionLogId = searchParams.get("recognitionLogId");

  const [customerContact, setCustomerContact] = useState("");
  const [deliveryAddress, setDeliveryAddress] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [fieldErrors, setFieldErrors] = useState<ReturnType<typeof validate>>({});
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const errors = validate(customerContact, deliveryAddress, quantity);
    setFieldErrors(errors);
    if (Object.keys(errors).length > 0) return;

    setSubmitting(true);
    setError(null);
    try {
      const res = await fetch("/api/orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customerContact,
          deliveryAddress,
          quantity,
          recognizedPartId: partId,
          confidence,
          recognitionLogId,
        }),
      });
      const json = await res.json();
      if (!res.ok) {
        setError(json.error ?? "주문 접수 중 오류가 발생했습니다.");
        return;
      }
      router.push(`/order/${json.order.id}`);
    } catch {
      setError("서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto flex max-w-lg flex-col gap-6">
      <OrderStepper current={3} />

      <div>
        <h1 className="text-2xl font-bold">주문 접수</h1>
        <p className="mt-1 text-gray-600">
          {partId ? "선택하신 부품으로 주문을 접수합니다." : "AI가 정확히 인식하지 못한 건이지만, 그대로 접수하실 수 있습니다."}
        </p>
      </div>

      <form onSubmit={handleSubmit} noValidate className="flex flex-col gap-5 rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
        <label className="flex flex-col gap-1">
          <span className="font-medium text-gray-800">연락처</span>
          <input
            type="tel"
            value={customerContact}
            onChange={(e) => {
              setCustomerContact(e.target.value);
              if (fieldErrors.customerContact) setFieldErrors((prev) => ({ ...prev, customerContact: undefined }));
            }}
            placeholder="010-0000-0000"
            className={`rounded-md border px-4 py-3 text-lg focus:outline-none ${
              fieldErrors.customerContact ? "border-red-400 focus:border-red-500" : "border-gray-300 focus:border-blue-500"
            }`}
          />
          {fieldErrors.customerContact && <span className="text-sm text-red-600">{fieldErrors.customerContact}</span>}
        </label>

        <label className="flex flex-col gap-1">
          <span className="font-medium text-gray-800">배송지</span>
          <input
            type="text"
            value={deliveryAddress}
            onChange={(e) => {
              setDeliveryAddress(e.target.value);
              if (fieldErrors.deliveryAddress) setFieldErrors((prev) => ({ ...prev, deliveryAddress: undefined }));
            }}
            placeholder="현장 주소를 입력하세요"
            className={`rounded-md border px-4 py-3 text-lg focus:outline-none ${
              fieldErrors.deliveryAddress ? "border-red-400 focus:border-red-500" : "border-gray-300 focus:border-blue-500"
            }`}
          />
          {fieldErrors.deliveryAddress && <span className="text-sm text-red-600">{fieldErrors.deliveryAddress}</span>}
        </label>

        <label className="flex flex-col gap-1">
          <span className="font-medium text-gray-800">수량</span>
          <input
            type="number"
            min={1}
            value={quantity}
            onChange={(e) => {
              setQuantity(Number(e.target.value));
              if (fieldErrors.quantity) setFieldErrors((prev) => ({ ...prev, quantity: undefined }));
            }}
            className={`rounded-md border px-4 py-3 text-lg focus:outline-none ${
              fieldErrors.quantity ? "border-red-400 focus:border-red-500" : "border-gray-300 focus:border-blue-500"
            }`}
          />
          {fieldErrors.quantity && <span className="text-sm text-red-600">{fieldErrors.quantity}</span>}
        </label>

        {error && <div className="rounded-md border border-red-300 bg-red-50 p-3 text-red-800">{error}</div>}

        <button
          type="submit"
          disabled={submitting}
          className="w-full rounded-lg bg-blue-600 px-6 py-4 text-lg font-semibold text-white transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400"
        >
          {submitting ? "접수 중..." : "주문 접수하기"}
        </button>
      </form>

      <Link href="/" className="text-center text-sm font-medium text-blue-600 hover:underline">
        ← 이전으로 (다른 사진으로 다시 시작하기)
      </Link>
    </div>
  );
}

export default function OrderNewPage() {
  return (
    <Suspense>
      <OrderForm />
    </Suspense>
  );
}
