import React from 'react';
import Animated, { useAnimatedStyle, interpolateColor } from 'react-native-reanimated';
import { useTabIconAnimation, TAB_BRAND, TAB_BRAND_CLEAR, TAB_MUTED } from './useTabIconAnimation';

interface Props { focused: boolean; size?: number; }

/** 2×2 grid of rounded squares — outline (muted) morphs to filled (brand) on focus. */
export const DashboardTabIcon = ({ focused, size = 26 }: Props) => {
  const { focus, containerStyle } = useTabIconAnimation(focused);
  const sq = size * 0.4;
  const gap = size * 0.1;
  const r = size * 0.1;

  // Reused across all four squares — same fill/border morph.
  const squareStyle = useAnimatedStyle(() => ({
    backgroundColor: interpolateColor(focus.value, [0, 1], [TAB_BRAND_CLEAR, TAB_BRAND]),
    borderColor: interpolateColor(focus.value, [0, 1], [TAB_MUTED, TAB_BRAND]),
  }));

  return (
    <Animated.View
      style={[{ width: size, height: size, alignItems: 'center', justifyContent: 'center' }, containerStyle]}
    >
      <Animated.View style={{ flexDirection: 'row', flexWrap: 'wrap', width: 2 * sq + gap, gap, justifyContent: 'center' }}>
        {[0, 1, 2, 3].map((i) => (
          <Animated.View key={i} style={[squareStyle, { width: sq, height: sq, borderRadius: r, borderWidth: 1.5 }]} />
        ))}
      </Animated.View>
    </Animated.View>
  );
};