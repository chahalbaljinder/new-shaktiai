// API client for SHAKTI-AI backend communication

export interface Agent {
  name: string;
  role: string;
  expertise: string;
  specialties: string[];
}

export interface Agents {
  [key: string]: Agent;
}

export interface ChatRequest {
  message: string;
  agentType: string;
}

export interface ChatResponse {
  response: string;
  agent_name: string;
  citations?: any[];
}

export interface Wish {
  id?: number;
  title: string;
  content: string;
  category?: string;
  priority?: string;
  reminder_date?: string;
  created_at?: string;
  updated_at?: string;
}

export interface ShareWishRequest {
  wishId: number;
  method: 'email' | 'whatsapp';
  recipient: string;
  senderName?: string;
}

export interface VoiceToTextResponse {
  text: string;
  success: boolean;
  error?: string;
}

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || '';
    console.log('API Client baseUrl:', this.baseUrl);
  }

  // Agent methods
  async getAgents(): Promise<{ agents: Agents }> {
    const response = await fetch(`${this.baseUrl}/api/agents`);
    if (!response.ok) throw new Error('Failed to fetch agents');
    return response.json();
  }

  async chatWithAgent(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}/api/agents/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });
    
    if (!response.ok) throw new Error('Failed to chat with agent');
    return response.json();
  }

  // Wishes Vault methods
  async getWishes(): Promise<{ wishes: Wish[] }> {
    const url = `${this.baseUrl}/api/wishes`;
    console.log('Fetching wishes from URL:', url);
    const response = await fetch(url);
    console.log('Response status:', response.status, response.statusText);
    if (!response.ok) throw new Error('Failed to fetch wishes');
    return response.json();
  }

  async createWish(wish: Omit<Wish, 'id' | 'created_at' | 'updated_at'>): Promise<{ success: boolean; wish_id: number; message: string }> {
    const response = await fetch(`${this.baseUrl}/api/wishes`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(wish),
    });
    
    if (!response.ok) throw new Error('Failed to create wish');
    return response.json();
  }

  async updateWish(wishId: number, updates: Partial<Wish>): Promise<{ success: boolean; message: string }> {
    const response = await fetch(`${this.baseUrl}/api/wishes/${wishId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updates),
    });
    
    if (!response.ok) throw new Error('Failed to update wish');
    return response.json();
  }

  async deleteWish(wishId: number): Promise<{ success: boolean; message: string }> {
    const response = await fetch(`${this.baseUrl}/api/wishes/${wishId}`, {
      method: 'DELETE',
    });
    
    if (!response.ok) throw new Error('Failed to delete wish');
    return response.json();
  }

  async shareWish(request: ShareWishRequest): Promise<{ success: boolean; message: string; whatsapp_url?: string }> {
    const response = await fetch(`${this.baseUrl}/api/wishes/share`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });
    
    if (!response.ok) throw new Error('Failed to share wish');
    return response.json();
  }

  // Voice methods
  async speechToText(audioFile: File): Promise<VoiceToTextResponse> {
    const formData = new FormData();
    formData.append('audio', audioFile);

    const response = await fetch(`${this.baseUrl}/api/voice/speech-to-text`, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) throw new Error('Failed to convert speech to text');
    return response.json();
  }

  async directSpeechToText(): Promise<VoiceToTextResponse> {
    const response = await fetch(`${this.baseUrl}/api/voice/direct-speech-to-text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) throw new Error('Failed to process direct speech to text');
    return response.json();
  }

  async textToSpeech(text: string, voice?: string): Promise<Blob> {
    const response = await fetch(`${this.baseUrl}/api/voice/text-to-speech`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text, voice }),
    });
    
    if (!response.ok) throw new Error('Failed to convert text to speech');
    return response.blob();
  }
}

export const apiClient = new ApiClient();
