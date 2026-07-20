import React from 'react';
import Animated, { useAnimatedStyle, interpolateColor } from 'react-native-reanimated';
import { useTabIconAnimation, TAB_BRAND, TAB_BRAND_CLEAR, TAB_MUTED, TAB_WHITE } from './useTabIconAnimation';

interface Props { focused: boolean; size?: number; }

/** Chat bubble with a tail + three dots. On focus the bubble fills brand and the dots pop white. */
export const InterviewTabIcon = ({ focused, size = 26 }: Props) => {
  const { focus, containerStyle } = useTabIconAnimation(focused);

  const bubbleStyle = useAnimatedStyle(() => ({
    backgroundColor: interpolateColor(focus.value, [0, 1], [TAB_BRAND_CLEAR, TAB_BRAND]),
    borderColor: interpolateColor(focus.value, [0, 1], [TAB_MUTED, TAB_BRAND]),
  }));

  const dotStyle = useAnimatedStyle(() => ({
    backgroundColor: interpolateColor(focus.value, [0, 1], [TAB_MUTED, TAB_WHITE]),
    transform: [{ scale: 0.6 + focus.value * 0.4 }], // dots pop in when active
  }));

  const dot = size * 0.1;

  return (
    <Animated.View
      style={[{ width: size, height: size, alignItems: 'center', justifyContent: 'center' }, containerStyle]}
    >
      <Animated.View
        style={[
          bubbleStyle,
          {
            width: size * 0.7, height: size * 0.52, borderRadius: size * 0.16, borderWidth: 1.5,
            flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: size * 0.1,
          },
        ]}
      >
        {[0, 1, 2].map((i) => (
          <Animated.View key={i} style={[dotStyle, { width: dot, height: dot, borderRadius: dot / 2 }]} />
        ))}
      </Animated.View>
      {/* Tail — a rotated square with only the lower-right edges, suggesting a speech bubble. */}
      <Animated.View
        style={[
          bubbleStyle,
          {
            position: 'absolute', bottom: size * 0.16, left: size * 0.27,
            width: size * 0.16, height: size * 0.16, borderRadius: size * 0.03,
            transform: [{ rotate: '45deg' }],
            borderRightWidth: 1.5, borderBottomWidth: 1.5,
          },
        ]}
      />
    </Animated.View>
  );
};