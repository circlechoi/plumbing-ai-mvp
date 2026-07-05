-- CreateTable
CREATE TABLE "Part" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "size" TEXT NOT NULL,
    "material" TEXT NOT NULL,
    "imageUrl" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateTable
CREATE TABLE "Order" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "customerContact" TEXT NOT NULL,
    "deliveryAddress" TEXT NOT NULL,
    "quantity" INTEGER NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'RECEIVED',
    "recognizedPartId" TEXT,
    "confidenceLevel" TEXT,
    "needsManualCheck" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "Order_recognizedPartId_fkey" FOREIGN KEY ("recognizedPartId") REFERENCES "Part" ("id") ON DELETE SET NULL ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "RecognitionLog" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "orderId" TEXT,
    "rawImageUrl" TEXT NOT NULL,
    "aiResponseJson" TEXT NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "RecognitionLog_orderId_fkey" FOREIGN KEY ("orderId") REFERENCES "Order" ("id") ON DELETE SET NULL ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "_PartCompatibility" (
    "A" TEXT NOT NULL,
    "B" TEXT NOT NULL,
    CONSTRAINT "_PartCompatibility_A_fkey" FOREIGN KEY ("A") REFERENCES "Part" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "_PartCompatibility_B_fkey" FOREIGN KEY ("B") REFERENCES "Part" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "_PartCompatibility_AB_unique" ON "_PartCompatibility"("A", "B");

-- CreateIndex
CREATE INDEX "_PartCompatibility_B_index" ON "_PartCompatibility"("B");
