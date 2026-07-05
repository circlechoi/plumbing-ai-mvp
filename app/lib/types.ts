export type ConfidenceLevel = "high" | "medium" | "low";

export interface RecognitionResult {
  part_name_guess: string;
  size_guess: string;
  material_guess: string;
  confidence: ConfidenceLevel;
  reasoning: string;
  matched_db_ids: string[];
}
