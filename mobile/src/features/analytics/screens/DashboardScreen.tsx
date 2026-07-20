import React, { useMemo, useCallback } from 'react';
import { View, Text, ScrollView, ActivityIndicator, RefreshControl, Pressable, StyleSheet } from 'react-native';
import { CartesianChart, Line, Bar, Scatter } from 'victory-native';
import { matchFont } from '@shopify/react-native-skia';

import { useDashboard } from '@features/analytics/hooks/useDashboard';
import type { AnalyticsResponse, InterviewHistoryItem, ProgressPoint } from '@features/analytics/models/analytics';
import { StatCard, SectionCard, Tag, StatusBadge, EmptyState } from '@features/analytics/components';

const BRAND = '#1e66f5'; // theme.colors.primary / brand-600
const AXIS_INK = '#94a3b8'; // slate-400 — recessive axes
const GRID_INK = '#e2e8f0'; // slate-200

/** Short, locale-independent date label for the progress x-axis. */
const shortDate = (iso: string): string => {
  if (!iso) return '';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '';
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return `${mm}/${dd}`;
};

const formatDate = (iso?: string | null): string => {
  if (!iso) return '';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '';
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
};

/** System font for Skia axis labels (no bundled .ttf required). */
const useAxisFont = (size = 10) => useMemo(() => {
  try { return matchFont({ fontFamily: 'sans-serif', fontSize: size, fontWeight: 'normal' }); }
  catch { return null; }
}, [size]);

