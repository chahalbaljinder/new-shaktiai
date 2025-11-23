/**
 * API Utility Functions for APEX System
 * Centralized API calls to the Flask backend
 */

const API_BASE_URL = 'http://localhost:8000/api'

// Helper function to handle API responses
async function handleResponse(response: Response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Network error' }))
    throw new Error(error.message || 'API request failed')
  }
  return response.json()
}

// Authentication
export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    return handleResponse(response)
  }
}

// Dashboard
export const dashboardAPI = {
  getStats: async () => {
    const response = await fetch(`${API_BASE_URL}/dashboard/stats`)
    return handleResponse(response)
  },
  
  getRecentQueries: async () => {
    const response = await fetch(`${API_BASE_URL}/dashboard/recent-queries`)
    return handleResponse(response)
  },
  
  getPersonnelDistribution: async () => {
    const response = await fetch(`${API_BASE_URL}/dashboard/personnel-distribution`)
    return handleResponse(response)
  }
}

// Feedback
export const feedbackAPI = {
  getAll: async (filters?: { type?: string; status?: string; search?: string }) => {
    const params = new URLSearchParams()
    if (filters?.type) params.append('type', filters.type)
    if (filters?.status) params.append('status', filters.status)
    if (filters?.search) params.append('search', filters.search)
    
    const response = await fetch(`${API_BASE_URL}/feedback?${params}`)
    return handleResponse(response)
  },
  
  submit: async (data: {
    user_id: number
    type: string
    title: string
    description: string
    category: string
    priority: string
    is_anonymous: boolean
  }) => {
    const response = await fetch(`${API_BASE_URL}/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  },
  
  getStats: async () => {
    const response = await fetch(`${API_BASE_URL}/feedback/stats`)
    return handleResponse(response)
  }
}

// Knowledge Base
export const knowledgeAPI = {
  query: async (data: {
    user_id: number
    query_text: string
    response_text: string
    response_time_ms: number
    sources?: string[]
    category?: string
  }) => {
    const response = await fetch(`${API_BASE_URL}/knowledge/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  }
}

// Wishes Vault
export const wishesAPI = {
  getAll: async (userId: number) => {
    const response = await fetch(`${API_BASE_URL}/wishes?user_id=${userId}`)
    return handleResponse(response)
  },
  
  create: async (data: {
    user_id: number
    title: string
    content: string
    category: string
    priority: string
  }) => {
    const response = await fetch(`${API_BASE_URL}/wishes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    return handleResponse(response)
  }
}

// Health Check
export const systemAPI = {
  healthCheck: async () => {
    const response = await fetch('http://localhost:8000/health')
    return handleResponse(response)
  },
  
  getStatus: async () => {
    const response = await fetch(`${API_BASE_URL}/status`)
    return handleResponse(response)
  }
}

export default {
  auth: authAPI,
  dashboard: dashboardAPI,
  feedback: feedbackAPI,
  knowledge: knowledgeAPI,
  wishes: wishesAPI,
  system: systemAPI
}
