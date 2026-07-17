import React from 'react';
import { View, Text, TextInput, Pressable, ActivityIndicator } from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import { useAuth } from '@features/auth/hooks/useAuth';

interface FormValues { email: string; password: string; full_name: string; }

export const RegisterScreen = ({ navigation }: any) => {
  const { register, loading, error } = useAuth();
  const { control, handleSubmit, formState: { errors } } = useForm<FormValues>();

  const onSubmit = (data: FormValues) => register(data.email, data.password, data.full_name);

  return (
    <View className="flex-1 bg-white p-6 justify-center">
      <Text className="text-2xl font-bold text-slate-900 mb-6">Create account</Text>

      <Controller control={control} name="full_name" rules={{ required: 'Required' }}
        render={({ field }) => (
          <TextInput placeholder="Full name" className="border border-slate-200 rounded-xl px-4 py-3 mb-2 text-slate-900"
            value={field.value} onChangeText={field.onChange} />
        )} />
      <Controller control={control} name="email" rules={{ required: 'Required' }}
        render={({ field }) => (
          <TextInput placeholder="Email" autoCapitalize="none" keyboardType="email-address"
            className="border border-slate-200 rounded-xl px-4 py-3 mb-2 text-slate-900"
            value={field.value} onChangeText={field.onChange} />
        )} />
      <Controller control={control} name="password" rules={{ required: 'Required', minLength: 6 }}
        render={({ field }) => (
          <TextInput placeholder="Password (min 6)" secureTextEntry
            className="border border-slate-200 rounded-xl px-4 py-3 mb-2 text-slate-900"
            value={field.value} onChangeText={field.onChange} />
        )} />
      {errors.password && <Text className="text-red-500 mb-2">Min 6 characters</Text>}
      {error && <Text className="text-red-500 mb-2">{error}</Text>}

      <Pressable onPress={handleSubmit(onSubmit)} disabled={loading}
        className="bg-brand-600 rounded-xl py-4 items-center mt-2">
        {loading ? <ActivityIndicator color="#fff" /> : <Text className="text-white font-semibold">Sign up</Text>}
      </Pressable>

      <Pressable onPress={() => navigation.navigate('Login')} className="mt-4 items-center">
        <Text className="text-brand-600">Already have an account? Log in</Text>
      </Pressable>
    </View>
  );
};