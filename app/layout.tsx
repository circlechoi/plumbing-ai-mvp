import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "배관·설비 자재 AI 인식 매칭",
  description: "부품 사진을 올리면 AI가 규격을 추정하고 대체 부품을 추천합니다 (데모)",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="ko"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-gray-50 text-gray-900">
        <header className="border-b border-gray-200 bg-white">
          <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
            <Link href="/" className="text-lg font-bold tracking-tight">
              🔧 설비자재 AI 매칭 (데모)
            </Link>
            <nav className="flex gap-4 text-sm font-medium text-gray-600">
              <Link href="/" className="hover:text-gray-900">
                부품 인식
              </Link>
              <Link href="/order-lookup" className="hover:text-gray-900">
                주문 조회
              </Link>
              <Link href="/admin" className="hover:text-gray-900">
                관리자
              </Link>
            </nav>
          </div>
        </header>
        <main className="mx-auto w-full max-w-5xl flex-1 px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
