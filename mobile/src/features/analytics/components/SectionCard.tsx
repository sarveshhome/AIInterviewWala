import React from 'react';
import { View, Text } from 'react-native';

interface SectionCardProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
}

/** Titled surface wrapper used to group each dashboard section. */
export const SectionCard = ({ title, subtitle, children }: SectionCardProps) => (
  <View className="bg-slate-50 rounded-2xl p-4 mb-4">
    <Text className="font-semibold text-slate-900">{title}</Text>
    {subtitle ? <Text className="text-slate-500 text-xs mb-2">{subtitle}</Text> : null}
    <View className="mt-2">{children}</View>
  </View>
);