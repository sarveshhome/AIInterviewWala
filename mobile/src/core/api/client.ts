import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import { ENV } from '@core/config/env';
import { tokenStorage } from '@core/storage/mmkv';

/** Axios instance with auth interceptor + automatic token refresh on 401. */
export const apiClient: AxiosInstance = axios.create({
  baseURL: ENV.API_BASE_URL,
  timeout: ENV.TIMEOUT_MS,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = tokenStorage.get();
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

let refreshing = false;

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config as InternalAxiosRequestConfig & { _retry?: boolean };
    if (error.response?.status === 401 && !original?._retry && tokenStorage.getRefresh()) {
      original._retry = true;
      try {
        const { data } = await axios.post(`${ENV.API_BASE_URL}/auth/refresh`, {
          refresh_token: tokenStorage.getRefresh(),
        });
        tokenStorage.set(data.access_token, data.refresh_token);
        original.headers!.Authorization = `Bearer ${data.access_token}`;
        return apiClient(original);
      } catch {
        tokenStorage.clear();
      }
    }
    return Promise.reject(error);
  },
);

/** Typed request helpers. */
export const api = {
  get: <T>(url: string, params?: object) => apiClient.get<T>(url, { params }).then((r) => r.data),
  post: <T>(url: string, body?: object) => apiClient.post<T>(url, body).then((r) => r.data),
  upload: <T>(url: string, formData: FormData) =>
    apiClient.post<T>(url, formData, { headers: { 'Content-Type': 'multipart/form-data' } }).then((r) => r.data),
};