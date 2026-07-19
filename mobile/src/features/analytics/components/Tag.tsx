import React from 'react';
import { View, Text } from 'react-native';

type Tone = 'success' | 'danger' | 'neutral';

const TONE_CLS: Record<Tone, string> = {
  success: 'bg-green-100 text-green-800',
  danger: 'bg-red-100 text-red-800',
  neutral: 'bg-slate-200 text-slate-700',
};

interface TagProps {
  label: string;
  tone?: Tone;
}

/** Pill chip for strong/weak areas (polarity) — not a chart. */
export const Tag = ({ label, tone = 'neutral' }: TagProps) => (
  <View className={`self-start rounded-full px-3 py-1 mr-2 mb-2 ${TONE_CLS[tone]}`}>
    <Text className="text-xs font-medium">{label}</Text>
  </View>
);