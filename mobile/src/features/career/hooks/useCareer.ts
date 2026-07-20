import { useMutation } from '@tanstack/react-query';
import { careerApi } from '@core/api/endpoints';
import type { CareerCoachResponse, LearningRoadmapResponse } from '@features/career/models/career';

/** Ask the AI career coach a question (single-shot). */
export const useCareerCoach = () =>
  useMutation<CareerCoachResponse, Error, { question: string; goal_role?: string }>({
    mutationFn: (body) => careerApi.coach(body),
  });

/** Build a learning roadmap toward a goal role from a list of skill gaps. */
export const useRoadmap = () =>
  useMutation<LearningRoadmapResponse, Error, { goal_role: string; gaps: string[] }>({
    mutationFn: (body) => careerApi.roadmap(body),
  });