export const DashboardScreen = () => {
  const { data, isLoading, isError, refetch, isFetching } = useDashboard();
  const font = useAxisFont(10);

  const onRefresh = useCallback(() => { refetch(); }, [refetch]);

  // All hooks must run before any early return — keep memoized derived data up here
  // so the hook order is identical on loading vs populated renders.
  const d: AnalyticsResponse = useMemo(() => data ?? {
    total_interviews: 0, average_score: null, weak_areas: [], strong_areas: [],
    tech_performance: {}, history: [], progress: [],
  }, [data]);

  // Plot progress as score per completed interview, in chronological order.
  const progressData = useMemo(
    () => d.progress.map((p: ProgressPoint, i: number) => ({ x: i + 1, score: p.score, date: p.date })),
    [d.progress],
  );
  const techData = useMemo(
    () => Object.entries(d.tech_performance).map(([tech, score]) => ({ tech, score })),
    [d.tech_performance],
  );

  const axisOptions = {
    font,
    lineColor: GRID_INK,
    labelColor: AXIS_INK,
    tickCount: 5 as const,
  };

  if (isLoading) {
    return (
      <View className="flex-1 items-center justify-center bg-white">
        <ActivityIndicator />
      </View>
    );
  }

  if (isError && !data) {
    return (
      <View className="flex-1 items-center justify-center bg-white p-6">
        <Text className="text-slate-700 font-semibold mb-1">Couldn't load your dashboard</Text>
        <Text className="text-slate-500 text-center mb-4">Check your connection and try again.</Text>
        <Pressable className="bg-brand-600 rounded-xl px-5 py-3" onPress={() => refetch()}>
          <Text className="text-white font-semibold">Retry</Text>
        </Pressable>
      </View>
    );
  }

  const isEmpty = d.total_interviews === 0 && d.history.length === 0;

  return (
    <ScrollView
      className="flex-1 bg-white"
      contentContainerClassName="p-6"
      refreshControl={
        <RefreshControl refreshing={isFetching && !isLoading} onRefresh={onRefresh} tintColor={BRAND} />
      }
    >
      <Text className="text-2xl font-bold text-slate-900 mb-1">Dashboard</Text>
      <Text className="text-slate-500 mb-4">
        {d.total_interviews} interview{d.total_interviews === 1 ? '' : 's'} · Avg {d.average_score ?? '–'}
      </Text>

      {isEmpty ? (
        <EmptyState
          message="No interviews yet"
          hint="Start an interview to see your score history and tech-wise performance here."
        />
      ) : (
        <>
          {/* Headline stat tiles */}
          <View className="flex-row gap-3 mb-4">
            <StatCard label="Total interviews" value={d.total_interviews} />
            <StatCard label="Average score" value={d.average_score} hint="out of 100" tone="brand" />
          </View>

          {/* Progress graph — score over time, single series, single hue */}
          <SectionCard title="Progress" subtitle="Score per completed interview (chronological)">
            {progressData.length >= 2 ? (
              <View style={styles.chart}>
                <CartesianChart
                  data={progressData}
                  xKey="x"
                  yKeys={['score']}
                  domain={{ y: [0, 100] }}
                  axisOptions={{
                    ...axisOptions,
                    tickCount: { x: Math.min(progressData.length, 6), y: 5 } as const,
                    formatXLabel: (label: number | string) => {
                      const i = Math.round(Number(label)) - 1;
                      return shortDate(progressData[i]?.date ?? '') || String(Math.round(Number(label)));
                    },
                    formatYLabel: (v: number | string) => `${Math.round(Number(v))}`,
                  }}
                >
                  {({ points }) => (
                    <>
                      <Line points={points.score} color={BRAND} strokeWidth={2} curveType="natural" />
                      <Scatter points={points.score} radius={4} color={BRAND} />
                    </>
                  )}
                </CartesianChart>
              </View>
            ) : (
              <EmptyState message="Not enough data yet" hint="Complete at least two interviews to see your progress." />
            )}
          </SectionCard>

          {/* Technology-wise performance — categorical magnitude, single hue (color never encodes rank) */}
          <SectionCard title="Technology-wise performance" subtitle="Average score per technology">
            {techData.length ? (
              <View style={{ height: Math.max(220, techData.length * 44) }}>
                <CartesianChart
                  data={techData}
                  xKey="tech"
                  yKeys={['score']}
                  domain={{ y: [0, 100] }}
                  axisOptions={{
                    ...axisOptions,
                    formatYLabel: (v: number | string) => `${Math.round(Number(v))}`,
                  }}
                >
                  {({ points, chartBounds }) => (
                    <Bar
                      points={points.score}
                      chartBounds={chartBounds}
                      color={BRAND}
                      barWidth={18}
                      roundedCorners={{ topLeft: 4, topRight: 4 }}
                    />
                  )}
                </CartesianChart>
              </View>
            ) : (
              <EmptyState message="No technology data yet" />
            )}
          </SectionCard>

          {/* Strong / weak areas — polarity chips, not a chart */}
          <View className="flex-row gap-3 mb-4">
            <View className="flex-1">
              <SectionCard title="Strong areas" subtitle="Avg ≥ 70">
                {d.strong_areas.length ? (
                  <View className="flex-row flex-wrap">
                    {d.strong_areas.map((a) => <Tag key={a} label={a} tone="success" />)}
                  </View>
                ) : <Text className="text-slate-500">—</Text>}
              </SectionCard>
            </View>
            <View className="flex-1">
              <SectionCard title="Weak areas" subtitle="Avg < 50">
                {d.weak_areas.length ? (
                  <View className="flex-row flex-wrap">
                    {d.weak_areas.map((a) => <Tag key={a} label={a} tone="danger" />)}
                  </View>
                ) : <Text className="text-slate-500">—</Text>}
              </SectionCard>
            </View>
          </View>

          {/* Interview history */}
          <Text className="font-semibold text-slate-900 mb-2">Recent interviews</Text>
          {d.history.length ? (
            <View className="rounded-2xl border border-slate-200 overflow-hidden">
              {d.history.map((h: InterviewHistoryItem, idx: number) => (
                <View
                  key={h.id}
                  className={`flex-row items-center justify-between px-4 py-3 ${idx > 0 ? 'border-t border-slate-100' : ''}`}
                >
                  <View className="flex-1 mr-3">
                    <View className="flex-row items-center mb-1">
                      <Text className="text-slate-900 font-medium capitalize">{h.type}</Text>
                      {h.technology ? <Text className="text-slate-500"> · {h.technology}</Text> : null}
                    </View>
                    <View className="flex-row items-center">
                      <StatusBadge status={h.status} />
                      {h.completed_at ? (
                        <Text className="text-slate-400 text-xs ml-2">{formatDate(h.completed_at)}</Text>
                      ) : null}
                    </View>
                  </View>
                  <Text className="text-slate-900 font-bold text-lg">{h.score ?? '–'}</Text>
                </View>
              ))}
            </View>
          ) : (
            <EmptyState message="No interviews yet" />
          )}
        </>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({ chart: { height: 220 } });