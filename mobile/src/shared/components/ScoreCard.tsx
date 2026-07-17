import React from 'react';
import { View, Text } from 'react-native';

interface Props { label: string; score: number | null; }

export const ScoreCard = ({ label, score }: Props) => (
  <View className="flex-1 bg-white rounded-2xl p-4 border border-slate-200">
    <Text className="text-slate-500 text-sm">{label}</Text>
    <Text className="text-3xl font-bold text-slate-900">{score ?? '–'}</Text>
  </View>
);