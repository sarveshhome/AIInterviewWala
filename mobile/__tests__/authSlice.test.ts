import { authReducer, loginThunk } from '@features/auth/slices/authSlice';

describe('authSlice', () => {
  it('handles pending state', () => {
    const action = { type: loginThunk.pending.type };
    const state = authReducer({ isAuthenticated: false, user: null, loading: false, error: null }, action as any);
    expect(state.loading).toBe(true);
    expect(state.error).toBeNull();
  });

  it('handles fulfilled state', () => {
    const action = { type: loginThunk.fulfilled.type, payload: { email: 'a@b.com' } };
    const state = authReducer({ isAuthenticated: false, user: null, loading: true, error: null }, action as any);
    expect(state.isAuthenticated).toBe(true);
    expect(state.user?.email).toBe('a@b.com');
    expect(state.loading).toBe(false);
  });
});