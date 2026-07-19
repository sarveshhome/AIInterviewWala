/** Analytics dashboard models — mirror backend `AnalyticsResponse` (backend/application/dtos/dtos.py). */

export type InterviewStatus = 'pending' | 'in_progress' | 'completed' | 'aborted';

export interface InterviewHistoryItem {
  id: string;
  type: string;
  technology?: string | null;
  status: InterviewStatus;
  score?: number | null;
  completed_at?: string | null; // ISO-8601, may be absent on legacy precomputed docs
}

export interface ProgressPoint {
  date: string; // ISO-8601 (may be '' when no timestamp was recorded)
  score: number;
  label: string; // e.g. "#1 technical"
}

export interface AnalyticsResponse {
  total_interviews: number;
  average_score: number | null;
  weak_areas: string[];
  strong_areas: string[];
  tech_performance: Record<string, number>;
  history: InterviewHistoryItem[];
  progress: ProgressPoint[];
}