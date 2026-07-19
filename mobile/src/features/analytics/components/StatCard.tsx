import React from 'react';
import { View, Text } from 'react-native';

interface StatCardProps {
  label: string;
  value: string | number | null;
  hint?: string;
  tone?: 'brand' | 'neutral';
}

/** Headline number tile — for "Average score" / "Total interviews". Not a chart. */
export const StatCard = ({ label, value, hint, tone = 'neutral' }: StatCardProps) => (
  <View className={`flex-1 rounded-2xl p-4 border ${tone === 'brand' ? 'bg-brand-50 border-brand-100' : 'bg-white border-slate-200'}`}>
    <Text className="text-slate-500 text-sm">{label}</Text>
    <Text className="text-3xl font-bold text-slate-900 mt-1">{value ?? '–'}</Text>
    {hint ? <Text className="text-slate-400 text-xs mt-1">{hint}</Text> : null}
  </View>
);