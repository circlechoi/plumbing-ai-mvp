import path from "node:path";

// 로컬 개발: public/uploads. Railway 등 배포 환경: 영구 볼륨 경로(UPLOADS_DIR)를 사용해
// 재배포 후에도 이미지가 유지되게 한다.
export function getUploadsDir() {
  return process.env.UPLOADS_DIR
    ? path.resolve(process.env.UPLOADS_DIR)
    : path.join(process.cwd(), "public", "uploads");
}
