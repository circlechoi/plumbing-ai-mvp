"use client";

import { useState } from "react";

export default function CopyButton({ value }: { value: string }) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // 클립보드 접근이 막힌 환경에서는 조용히 무시
    }
  }

  return (
    <button
      type="button"
      onClick={handleCopy}
      className="whitespace-nowrap rounded-md border border-gray-300 px-2 py-0.5 text-xs font-medium text-gray-600 hover:bg-gray-50"
    >
      {copied ? "복사됨!" : "복사"}
    </button>
  );
}
