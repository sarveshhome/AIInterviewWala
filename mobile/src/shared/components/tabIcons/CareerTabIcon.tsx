import React from 'react';
import Animated, { useAnimatedStyle, interpolateColor } from 'react-native-reanimated';
import { useTabIconAnimation, TAB_BRAND, TAB_BRAND_CLEAR, TAB_MUTED, TAB_WHITE } from './useTabIconAnimation';

interface Props { focused: boolean; size?: number; }

/** Compass / route marker — a ring that fills brand on focus with a needle that
 *  snaps to white when active. Signals "guidance / direction" for the Career tab. */
export const CareerTabIcon = ({ focused, size = 26 }: Props) => {
  const { focus, containerStyle } = useTabIconAnimation(focused);

  const ringStyle = useAnimatedStyle(() => ({
    backgroundColor: interpolateColor(focus.value, [0, 1], [TAB_BRAND_CLEAR, TAB_BRAND]),
    borderColor: interpolateColor(focus.value, [0, 1], [TAB_MUTED, TAB_BRAND]),
  }));

  const needleStyle = useAnimatedStyle(() => ({
    backgroundColor: interpolateColor(focus.value, [0, 1], [TAB_MUTED, TAB_WHITE]),
    // needle rotates from a resting diagonal to pointing up-right when active
    transform: [{ rotate: `${-35 + focus.value * 35}deg` }],
  }));

  return (
    <Animated.View
      style={[{ width: size, height: size, alignItems: 'center', justifyContent: 'center' }, containerStyle]}
    >
      <Animated.View
        style={[
          ringStyle,
          {
            width: size * 0.72, height: size * 0.72, borderRadius: size * 0.36, borderWidth: 1.5,
            alignItems: 'center', justifyContent: 'center',
          },
        ]}
      >
        {/* Needle — a slim diamond anchored at the compass center. */}
        <Animated.View
          style={[
            needleStyle,
            {
              width: size * 0.08, height: size * 0.4, borderRadius: size * 0.04,
              position: 'absolute',
            },
          ]}
        />
        {/* Center pivot dot. */}
        <Animated.View
          style={[
            needleStyle,
            { width: size * 0.12, height: size * 0.12, borderRadius: size * 0.06 },
          ]}
        />
      </Animated.View>
    </Animated.View>
  );
};