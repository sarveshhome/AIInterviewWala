import { useMutation } from '@tanstack/react-query';
import { resumeApi } from '@core/api/endpoints';

/** Upload a resume file and get the ATS analysis. */
export const useResumeUpload = () =>
  useMutation({
    mutationFn: async (fileUri: string) => {
      const formData = new FormData();
      formData.append('file', { uri: fileUri, name: 'resume.pdf', type: 'application/pdf' } as any);
      return resumeApi.upload(formData);
    },
  });