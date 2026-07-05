import { NextResponse } from "next/server";
import { prisma } from "@/app/lib/prisma";

export async function GET(_req: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const order = await prisma.order.findUnique({
    where: { id },
    include: { recognizedPart: true, recognitionLogs: true },
  });

  if (!order) {
    return NextResponse.json({ error: "주문을 찾을 수 없습니다." }, { status: 404 });
  }

  return NextResponse.json({ order });
}

export async function PATCH(req: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const body = await req.json();
  const { status, recognizedPartId } = body as {
    status?: "RECEIVED" | "CHECKING" | "COMPLETED";
    recognizedPartId?: string | null;
  };

  const data: { status?: typeof status; recognizedPartId?: string | null; needsManualCheck?: boolean } = {};
  if (status) data.status = status;
  if (recognizedPartId !== undefined) {
    data.recognizedPartId = recognizedPartId;
    // 관리자가 직접 부품을 재지정하면 수동 확인이 해소된 것으로 처리
    data.needsManualCheck = false;
  }

  const order = await prisma.order.update({
    where: { id },
    data,
    include: { recognizedPart: true, recognitionLogs: true },
  });

  return NextResponse.json({ order });
}
