import { NextResponse } from "next/server";
import { createHash } from "node:crypto";

export async function POST(req: Request) {
  const { password } = (await req.json()) as { password?: string };
  const adminPassword = process.env.ADMIN_PASSWORD;

  if (!adminPassword) {
    return NextResponse.json(
      { error: "서버에 ADMIN_PASSWORD가 설정되어 있지 않습니다. .env 파일을 확인하세요." },
      { status: 500 }
    );
  }

  if (password !== adminPassword) {
    return NextResponse.json({ error: "비밀번호가 올바르지 않습니다." }, { status: 401 });
  }

  // 쿠키에 원문 비밀번호 대신 해시값만 저장 (미들웨어에서 동일한 해시로 비교)
  const sessionToken = createHash("sha256").update(adminPassword).digest("hex");
  const res = NextResponse.json({ ok: true });
  res.cookies.set("admin_session", sessionToken, {
    httpOnly: true,
    sameSite: "lax",
    path: "/",
    maxAge: 60 * 60 * 8, // 8시간
  });
  return res;
}
