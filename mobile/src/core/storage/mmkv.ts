import { MMKV } from 'react-native-mmkv';

/** Single MMKV instance for the app — fast, encrypted-capable key/value storage. */
export const storage = new MMKV({
  id: 'aic-storage',
  encryptionKey: undefined, // set a key in production for at-rest encryption
});

export const StorageKeys = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER: 'user',
  ONBOARDED: 'onboarded',
} as const;

export const tokenStorage = {
  get: () => storage.getString(StorageKeys.ACCESS_TOKEN) ?? null,
  getRefresh: () => storage.getString(StorageKeys.REFRESH_TOKEN) ?? null,
  set: (access: string, refresh: string) => {
    storage.set(StorageKeys.ACCESS_TOKEN, access);
    storage.set(StorageKeys.REFRESH_TOKEN, refresh);
  },
  clear: () => {
    storage.delete(StorageKeys.ACCESS_TOKEN);
    storage.delete(StorageKeys.REFRESH_TOKEN);
  },
};