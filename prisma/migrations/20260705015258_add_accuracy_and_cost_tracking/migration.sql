-- AlterTable
ALTER TABLE "Order" ADD COLUMN "aiTopPickId" TEXT;

-- AlterTable
ALTER TABLE "RecognitionLog" ADD COLUMN "inputTokens" INTEGER;
ALTER TABLE "RecognitionLog" ADD COLUMN "model" TEXT;
ALTER TABLE "RecognitionLog" ADD COLUMN "outputTokens" INTEGER;
