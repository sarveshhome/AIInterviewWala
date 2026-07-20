import React, { useState } from 'react';
import { View, Text, TextInput, ScrollView, KeyboardTypeOptions } from 'react-native';
import { Button } from '@shared/components/Button';
import { useCareerCoach, useRoadmap } from '@features/career/hooks/useCareer';
import type { CareerCoachResponse, LearningRoadmapResponse } from '@features/career/models/career';

type Mode = 'coach' | 'roadmap';

const inputClass =
  'border border-slate-200 rounded-xl px-4 py-3 text-slate-900 mb-3 bg-white';

/** Small labelled input — reused across both panes. */
const Field = ({
  label, value, onChange, placeholder, multiline, keyboardType,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  multiline?: boolean;
  keyboardType?: KeyboardTypeOptions;
}) => (
  <View>
    <Text className="text-slate-700 font-medium mb-1">{label}</Text>
    <TextInput
      value={value}
      onChangeText={onChange}
      placeholder={placeholder}
      placeholderTextColor="#94a3b8"
      multiline={multiline}
      keyboardType={keyboardType}
      autoCapitalize="none"
      className={inputClass}
    />
  </View>
);

const ErrorLine = ({ message }: { message?: string }) =>
  message ? <Text className="text-red-500 mb-3">{message}</Text> : null;

/** Coach result — answer + bulleted action items & resources. */
const CoachResult = ({ data }: { data: CareerCoachResponse }) => (
  <View className="bg-slate-50 rounded-2xl p-4 border border-slate-200">
    <Text className="font-semibold text-slate-900 mb-1">Answer</Text>
    <Text className="text-slate-700 mb-3">{data.answer}</Text>
    {data.action_items.length > 0 && (
      <>
        <Text className="font-semibold text-slate-900">Action items</Text>
        {data.action_items.map((a) => <Text key={a} className="text-slate-700">• {a}</Text>)}
      </>
    )}
    {data.resources.length > 0 && (
      <>
        <Text className="font-semibold text-slate-900 mt-2">Resources</Text>
        {data.resources.map((r) => <Text key={r} className="text-slate-700">• {r}</Text>)}
      </>
    )}
  </View>
);

/** Roadmap result — header + milestone cards. */
const RoadmapResult = ({ data }: { data: LearningRoadmapResponse }) => (
  <View className="bg-slate-50 rounded-2xl p-4 border border-slate-200">
    <Text className="text-lg font-bold text-slate-900">{data.title}</Text>
    <Text className="text-slate-500 mb-3">~{data.est_total_weeks} weeks total</Text>
    {data.milestones.map((m, i) => (
      <View key={`${m.title}-${i}`} className="bg-white rounded-xl p-3 border border-slate-200 mb-3">
        <View className="flex-row justify-between items-center mb-1">
          <Text className="font-semibold text-slate-900 flex-1">{i + 1}. {m.title}</Text>
          <Text className="text-slate-500 text-xs">{m.est_weeks}w</Text>
        </View>
        {m.topics.length > 0 && (
          <Text className="text-slate-700 mb-1">Topics: {m.topics.join(', ')}</Text>
        )}
        {m.resources.length > 0 && (
          <>
            <Text className="text-slate-500 text-xs mt-1">Resources</Text>
            {m.resources.map((r) => <Text key={r} className="text-slate-700 text-xs">• {r}</Text>)}
          </>
        )}
      </View>
    ))}
  </View>
);

export const CareerScreen = () => {
  const [mode, setMode] = useState<Mode>('coach');

  // Coach form state
  const [question, setQuestion] = useState('');
  const [goalRole, setGoalRole] = useState('');
  const coach = useCareerCoach();

  // Roadmap form state
  const [roadmapRole, setRoadmapRole] = useState('');
  const [gapsText, setGapsText] = useState('');
  const roadmap = useRoadmap();

  const askCoach = () => {
    if (!question.trim()) return;
    coach.mutate({ question: question.trim(), goal_role: goalRole.trim() || undefined });
  };

  const buildRoadmap = () => {
    const gaps = gapsText.split(',').map((g) => g.trim()).filter(Boolean);
    if (!roadmapRole.trim() || gaps.length === 0) return;
    roadmap.mutate({ goal_role: roadmapRole.trim(), gaps });
  };

  return (
    <ScrollView className="flex-1 bg-white p-6" keyboardShouldPersistTaps="handled">
      <Text className="text-2xl font-bold text-slate-900 mb-1">Career</Text>
      <Text className="text-slate-500 mb-5">Ask the coach or build a learning roadmap.</Text>

      {/* Segmented control */}
      <View className="flex-row bg-slate-100 rounded-xl p-1 mb-6">
        {(['coach', 'roadmap'] as Mode[]).map((m) => (
          <View key={m} className="flex-1">
            <Button
              title={m === 'coach' ? 'Coach' : 'Roadmap'}
              onPress={() => setMode(m)}
              variant={mode === m ? 'primary' : 'secondary'}
            />
          </View>
        ))}
      </View>

      {mode === 'coach' ? (
        <>
          <Field label="Goal role (optional)" value={goalRole} onChange={setGoalRole} placeholder="e.g. Senior Backend Engineer" />
          <Field label="Question" value={question} onChange={setQuestion} placeholder="How do I move from IC to staff?" multiline />
          <Button title="Ask coach" onPress={askCoach} loading={coach.isPending} disabled={!question.trim()} />
          <ErrorLine message={coach.error?.message} />
          {coach.data && <View className="mt-4"><CoachResult data={coach.data} /></View>}
        </>
      ) : (
        <>
          <Field label="Goal role" value={roadmapRole} onChange={setRoadmapRole} placeholder="e.g. Staff Engineer" />
          <Field label="Skill gaps (comma separated)" value={gapsText} onChange={setGapsText} placeholder="system design, leadership" />
          <Button title="Build roadmap" onPress={buildRoadmap} loading={roadmap.isPending} disabled={!roadmapRole.trim() || !gapsText.trim()} />
          <ErrorLine message={roadmap.error?.message} />
          {roadmap.data && <View className="mt-4"><RoadmapResult data={roadmap.data} /></View>}
        </>
      )}
    </ScrollView>
  );
};