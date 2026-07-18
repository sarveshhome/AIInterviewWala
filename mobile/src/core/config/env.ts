/** App-wide runtime configuration. Override via react-native-config for variants. */
import { Platform } from 'react-native';

// In dev, the backend runs on the host machine. The iOS Simulator shares the
// Mac's network so `localhost` works; the Android Emulator is its own VM and
// must use the 10.0.2.2 alias to reach the host's loopback.
const DEV_HOST = Platform.OS === 'android' ? 'http://10.0.2.2:8000' : 'http://localhost:8000';

export const ENV = {
  API_BASE_URL: __DEV__
    ? `${DEV_HOST}/api/v1`
    : 'https://api.aiinterviewcoach.example/api/v1',
  TIMEOUT_MS: 30000,
} as const;