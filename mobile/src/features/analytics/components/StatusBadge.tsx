import React from 'react';
import { View, Text } from 'react-native';
import type { InterviewStatus } from '@features/analytics/models/analytics';

const STATUS_META: Record<InterviewStatus, { label: string; cls: string }> = {
  pending: { label: 'Pending', cls: 'bg-slate-200 text-slate-700' },
  in_progress: { label: 'In progress', cls: 'bg-amber-100 text-amber-800' },
  completed: { label: 'Completed', cls: 'bg-green-100 text-green-800' },
  aborted: { label: 'Aborted', cls: 'bg-red-100 text-red-800' },
};

interface StatusBadgeProps {
  status: InterviewStatus;
}

/** Maps InterviewStatus to a status-colored badge — color + label, never color alone. */
export const StatusBadge = ({ status }: StatusBadgeProps) => {
  const meta = STATUS_META[status] ?? STATUS_META.pending;
  return (
    <View className={`self-start rounded-full px-2.5 py-0.5 ${meta.cls}`}>
      <Text className="text-xs font-medium">{meta.label}</Text>
    </View>
  );
};