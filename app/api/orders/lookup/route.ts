import { NextResponse } from "next/server";
import { prisma } from "@/app/lib/prisma";

function digitsOnly(s: string) {
  return s.replace(/\D/g, "");
}

export async function POST(req: Request) {
  const { orderId, phone } = (await req.json()) as { orderId?: string; phone?: string };

  if (!orderId?.trim() || !phone?.trim()) {
    return NextResponse.json({ error: "주문번호와 연락처를 모두 입력해주세요." }, { status: 400 });
  }

  const order = await prisma.order.findUnique({ where: { id: orderId.trim() } });

  // 주문이 없거나 연락처가 일치하지 않아도 동일한 에러 메시지로 응답한다 (주문 존재 여부 노출 방지)
  if (!order || digitsOnly(order.customerContact) !== digitsOnly(phone)) {
    return NextResponse.json(
      { error: "일치하는 주문 정보를 찾을 수 없습니다. 주문번호와 연락처를 다시 확인해주세요." },
      { status: 404 }
    );
  }

  return NextResponse.json({ orderId: order.id });
}
