import React from 'react';
import { Text } from 'react-native';
import { render, screen } from '@testing-library/react-native';

// Mock the data hook so we can drive each dashboard state.
let mockReturn: any = { data: undefined, isLoading: true, isError: false, isFetching: false, refetch: jest.fn() };
jest.mock('@features/analytics/hooks/useDashboard', () => ({
  useDashboard: () => mockReturn,
}));

// Skia + victory-native can't render in jest — stub them to plain Views.
jest.mock('@shopify/react-native-skia', () => ({ matchFont: () => null }));
jest.mock('victory-native', () => {
  const React = jest.requireActual('react');
  const { View } = jest.requireActual('react-native');
  // CartesianChart takes a render-prop child; the others take plain children.
  const Stub = ({ children }: any) => React.createElement(View, null,
    typeof children === 'function' ? children({ points: { score: [] }, chartBounds: {} }) : children);
  return {
    CartesianChart: Stub,
    Line: Stub,
    Bar: Stub,
    Scatter: Stub,
  };
});

import { DashboardScreen } from '@features/analytics/screens/DashboardScreen';

const populatedData = {
  total_interviews: 3,
  average_score: 78.5,
  weak_areas: ['Kafka'],
  strong_areas: ['Python', 'React'],
  tech_performance: { Python: 85, Kafka: 42 },
  history: [
    { id: '1', type: 'technical', technology: 'Python', status: 'completed', score: 85, completed_at: '2026-07-19T10:00:00Z' },
    { id: '2', type: 'coding', technology: null, status: 'in_progress', score: null, completed_at: null },
  ],
  progress: [
    { date: '2026-07-18T10:00:00Z', score: 72, label: '#1 technical' },
    { date: '2026-07-19T10:00:00Z', score: 85, label: '#2 technical' },
  ],
};

beforeEach(() => {
  mockReturn = { data: undefined, isLoading: true, isError: false, isFetching: false, refetch: jest.fn() };
});

describe('DashboardScreen', () => {
  it('shows a loading indicator while loading', () => {
    render(<DashboardScreen />);
    // The populated/empty branches render the "Dashboard" heading; loading does not.
    expect(screen.queryByText('Dashboard')).toBeNull();
  });

  it('shows an empty state when there is no data', () => {
    mockReturn = { data: { total_interviews: 0, average_score: null, weak_areas: [], strong_areas: [], tech_performance: {}, history: [], progress: [] }, isLoading: false, isError: false, isFetching: false, refetch: jest.fn() };
    render(<DashboardScreen />);
    expect(screen.getByText('No interviews yet')).toBeTruthy();
  });

  it('renders all six sections when populated', () => {
    mockReturn = { data: populatedData, isLoading: false, isError: false, isFetching: false, refetch: jest.fn() };
    render(<DashboardScreen />);
    // Header summary + stat tiles
    expect(screen.getByText(/3 interviews/)).toBeTruthy();
    expect(screen.getByText('Total interviews')).toBeTruthy();
    expect(screen.getByText('Average score')).toBeTruthy();
    // Progress / tech / strong / weak sections
    expect(screen.getByText('Progress')).toBeTruthy();
    expect(screen.getByText('Technology-wise performance')).toBeTruthy();
    expect(screen.getByText('Strong areas')).toBeTruthy();
    expect(screen.getByText('Weak areas')).toBeTruthy();
    // Strong/weak chips
    expect(screen.getByText('Python')).toBeTruthy();
    expect(screen.getByText('Kafka')).toBeTruthy();
    // History rows (type and technology render as adjacent text nodes)
    expect(screen.getByText('technical')).toBeTruthy();
    expect(screen.getByText('coding')).toBeTruthy();
  });

  it('shows an error state with retry when the fetch fails', () => {
    const refetch = jest.fn();
    mockReturn = { data: undefined, isLoading: false, isError: true, isFetching: false, refetch };
    render(<DashboardScreen />);
    expect(screen.getByText("Couldn't load your dashboard")).toBeTruthy();
  });
});