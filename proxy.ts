import { NextResponse, type NextRequest } from "next/server";
import { createHash } from "node:crypto";

export function proxy(req: NextRequest) {
  if (req.nextUrl.pathname === "/admin/login") {
    return NextResponse.next();
  }

  const adminPassword = process.env.ADMIN_PASSWORD;
  // ADMIN_PASSWORD가 설정되지 않은 경우 게이트를 적용하지 않음 (로컬 데모 편의)
  if (!adminPassword) {
    return NextResponse.next();
  }

  const expected = createHash("sha256").update(adminPassword).digest("hex");
  const session = req.cookies.get("admin_session")?.value;

  if (session === expected) {
    return NextResponse.next();
  }

  const loginUrl = new URL("/admin/login", req.url);
  loginUrl.searchParams.set("next", req.nextUrl.pathname);
  return NextResponse.redirect(loginUrl);
}

export const config = {
  matcher: ["/admin/:path*"],
};
