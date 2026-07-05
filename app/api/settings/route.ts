import { NextResponse } from "next/server";
import { prisma } from "@/app/lib/prisma";

export async function GET() {
  const settings = await prisma.settings.upsert({
    where: { id: 1 },
    update: {},
    create: { id: 1 },
  });
  return NextResponse.json({ settings });
}

export async function PATCH(req: Request) {
  const { autoApproveEnabled } = (await req.json()) as { autoApproveEnabled?: boolean };

  if (typeof autoApproveEnabled !== "boolean") {
    return NextResponse.json({ error: "autoApproveEnabled는 boolean이어야 합니다." }, { status: 400 });
  }

  const settings = await prisma.settings.upsert({
    where: { id: 1 },
    update: { autoApproveEnabled },
    create: { id: 1, autoApproveEnabled },
  });

  return NextResponse.json({ settings });
}
