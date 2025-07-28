'use client'
import { createContext, useContext, useEffect, useState } from 'react'

interface User {
  id: number
  name: string
  email: string
}

interface AuthContextType {
  user: User | null
  login: (email: string, password: string) => Promise<boolean>
  register: (name: string, email: string, password: string) => Promise<boolean>
  logout: () => void
  loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      
      if (response.ok) {
        const data = await response.json()
        setUser(data.user)
        return true
      } else {
        const errorData = await response.json()
        console.error('Login failed:', errorData)
        return false
      }
    } catch (error) {
      console.error('Login error:', error)
      return false
    }
  }

  const register = async (name: string, email: string, password: string): Promise<boolean> => {
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password }),
      })
      
      if (response.ok) {
        const data = await response.json()
        setUser(data.user)
        return true
      } else {
        const errorData = await response.json()
        console.error('Registration failed:', errorData)
        return false
      }
    } catch (error) {
      console.error('Register error:', error)
      return false
    }
  }

  const logout = () => {
    setUser(null)
    fetch('/api/auth/logout', { method: 'POST' })
  }

  useEffect(() => {
    console.log('AuthProvider: Starting auth check...')
    
    // Simple fetch with immediate timeout fallback
    const checkAuth = () => {
      console.log('AuthProvider: Making API call to /api/auth/me')
      
      fetch('/api/auth/me')
        .then(res => {
          console.log('AuthProvider: API response received', res.status)
          if (res.ok) {
            return res.json()
          }
          throw new Error('API response not ok')
        })
        .then(data => {
          console.log('AuthProvider: Response data:', data)
          if (data && data.user) {
            setUser(data.user)
          }
        })
        .catch(error => {
          console.log('AuthProvider: Auth check failed:', error)
        })
        .finally(() => {
          console.log('AuthProvider: Setting loading to false')
          setLoading(false)
        })
      
      // Fallback timeout - if API doesn't respond in 2 seconds, stop loading anyway
      setTimeout(() => {
        console.log('AuthProvider: Fallback timeout - stopping loading')
        setLoading(false)
      }, 2000)
    }
    
    checkAuth()
  }, [])

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}