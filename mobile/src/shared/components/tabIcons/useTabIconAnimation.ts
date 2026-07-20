import { useEffect } from 'react';
import { useSharedValue, useAnimatedStyle, withSpring } from 'react-native-reanimated';

/** Palette for tab icons — matches theme.colors (brand-600 / slate-400). */
export const TAB_BRAND = '#1e66f5';
export const TAB_MUTED = '#94a3b8';
export const TAB_WHITE = '#ffffff';
/** Transparent brand (rgba with 0 alpha) so interpolateColor can fade fill in/out. */
export const TAB_BRAND_CLEAR = 'rgba(30,102,245,0)';

const SPRING = { stiffness: 320, damping: 18, mass: 0.6 };

/**
 * Drives a tab icon's focus animation. Returns a `focus` shared value (0→1)
 * and the container style (spring scale + lift on focus). Child shapes read
 * `focus.value` in their own `useAnimatedStyle` worklets to morph color/size.
 */
export const useTabIconAnimation = (focused: boolean) => {
  const focus = useSharedValue(focused ? 1 : 0);

  useEffect(() => {
    focus.value = withSpring(focused ? 1 : 0, SPRING);
  }, [focused, focus]);

  const containerStyle = useAnimatedStyle(() => ({
    transform: [
      { scale: 0.92 + focus.value * 0.16 }, // 0.92 (resting) → 1.08 (active)
      { translateY: -2 * focus.value }, // small lift when selected
    ],
  }));

  return { focus, containerStyle };
};