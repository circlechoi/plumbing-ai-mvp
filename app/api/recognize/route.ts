import { NextResponse } from "next/server";
import { randomUUID } from "node:crypto";
import { writeFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { prisma } from "@/app/lib/prisma";
import { recognizePart } from "@/app/lib/recognition";
import { getUploadsDir } from "@/app/lib/uploads";
import { checkRateLimit, getClientIp } from "@/app/lib/rateLimit";

const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"] as const;
type AllowedType = (typeof ALLOWED_TYPES)[number];
const MAX_SIZE_BYTES = 10 * 1024 * 1024; // 10MB

function isAllowedType(type: string): type is AllowedType {
  return (ALLOWED_TYPES as readonly string[]).includes(type);
}

export async function POST(req: Request) {
  const ip = getClientIp(req);
  const { allowed, retryAfterSeconds } = checkRateLimit(ip);
  if (!allowed) {
    return NextResponse.json(
      { error: `요청이 너무 많습니다. ${retryAfterSeconds}초 후 다시 시도해주세요.` },
      { status: 429 }
    );
  }

  const formData = await req.formData();
  const file = formData.get("image");

  if (!(file instanceof File)) {
    return NextResponse.json({ error: "이미지 파일이 필요합니다." }, { status: 400 });
  }

  if (!isAllowedType(file.type)) {
    return NextResponse.json({ error: "jpg, png, gif, webp 형식의 이미지만 업로드할 수 있습니다." }, { status: 400 });
  }

  if (file.size > MAX_SIZE_BYTES) {
    return NextResponse.json({ error: "이미지 파일은 10MB를 넘을 수 없습니다." }, { status: 400 });
  }

  const buffer = Buffer.from(await file.arrayBuffer());

  const ext = file.type.split("/")[1];
  const filename = `${randomUUID()}.${ext}`;
  const uploadsDir = getUploadsDir();
  await mkdir(uploadsDir, { recursive: true });
  await writeFile(path.join(uploadsDir, filename), buffer);
  const imageUrl = `/api/uploads/${filename}`;

  let recognized;
  try {
    recognized = await recognizePart({ imageBuffer: buffer });
  } catch (error) {
    const message = error instanceof Error ? error.message : "알 수 없는 오류";
    return NextResponse.json({ error: `AI 인식 기능을 사용할 수 없습니다: ${message}` }, { status: 500 });
  }

  const { result, fallbackUsed, usage } = recognized;

  const log = await prisma.recognitionLog.create({
    data: {
      rawImageUrl: imageUrl,
      aiResponseJson: JSON.stringify(result),
      model: usage.model,
      inputTokens: usage.inputTokens,
      outputTokens: usage.outputTokens,
    },
  });

  const matchedParts = result.matched_db_ids.length
    ? await prisma.part.findMany({ where: { id: { in: result.matched_db_ids } } })
    : [];

  return NextResponse.json({
    recognitionLogId: log.id,
    imageUrl,
    result,
    matchedParts,
    fallbackUsed,
  });
}
