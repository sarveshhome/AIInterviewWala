import React from 'react';
import Animated, { useAnimatedStyle, interpolateColor } from 'react-native-reanimated';
import { useTabIconAnimation, TAB_BRAND, TAB_BRAND_CLEAR, TAB_MUTED, TAB_WHITE } from './useTabIconAnimation';

interface Props { focused: boolean; size?: number; }

/** Document with three text lines. On focus the page fills brand and the lines draw in (grow) white. */
export const ResumeTabIcon = ({ focused, size = 26 }: Props) => {
  const { focus, containerStyle } = useTabIconAnimation(focused);

  const docStyle = useAnimatedStyle(() => ({
    backgroundColor: interpolateColor(focus.value, [0, 1], [TAB_BRAND_CLEAR, TAB_BRAND]),
    borderColor: interpolateColor(focus.value, [0, 1], [TAB_MUTED, TAB_BRAND]),
  }));

  const lineStyle = useAnimatedStyle(() => ({
    backgroundColor: interpolateColor(focus.value, [0, 1], [TAB_MUTED, TAB_WHITE]),
    width: size * 0.12 + focus.value * size * 0.24, // lines "draw in" as the tab activates
  }));

  return (
    <Animated.View
      style={[{ width: size, height: size, alignItems: 'center', justifyContent: 'center' }, containerStyle]}
    >
      <Animated.View
        style={[
          docStyle,
          {
            width: size * 0.56, height: size * 0.72, borderRadius: size * 0.1, borderWidth: 1.5,
            padding: size * 0.12, justifyContent: 'space-between',
          },
        ]}
      >
        {[0, 1, 2].map((i) => (
          <Animated.View key={i} style={[lineStyle, { height: size * 0.06, borderRadius: size * 0.03 }]} />
        ))}
      </Animated.View>
    </Animated.View>
  );
};