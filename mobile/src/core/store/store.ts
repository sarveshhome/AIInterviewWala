import { configureStore } from '@reduxjs/toolkit';
import { authReducer } from '@features/auth/slices/authSlice';
import { interviewReducer } from '@features/interview/slices/interviewSlice';

/** Redux store with feature slices. API caching is handled by React Query,
 *  so Redux holds only auth + active interview session state. */
export const store = configureStore({
  reducer: {
    auth: authReducer,
    interview: interviewReducer,
  },
  middleware: (getDefault) => getDefault({ serializableCheck: false }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;