import React from 'react';
import { View, Text, ScrollView, ActivityIndicator } from 'react-native';
import { VictoryBar, VictoryChart, VictoryTheme, VictoryPie } from 'victory-native';
import { useDashboard } from '@features/analytics/hooks/useDashboard';

export const DashboardScreen = () => {
  const { data, isLoading } = useDashboard();

  if (isLoading) return <View className="flex-1 items-center justify-center"><ActivityIndicator /></View>;

  const techData = Object.entries(data?.tech_performance ?? {}).map(([tech, score]) => ({ tech, score }));
  const pieData = [
    { x: 'Strong', y: data?.strong_areas?.length ?? 0 },
    { x: 'Weak', y: data?.weak_areas?.length ?? 0 },
  ];

  return (
    <ScrollView className="flex-1 bg-white p-6">
      <Text className="text-2xl font-bold text-slate-900 mb-1">Dashboard</Text>
      <Text className="text-slate-500 mb-4">Interviews: {data?.total_interviews ?? 0} · Avg {data?.average_score ?? '–'}</Text>

      <View className="bg-slate-50 rounded-2xl p-4 mb-4">
        <Text className="font-semibold text-slate-900 mb-2">Technology-wise performance</Text>
        {techData.length ? (
          <VictoryChart theme={VictoryTheme.material} height={220}>
            <VictoryBar data={techData} x="tech" y="score" />
          </VictoryChart>
        ) : <Text className="text-slate-500">No data yet.</Text>}
      </View>

      <View className="flex-row gap-4 mb-4">
        <View className="flex-1 bg-green-50 rounded-2xl p-4">
          <Text className="font-semibold text-green-700">Strong areas</Text>
          <Text className="text-slate-700">{data?.strong_areas?.join(', ') || '—'}</Text>
        </View>
        <View className="flex-1 bg-red-50 rounded-2xl p-4">
          <Text className="font-semibold text-red-700">Weak areas</Text>
          <Text className="text-slate-700">{data?.weak_areas?.join(', ') || '—'}</Text>
        </View>
      </View>

      <Text className="font-semibold text-slate-900 mb-2">Recent interviews</Text>
      {(data?.history ?? []).map((h) => (
        <View key={h.id} className="flex-row justify-between py-2 border-b border-slate-100">
          <Text className="text-slate-700">{h.type}{h.technology ? ` · ${h.technology}` : ''}</Text>
          <Text className="text-slate-900 font-semibold">{h.score ?? '–'}</Text>
        </View>
      ))}
    </ScrollView>
  );
};