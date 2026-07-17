import React from 'react';
import { Pressable, Text, ActivityIndicator } from 'react-native';

interface ButtonProps {
  title: string;
  onPress: () => void;
  loading?: boolean;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export const Button = ({ title, onPress, loading, variant = 'primary', disabled }: ButtonProps) => (
  <Pressable
    onPress={onPress}
    disabled={disabled || loading}
    className={`rounded-xl py-4 items-center ${variant === 'primary' ? 'bg-brand-600' : 'bg-slate-200'} ${disabled ? 'opacity-50' : ''}`}
  >
    {loading ? <ActivityIndicator color="#fff" /> : (
      <Text className={variant === 'primary' ? 'text-white font-semibold' : 'text-slate-800 font-semibold'}>{title}</Text>
    )}
  </Pressable>
);