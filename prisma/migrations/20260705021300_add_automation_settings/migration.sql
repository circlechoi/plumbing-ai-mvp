-- CreateTable
CREATE TABLE "Settings" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT DEFAULT 1,
    "autoApproveEnabled" BOOLEAN NOT NULL DEFAULT false,
    "updatedAt" DATETIME NOT NULL
);

-- RedefineTables
PRAGMA defer_foreign_keys=ON;
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Order" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "customerContact" TEXT NOT NULL,
    "deliveryAddress" TEXT NOT NULL,
    "quantity" INTEGER NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'RECEIVED',
    "recognizedPartId" TEXT,
    "aiTopPickId" TEXT,
    "confidenceLevel" TEXT,
    "needsManualCheck" BOOLEAN NOT NULL DEFAULT false,
    "autoProcessed" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL,
    CONSTRAINT "Order_recognizedPartId_fkey" FOREIGN KEY ("recognizedPartId") REFERENCES "Part" ("id") ON DELETE SET NULL ON UPDATE CASCADE
);
INSERT INTO "new_Order" ("aiTopPickId", "confidenceLevel", "createdAt", "customerContact", "deliveryAddress", "id", "needsManualCheck", "quantity", "recognizedPartId", "status", "updatedAt") SELECT "aiTopPickId", "confidenceLevel", "createdAt", "customerContact", "deliveryAddress", "id", "needsManualCheck", "quantity", "recognizedPartId", "status", "updatedAt" FROM "Order";
DROP TABLE "Order";
ALTER TABLE "new_Order" RENAME TO "Order";
PRAGMA foreign_keys=ON;
PRAGMA defer_foreign_keys=OFF;
