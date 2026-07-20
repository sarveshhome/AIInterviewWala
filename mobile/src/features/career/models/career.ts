/** Career feature response types — mirror backend Cohere career AI JSON. */

/** POST /career/coach — structured coaching answer. */
export interface CareerCoachResponse {
  answer: string;
  action_items: string[];
  resources: string[];
}

/** A single step in a learning roadmap. */
export interface RoadmapMilestone {
  title: string;
  topics: string[];
  resources: string[];
  est_weeks: number;
}

/** POST /career/roadmap — a phased learning plan toward a goal role. */
export interface LearningRoadmapResponse {
  title: string;
  est_total_weeks: number;
  milestones: RoadmapMilestone[];
}