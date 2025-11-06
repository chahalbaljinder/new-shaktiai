// React Query hooks for API calls
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient, type ChatRequest, type Wish, type ShareWishRequest } from './client';
import { toast } from 'sonner';

// Agent hooks
export const useAgents = () => {
  return useQuery({
    queryKey: ['agents'],
    queryFn: () => apiClient.getAgents(),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
};

export const useChatWithAgent = () => {
  return useMutation({
    mutationFn: (request: ChatRequest) => apiClient.chatWithAgent(request),
    onError: (error: Error) => {
      toast.error(`Failed to chat with agent: ${error.message}`);
    },
  });
};

// Wishes Vault hooks
export const useWishes = () => {
  return useQuery({
    queryKey: ['wishes'],
    queryFn: () => apiClient.getWishes(),
    staleTime: 1000 * 60 * 2, // 2 minutes
  });
};

export const useCreateWish = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (wish: Omit<Wish, 'id' | 'created_at' | 'updated_at'>) => 
      apiClient.createWish(wish),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['wishes'] });
      toast.success(data.message || 'Wish created successfully');
    },
    onError: (error: Error) => {
      toast.error(`Failed to create wish: ${error.message}`);
    },
  });
};

export const useUpdateWish = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ wishId, updates }: { wishId: number; updates: Partial<Wish> }) => 
      apiClient.updateWish(wishId, updates),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['wishes'] });
      toast.success(data.message || 'Wish updated successfully');
    },
    onError: (error: Error) => {
      toast.error(`Failed to update wish: ${error.message}`);
    },
  });
};

export const useDeleteWish = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (wishId: number) => apiClient.deleteWish(wishId),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['wishes'] });
      toast.success(data.message || 'Wish deleted successfully');
    },
    onError: (error: Error) => {
      toast.error(`Failed to delete wish: ${error.message}`);
    },
  });
};

export const useShareWish = () => {
  return useMutation({
    mutationFn: (request: ShareWishRequest) => apiClient.shareWish(request),
    onSuccess: (data) => {
      toast.success(data.message || 'Wish shared successfully');
      
      // If it's a WhatsApp share and we have a URL, open it
      if (data.whatsapp_url) {
        window.open(data.whatsapp_url, '_blank');
      }
    },
    onError: (error: Error) => {
      toast.error(`Failed to share wish: ${error.message}`);
    },
  });
};

// Voice hooks
export const useSpeechToText = () => {
  return useMutation({
    mutationFn: (audioFile: File) => apiClient.speechToText(audioFile),
    onError: (error: Error) => {
      toast.error(`Failed to convert speech: ${error.message}`);
    },
  });
};

export const useDirectSpeechToText = () => {
  return useMutation({
    mutationFn: () => apiClient.directSpeechToText(),
    onError: (error: Error) => {
      toast.error(`Failed to process voice input: ${error.message}`);
    },
  });
};

export const useTextToSpeech = () => {
  return useMutation({
    mutationFn: ({ text, voice }: { text: string; voice?: string }) => 
      apiClient.textToSpeech(text, voice),
    onError: (error: Error) => {
      toast.error(`Failed to generate speech: ${error.message}`);
    },
  });
};
