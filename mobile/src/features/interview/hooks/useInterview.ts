import { useMutation } from '@tanstack/react-query';
import { interviewApi } from '@core/api/endpoints';
import { useAppDispatch, useAppSelector } from '@core/store/hooks';
import { setActiveQuestion, setFeedback, reset } from '@features/interview/slices/interviewSlice';

/** Interview orchestration hook: start → answer → eval + next question. */
export const useInterview = () => {
  const dispatch = useAppDispatch();
  const { active, interviewId, lastFeedback, history } = useAppSelector((s) => s.interview);

  const startMutation = useMutation({
    mutationFn: interviewApi.start,
    onSuccess: (q) => dispatch(setActiveQuestion(q)),
  });

  const answerMutation = useMutation({
    mutationFn: interviewApi.answer,
    onSuccess: (data, vars) => {
      dispatch(setFeedback({ feedback: data.feedback, question: active?.text ?? '', answer: vars.text ?? vars.code ?? '' }));
      if (data.next_question) dispatch(setActiveQuestion(data.next_question));
      else dispatch(setActiveQuestion({ ...active!, text: '' })); // mark end-of-interview
    },
  });

  const completeMutation = useMutation({ mutationFn: interviewApi.complete });

  return {
    active, interviewId, lastFeedback, history,
    start: startMutation.mutateAsync, startLoading: startMutation.isPending,
    submit: answerMutation.mutateAsync, submitting: answerMutation.isPending,
    complete: completeMutation.mutateAsync, completing: completeMutation.isPending,
    reset: () => dispatch(reset()),
  };
};