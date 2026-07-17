import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface QuestionModel {
  id: string;
  interview_id: string;
  type: string;
  topic: string;
  difficulty: string;
  text: string;
  order: number;
}

export interface FeedbackModel {
  score: { value: number };
  mistakes: string[];
  ideal_answer: string | null;
  suggested_improvements: string[];
  follow_up_question: string | null;
}

interface InterviewState {
  active: QuestionModel | null;
  interviewId: string | null;
  lastFeedback: FeedbackModel | null;
  history: { question: string; answer: string; score: number }[];
}

const initialState: InterviewState = { active: null, interviewId: null, lastFeedback: null, history: [] };

const interviewSlice = createSlice({
  name: 'interview',
  initialState,
  reducers: {
    setActiveQuestion(state, action: PayloadAction<QuestionModel>) {
      state.active = action.payload;
      state.interviewId = action.payload.interview_id;
    },
    setFeedback(state, action: PayloadAction<{ feedback: FeedbackModel; question: string; answer: string }>) {
      state.lastFeedback = action.payload.feedback;
      state.history.push({ question: action.payload.question, answer: action.payload.answer, score: action.payload.feedback.score.value });
    },
    reset(state) {
      state.active = null; state.interviewId = null; state.lastFeedback = null; state.history = [];
    },
  },
});

export const { setActiveQuestion, setFeedback, reset } = interviewSlice.actions;
export const interviewReducer = interviewSlice.reducer;