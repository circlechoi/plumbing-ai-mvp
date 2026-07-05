const STEPS = ["사진 업로드", "AI 인식 결과", "주문 정보 입력", "접수 완료"] as const;

export default function OrderStepper({ current }: { current: 1 | 2 | 3 | 4 }) {
  return (
    <ol className="flex items-center gap-2 overflow-x-auto text-xs sm:text-sm">
      {STEPS.map((label, i) => {
        const step = (i + 1) as 1 | 2 | 3 | 4;
        const isDone = step < current;
        const isCurrent = step === current;
        return (
          <li key={label} className="flex shrink-0 items-center gap-2">
            <div className="flex items-center gap-2">
              <span
                className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full font-semibold ${
                  isCurrent
                    ? "bg-blue-600 text-white"
                    : isDone
                      ? "bg-green-600 text-white"
                      : "bg-gray-200 text-gray-500"
                }`}
              >
                {isDone ? "✓" : step}
              </span>
              <span
                className={`whitespace-nowrap ${
                  isCurrent ? "font-semibold text-gray-900" : isDone ? "text-gray-600" : "text-gray-400"
                }`}
              >
                {label}
              </span>
            </div>
            {step !== 4 && <span className="h-px w-6 shrink-0 bg-gray-200 sm:w-10" />}
          </li>
        );
      })}
    </ol>
  );
}
