import React, { useState } from 'react';
import { View, Text, TextInput, Pressable, ActivityIndicator, ScrollView } from 'react-native';
import { useInterview } from '@features/interview/hooks/useInterview';

const TYPES = [
  { key: 'technical', label: 'Technical', techs: ['.NET', 'React', 'React Native', 'Python', 'Kafka', 'GraphQL', 'Azure', 'AWS', 'GCP', 'Docker', 'Kubernetes', 'Microservices', 'MongoDB', 'SQL Server', 'Redis', 'System Design'] },
  { key: 'coding', label: 'Coding', techs: ['Python', 'Java', 'C#', 'JavaScript', 'TypeScript'] },
  { key: 'behavioral', label: 'Behavioral', techs: [] },
  { key: 'system_design', label: 'System Design', techs: ['Scalability', 'Caching', 'Messaging', 'Database'] },
  { key: 'voice', label: 'Voice', techs: [] },
];

export const InterviewSetupScreen = ({ navigation }: any) => {
  const { start, startLoading } = useInterview();
  const [type, setType] = useState('technical');
  const [tech, setTech] = useState<string | undefined>();
  const [count, setCount] = useState(10);

  const current = TYPES.find((t) => t.key === type)!;

  const begin = async () => {
    await start({ type, technology: tech, total_questions: count });
    navigation.navigate('InterviewSession');
  };

  return (
    <ScrollView className="flex-1 bg-white p-6">
      <Text className="text-2xl font-bold text-slate-900 mb-4">Start an interview</Text>
      <Text className="text-slate-500 mb-2">Type</Text>
      <View className="flex-row flex-wrap gap-2 mb-4">
        {TYPES.map((t) => (
          <Pressable key={t.key} onPress={() => { setType(t.key); setTech(undefined); }}
            className={`px-4 py-2 rounded-xl ${type === t.key ? 'bg-brand-600' : 'bg-slate-100'}`}>
            <Text className={type === t.key ? 'text-white' : 'text-slate-700'}>{t.label}</Text>
          </Pressable>
        ))}
      </View>

      {current.techs.length > 0 && (
        <>
          <Text className="text-slate-500 mb-2">Technology</Text>
          <View className="flex-row flex-wrap gap-2 mb-4">
            {current.techs.map((t) => (
              <Pressable key={t} onPress={() => setTech(t)}
                className={`px-3 py-2 rounded-lg ${tech === t ? 'bg-brand-600' : 'bg-slate-100'}`}>
                <Text className={tech === t ? 'text-white' : 'text-slate-700'}>{t}</Text>
              </Pressable>
            ))}
          </View>
        </>
      )}

      <Text className="text-slate-500 mb-2">Questions: {count}</Text>
      <TextInput value={String(count)} keyboardType="numeric" onChangeText={(v) => setCount(Number(v) || 5)}
        className="border border-slate-200 rounded-xl px-4 py-3 mb-6 text-slate-900" />

      <Pressable onPress={begin} disabled={startLoading}
        className="bg-brand-600 rounded-xl py-4 items-center">
        {startLoading ? <ActivityIndicator color="#fff" /> : <Text className="text-white font-semibold">Begin</Text>}
      </Pressable>
    </ScrollView>
  );
};