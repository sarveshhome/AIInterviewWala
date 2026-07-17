// Mock MMKV for jest
jest.mock('react-native-mmkv', () => ({
  MMKV: class {
    store = {};
    getString(k) { return this.store[k]; }
    set(k, v) { this.store[k] = String(v); }
    delete(k) { delete this.store[k]; }
  },
}));