/** App-wide runtime configuration. Override via react-native-config for variants. */
export const ENV = {
  API_BASE_URL: __DEV__
    ? 'http://localhost:8000/api/v1'
    : 'https://api.aiinterviewcoach.example/api/v1',
  TIMEOUT_MS: 30000,
} as const;