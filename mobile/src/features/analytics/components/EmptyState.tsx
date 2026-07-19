import React from 'react';
import { View, Text } from 'react-native';

interface EmptyStateProps {
  message: string;
  hint?: string;
}

/** Centered placeholder for empty sections / screens. */
export const EmptyState = ({ message, hint }: EmptyStateProps) => (
  <View className="items-center justify-center py-8">
    <Text className="text-slate-500 text-center">{message}</Text>
    {hint ? <Text className="text-slate-400 text-xs text-center mt-1">{hint}</Text> : null}
  </View>
);