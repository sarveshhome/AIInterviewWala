import { api } from './client';

/** Centralized API endpoint definitions — one place to find every call. */
export const authApi = {
  register: (body: { email: string; password: string; full_name: string }) =>
    api.post<{ access_token: string; refresh_token: string }>('/auth/register', body),
  login: (body: { email: string; password: string }) =>
    api.post<{ access_token: string; refresh_token: string }>('/auth/login', body),
  oauth: (body: { provider: 'google' | 'linkedin'; token: string }) =>
    api.post<{ access_token: string; refresh_token: string }>('/auth/oauth', body),
  refresh: (refresh_token: string) =>
    api.post<{ access_token: string; refresh_token: string }>('/auth/refresh', { refresh_token }),
};

export const resumeApi = {
  upload: (formData: FormData) => api.upload<{
    id: string; file_name: string; ats_score: number | null;
    missing_skills: string[]; strong_areas: string[]; weak_areas: string[];
    recommended_improvements: string[]; extracted_skills: string[];
  }>('/resume/upload', formData),
};

export const interviewApi = {
  start: (body: { type: string; technology?: string; total_questions?: number }) =>
    api.post<{ id: string; interview_id: string; type: string; topic: string; difficulty: string; text: string; order: number }>('/interview/start', body),
  answer: (body: { question_id: string; text?: string; code?: string; language?: string; duration_seconds?: number }) =>
    api.post<{
      answer_id: string; question_id: string;
      feedback: { score: { value: number }; mistakes: string[]; ideal_answer: string | null; suggested_improvements: string[]; follow_up_question: string | null };
      next_question: { id: string; interview_id: string; type: string; topic: string; difficulty: string; text: string; order: number } | null;
    }>('/interview/answer', body),
  complete: (interviewId: string) =>
    api.post<{ interview_id: string; overall_score: number | null; summary: string | null; completed_at: string | null }>(`/interview/${interviewId}/complete`),
};

export const careerApi = {
  coach: (body: { question: string; goal_role?: string }) => api.post('/career/coach', body),
  roadmap: (body: { goal_role: string; gaps: string[] }) => api.post('/career/roadmap', body),
};

export const dashboardApi = {
  get: () => api.get<{
    total_interviews: number; average_score: number | null;
    weak_areas: string[]; strong_areas: string[]; tech_performance: Record<string, number>;
    history: { id: string; type: string; technology?: string | null; score?: number | null }[];
  }>('/dashboard'),
  history: (skip = 0, limit = 20) => api.get('/interviews', { skip, limit }),
};