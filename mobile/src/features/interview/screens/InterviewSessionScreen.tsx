import React, { useState } from 'react';
import { View, Text, TextInput, Pressable, ActivityIndicator, ScrollView } from 'react-native';
import { useInterview } from '@features/interview/hooks/useInterview';

export const InterviewSessionScreen = ({ navigation }: any) => {
  const { active, lastFeedback, submit, submitting, complete, completing, interviewId } = useInterview();
  const [answer, setAnswer] = useState('');
  const isDone = active && !active.text;

  const onSubmit = async () => {
    if (!active) return;
    await submit({ question_id: active.id, text: answer });
    setAnswer('');
  };

  const onComplete = async () => {
    if (interviewId) await complete(interviewId);
    navigation.navigate('Dashboard');
  };

  if (!active) {
    return (
      <View className="flex-1 items-center justify-center">
        <ActivityIndicator />
      </View>
    );
  }

  return (
    <ScrollView className="flex-1 bg-slate-50 p-6">
      <Text className="text-xs text-slate-500 mb-1">{active.topic} · {active.difficulty}</Text>
      <Text className="text-lg font-semibold text-slate-900 mb-4">{active.text}</Text>

      {lastFeedback && (
        <View className="bg-white rounded-2xl p-4 mb-4 border border-slate-200">
          <Text className="text-green-600 font-bold mb-1">Score: {lastFeedback.score.value}/100</Text>
          {lastFeedback.ideal_answer && (
            <Text className="text-slate-700 mb-2">💡 Ideal: {lastFeedback.ideal_answer}</Text>
          )}
          {lastFeedback.mistakes.length > 0 && (
            <Text className="text-red-500 mb-2">⚠️ {lastFeedback.mistakes.join('; ')}</Text>
          )}
          {lastFeedback.follow_up_question && (
            <Text className="text-slate-500">➡️ Follow-up: {lastFeedback.follow_up_question}</Text>
          )}
        </View>
      )}

      {isDone ? (
        <Pressable onPress={onComplete} disabled={completing}
          className="bg-green-600 rounded-xl py-4 items-center">
          {completing ? <ActivityIndicator color="#fff" /> : <Text className="text-white font-semibold">Finish & see summary</Text>}
        </Pressable>
      ) : (
        <>
          <TextInput value={answer} onChangeText={setAnswer} multiline
            placeholder="Type your answer..." textAlignVertical="top"
            className="bg-white border border-slate-200 rounded-xl p-4 min-h-[120px] text-slate-900 mb-4" />
          <Pressable onPress={onSubmit} disabled={submitting}
            className="bg-brand-600 rounded-xl py-4 items-center">
            {submitting ? <ActivityIndicator color="#fff" /> : <Text className="text-white font-semibold">Submit answer</Text>}
          </Pressable>
        </>
      )}
    </ScrollView>
  );
};