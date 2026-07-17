import React from 'react';
import { View, Text, TextInput, Pressable, ActivityIndicator } from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import { useAuth } from '@features/auth/hooks/useAuth';

interface FormValues { email: string; password: string; }

export const LoginScreen = ({ navigation }: any) => {
  const { login, loading, error } = useAuth();
  const { control, handleSubmit, formState: { errors } } = useForm<FormValues>({
    defaultValues: { email: '', password: '' },
  });

  const onSubmit = (data: FormValues) => login(data.email, data.password);

  return (
    <View className="flex-1 bg-white p-6 justify-center">
      <Text className="text-2xl font-bold text-slate-900 mb-1">Welcome back</Text>
      <Text className="text-slate-500 mb-6">Make an impression with AI interview prep.</Text>

      <Controller control={control} name="email" rules={{ required: 'Email is required' }}
        render={({ field: { onChange, value } }) => (
          <TextInput placeholder="Email" value={value} onChangeText={onChange}
            keyboardType="email-address" autoCapitalize="none"
            className="border border-slate-200 rounded-xl px-4 py-3 mb-2 text-slate-900" />
        )} />
      {errors.email && <Text className="text-red-500 mb-2">{errors.email.message}</Text>}

      <Controller control={control} name="password" rules={{ required: 'Password is required', minLength: { value: 6, message: 'Min 6 chars' } }}
        render={({ field: { onChange, value } }) => (
          <TextInput placeholder="Password" value={value} onChangeText={onChange} secureTextEntry
            className="border border-slate-200 rounded-xl px-4 py-3 mb-2 text-slate-900" />
        )} />
      {errors.password && <Text className="text-red-500 mb-2">{errors.password.message}</Text>}

      {error && <Text className="text-red-500 mb-2">{error}</Text>}

      <Pressable onPress={handleSubmit(onSubmit)} disabled={loading}
        className="bg-brand-600 rounded-xl py-4 items-center mt-2">
        {loading ? <ActivityIndicator color="#fff" /> : <Text className="text-white font-semibold">Log in</Text>}
      </Pressable>

      <Pressable onPress={() => navigation.navigate('Register')} className="mt-4 items-center">
        <Text className="text-brand-600">Don't have an account? Sign up</Text>
      </Pressable>
    </View>
  );
};