import { prisma } from "../app/lib/prisma";

// 배관/설비 부속 목업 데이터 (강남·서초 인테리어 시공 현장에서 흔히 쓰이는 부속 기준)
const parts = [
  { key: "pvc-socket-20", name: "PVC 소켓 이음관", size: "20mm", material: "PVC" },
  { key: "pvc-socket-25", name: "PVC 소켓 이음관", size: "25mm", material: "PVC" },
  { key: "pvc-socket-32", name: "PVC 소켓 이음관", size: "32mm", material: "PVC" },
  { key: "pvc-elbow-20", name: "PVC 엘보 (90도)", size: "20mm", material: "PVC" },
  { key: "pvc-elbow-25", name: "PVC 엘보 (90도)", size: "25mm", material: "PVC" },
  { key: "pvc-tee-20", name: "PVC 티(T) 이음관", size: "20mm", material: "PVC" },
  { key: "pvc-union-25", name: "PVC 유니온", size: "25mm", material: "PVC" },
  { key: "pvc-cap-20", name: "PVC 캡 (막음마개)", size: "20mm", material: "PVC" },
  { key: "brass-nipple-15a", name: "황동 니플", size: "15A (1/2인치)", material: "황동(Brass)" },
  { key: "brass-nipple-20a", name: "황동 니플", size: "20A (3/4인치)", material: "황동(Brass)" },
  { key: "sus-nipple-15a", name: "스테인리스 니플", size: "15A (1/2인치)", material: "STS304" },
  { key: "sus-nipple-20a", name: "스테인리스 니플", size: "20A (3/4인치)", material: "STS304" },
  { key: "brass-socket-20a", name: "황동 소켓 이음관", size: "20A (3/4인치)", material: "황동(Brass)" },
  { key: "sus-socket-20a", name: "스테인리스 소켓 이음관", size: "20A (3/4인치)", material: "STS304" },
  { key: "brass-socket-25a", name: "황동 소켓 이음관", size: "25A (1인치)", material: "황동(Brass)" },
  { key: "gate-valve-15a", name: "게이트밸브", size: "15A (1/2인치)", material: "황동(Brass)" },
  { key: "gate-valve-20a", name: "게이트밸브", size: "20A (3/4인치)", material: "황동(Brass)" },
  { key: "ball-valve-15a", name: "볼밸브", size: "15A (1/2인치)", material: "스테인리스" },
  { key: "ball-valve-20a", name: "볼밸브", size: "20A (3/4인치)", material: "스테인리스" },
  { key: "check-valve-15a", name: "체크밸브", size: "15A (1/2인치)", material: "황동(Brass)" },
  { key: "check-valve-20a", name: "체크밸브", size: "20A (3/4인치)", material: "황동(Brass)" },
  { key: "union-15a", name: "유니온 이음관", size: "15A (1/2인치)", material: "황동(Brass)" },
  { key: "union-20a", name: "유니온 이음관", size: "20A (3/4인치)", material: "황동(Brass)" },
  { key: "flange-50a", name: "플랜지", size: "50A (2인치)", material: "주철(Cast Iron)" },
  { key: "strainer-20a", name: "스트레이너 (여과기)", size: "20A (3/4인치)", material: "황동(Brass)" },
  { key: "clamp-25", name: "클램프 (배관 고정용)", size: "25mm", material: "스테인리스" },
  { key: "anchor-m8", name: "앵커볼트", size: "M8 x 60mm", material: "아연도금강" },
  { key: "anchor-m10", name: "앵커볼트", size: "M10 x 80mm", material: "아연도금강" },
  { key: "anchor-m12", name: "앵커볼트", size: "M12 x 100mm", material: "아연도금강" },
  { key: "wing-anchor-m8", name: "나비형 앵커볼트", size: "M8 x 60mm", material: "아연도금강" },
] as const;

// 서로 호환(대체 가능)되는 부품 그룹 (같은 규격대, 다른 재질/형태의 대체품)
const compatibilityGroups: string[][] = [
  ["brass-nipple-15a", "sus-nipple-15a"],
  ["brass-nipple-20a", "sus-nipple-20a"],
  ["brass-socket-20a", "sus-socket-20a"],
  ["gate-valve-15a", "ball-valve-15a"],
  ["gate-valve-20a", "ball-valve-20a"],
  ["anchor-m8", "wing-anchor-m8"],
];

async function main() {
  console.log("시딩 시작: 부품 마스터 데이터...");

  const idByKey = new Map<string, string>();

  for (const p of parts) {
    const created = await prisma.part.upsert({
      where: { id: p.key },
      update: { name: p.name, size: p.size, material: p.material },
      create: { id: p.key, name: p.name, size: p.size, material: p.material },
    });
    idByKey.set(p.key, created.id);
  }

  console.log(`부품 ${parts.length}개 시딩 완료.`);

  console.log("호환 관계 연결 중...");
  for (const group of compatibilityGroups) {
    const ids = group.map((key) => idByKey.get(key)!);
    for (const id of ids) {
      const others = ids.filter((otherId) => otherId !== id);
      await prisma.part.update({
        where: { id },
        data: {
          compatibleWith: { connect: others.map((otherId) => ({ id: otherId })) },
        },
      });
    }
  }

  console.log(`호환 그룹 ${compatibilityGroups.length}개 연결 완료.`);
  console.log("시딩 완료!");
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
