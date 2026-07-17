import { createSlice, PayloadAction, createAsyncThunk } from '@reduxjs/toolkit';
import { authApi } from '@core/api/endpoints';
import { tokenStorage } from '@core/storage/mmkv';

export interface AuthState {
  isAuthenticated: boolean;
  user: { email?: string; full_name?: string } | null;
  loading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  isAuthenticated: !!tokenStorage.get(),
  user: null,
  loading: false,
  error: null,
};

export const loginThunk = createAsyncThunk(
  'auth/login',
  async ({ email, password }: { email: string; password: string }, { rejectWithValue }) => {
    try {
      const data = await authApi.login({ email, password });
      tokenStorage.set(data.access_token, data.refresh_token);
      return { email };
    } catch (e: any) {
      return rejectWithValue(e?.response?.data?.message ?? 'Login failed');
    }
  },
);

export const registerThunk = createAsyncThunk(
  'auth/register',
  async (payload: { email: string; password: string; full_name: string }, { rejectWithValue }) => {
    try {
      const data = await authApi.register(payload);
      tokenStorage.set(data.access_token, data.refresh_token);
      return { email: payload.email, full_name: payload.full_name };
    } catch (e: any) {
      return rejectWithValue(e?.response?.data?.message ?? 'Registration failed');
    }
  },
);

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout(state) {
      tokenStorage.clear();
      state.isAuthenticated = false;
      state.user = null;
    },
    restoreSession(state, action: PayloadAction<{ email?: string }>) {
      state.isAuthenticated = true;
      state.user = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginThunk.pending, (s) => { s.loading = true; s.error = null; })
      .addCase(loginThunk.fulfilled, (s, a) => { s.loading = false; s.isAuthenticated = true; s.user = a.payload; })
      .addCase(loginThunk.rejected, (s, a) => { s.loading = false; s.error = a.payload as string; })
      .addCase(registerThunk.pending, (s) => { s.loading = true; s.error = null; })
      .addCase(registerThunk.fulfilled, (s, a) => { s.loading = false; s.isAuthenticated = true; s.user = a.payload; })
      .addCase(registerThunk.rejected, (s, a) => { s.loading = false; s.error = a.payload as string; });
  },
});

export const { logout, restoreSession } = authSlice.actions;
export const authReducer = authSlice.reducer;