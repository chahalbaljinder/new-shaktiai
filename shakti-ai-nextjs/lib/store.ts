import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  name: string
  email: string
  avatar?: string
  preferences: {
    theme: 'light' | 'dark' | 'auto'
    language: string
    notifications: boolean
    voiceEnabled: boolean
  }
}

interface Wish {
  id: string
  title: string
  content: string
  category: string
  priority: 'low' | 'medium' | 'high'
  isPrivate: boolean
  tags: string[]
  createdAt: Date
  updatedAt: Date
}

interface ChatMessage {
  id: string
  content: string
  role: 'user' | 'agent'
  agentName?: string
  timestamp: Date
  sources?: string[]
}

interface AppState {
  // User state
  user: User | null
  setUser: (user: User | null) => void
  
  // Navigation state
  currentPage: string
  setCurrentPage: (page: string) => void
  sidebarOpen: boolean
  setSidebarOpen: (open: boolean) => void
  
  // Wishes state
  wishes: Wish[]
  addWish: (wish: Omit<Wish, 'id' | 'createdAt' | 'updatedAt'>) => void
  updateWish: (id: string, updates: Partial<Wish>) => void
  deleteWish: (id: string) => void
  
  // Chat state
  chatHistory: ChatMessage[]
  addMessage: (message: Omit<ChatMessage, 'id'>) => void
  clearChat: () => void
  
  // Voice state
  voiceActive: boolean
  setVoiceActive: (active: boolean) => void
  
  // Emergency state
  emergencyMode: boolean
  setEmergencyMode: (active: boolean) => void
  
  // Selected agents
  selectedAgents: string[]
  setSelectedAgents: (agents: string[]) => void
}

export const useAppStore = create<AppState>()(
  persist(
    (set, get) => ({
      // User state
      user: null,
      setUser: (user) => set({ user }),
      
      // Navigation state
      currentPage: 'dashboard',
      setCurrentPage: (page) => set({ currentPage: page }),
      sidebarOpen: true,
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
      
      // Wishes state
      wishes: [],
      addWish: (wishData) => {
        const newWish: Wish = {
          ...wishData,
          id: Date.now().toString(),
          createdAt: new Date(),
          updatedAt: new Date(),
        }
        set((state) => ({ wishes: [...state.wishes, newWish] }))
      },
      updateWish: (id, updates) => {
        set((state) => ({
          wishes: state.wishes.map((wish) =>
            wish.id === id ? { ...wish, ...updates, updatedAt: new Date() } : wish
          ),
        }))
      },
      deleteWish: (id) => {
        set((state) => ({
          wishes: state.wishes.filter((wish) => wish.id !== id),
        }))
      },
      
      // Chat state
      chatHistory: [],
      addMessage: (messageData) => {
        const newMessage: ChatMessage = {
          ...messageData,
          id: Date.now().toString(),
        }
        set((state) => ({ chatHistory: [...state.chatHistory, newMessage] }))
      },
      clearChat: () => set({ chatHistory: [] }),
      
      // Voice state
      voiceActive: false,
      setVoiceActive: (active) => set({ voiceActive: active }),
      
      // Emergency state
      emergencyMode: false,
      setEmergencyMode: (active) => set({ emergencyMode: active }),
      
      // Selected agents
      selectedAgents: [],
      setSelectedAgents: (agents) => set({ selectedAgents: agents }),
    }),
    {
      name: 'shakti-ai-storage',
      partialize: (state) => ({
        user: state.user,
        wishes: state.wishes,
        chatHistory: state.chatHistory,
        selectedAgents: state.selectedAgents,
      }),
    }
  )
)
