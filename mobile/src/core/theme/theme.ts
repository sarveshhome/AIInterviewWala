/** Design tokens. NativeWind maps brand-* from tailwind.config.js. */
export const theme = {
  colors: {
    primary: '#1e66f5',
    background: '#ffffff',
    surface: '#f6f7fb',
    text: '#0f172a',
    muted: '#64748b',
    success: '#16a34a',
    warning: '#d97706',
    danger: '#dc2626',
  },
  spacing: { sm: 8, md: 16, lg: 24, xl: 32 },
  radius: { sm: 8, md: 12, lg: 16, xl: 24 },
} as const;

export type Theme = typeof theme;