import { useAppDispatch, useAppSelector } from '@core/store/hooks';
import { loginThunk, registerThunk, logout } from '@features/auth/slices/authSlice';

/** Single hook exposing all auth state + actions for screens. */
export const useAuth = () => {
  const dispatch = useAppDispatch();
  const { isAuthenticated, user, loading, error } = useAppSelector((s) => s.auth);

  return {
    isAuthenticated, user, loading, error,
    login: (email: string, password: string) => dispatch(loginThunk({ email, password })),
    register: (email: string, password: string, full_name: string) =>
      dispatch(registerThunk({ email, password, full_name })),
    logout: () => dispatch(logout()),
  };
};