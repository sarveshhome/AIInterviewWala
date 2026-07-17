import React, { useState } from 'react';
import { View, Text, Pressable, ActivityIndicator, ScrollView } from 'react-native';
import DocumentPicker from 'react-native-document-picker'; // optional dependency
import { useResumeUpload } from '@features/resume/hooks/useResume';

export const ResumeUploadScreen = () => {
  const [result, setResult] = useState<any>(null);
  const upload = useResumeUpload();

  const pick = async () => {
    try {
      const [doc] = await DocumentPicker.pick({ type: [DocumentPicker.types.pdf, DocumentPicker.types.plainText] });
      const res = await upload.mutateAsync(doc.uri);
      setResult(res);
    } catch {
      /* user cancelled */
    }
  };

  return (
    <ScrollView className="flex-1 bg-white p-6">
      <Text className="text-2xl font-bold text-slate-900 mb-2">Resume analysis</Text>
      <Text className="text-slate-500 mb-6">Upload your resume for an ATS score & skill gaps.</Text>

      <Pressable onPress={pick} disabled={upload.isPending}
        className="bg-brand-600 rounded-xl py-4 items-center mb-6">
        {upload.isPending ? <ActivityIndicator color="#fff" /> : <Text className="text-white font-semibold">Choose file</Text>}
      </Pressable>

      {result && (
        <View className="bg-slate-50 rounded-2xl p-4 border border-slate-200">
          <Text className="text-2xl font-bold text-green-600 mb-2">ATS {result.ats_score ?? '–'}</Text>
          <Text className="font-semibold text-slate-900 mt-2">Strong areas</Text>
          <Text className="text-slate-700">{result.strong_areas.join(', ') || '—'}</Text>
          <Text className="font-semibold text-slate-900 mt-2">Missing skills</Text>
          <Text className="text-slate-700">{result.missing_skills.join(', ') || '—'}</Text>
          <Text className="font-semibold text-slate-900 mt-2">Improvements</Text>
          {result.recommended_improvements.map((r: string) => (
            <Text key={r} className="text-slate-700">• {r}</Text>
          ))}
        </View>
      )}
    </ScrollView>
  );
};