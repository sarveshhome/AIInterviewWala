import { useQuery } from '@tanstack/react-query';
import { dashboardApi } from '@core/api/endpoints';

export const useDashboard = () =>
  useQuery({ queryKey: ['dashboard'], queryFn: dashboardApi.get, staleTime: 60_000 });

export const useHistory = (skip = 0, limit = 20) =>
  useQuery({ queryKey: ['history', skip, limit], queryFn: () => dashboardApi.history(skip, limit), staleTime: 30_000 });