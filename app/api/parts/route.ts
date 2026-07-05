import { NextResponse } from "next/server";
import { prisma } from "@/app/lib/prisma";

export async function GET() {
  const parts = await prisma.part.findMany({
    orderBy: { createdAt: "asc" },
    include: { compatibleWith: true },
  });
  return NextResponse.json({ parts });
}

export async function POST(req: Request) {
  const body = await req.json();
  const { name, size, material, compatibleWithIds } = body as {
    name?: string;
    size?: string;
    material?: string;
    compatibleWithIds?: string[];
  };

  if (!name?.trim() || !size?.trim() || !material?.trim()) {
    return NextResponse.json({ error: "name, size, material은 필수입니다." }, { status: 400 });
  }

  const part = await prisma.part.create({
    data: {
      name: name.trim(),
      size: size.trim(),
      material: material.trim(),
      ...(compatibleWithIds?.length
        ? { compatibleWith: { connect: compatibleWithIds.map((id) => ({ id })) } }
        : {}),
    },
    include: { compatibleWith: true },
  });

  // 자기참조 다대다 관계이므로, 상대 부품 쪽에서도 이 새 부품이 호환 목록에 보이도록 반대 방향도 연결한다
  if (compatibleWithIds?.length) {
    await Promise.all(
      compatibleWithIds.map((otherId) =>
        prisma.part.update({
          where: { id: otherId },
          data: { compatibleWith: { connect: { id: part.id } } },
        })
      )
    );
  }

  return NextResponse.json({ part }, { status: 201 });
}
