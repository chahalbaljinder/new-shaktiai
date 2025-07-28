// Debug authentication status
'use client'

import { useAuth } from '@/components/AuthProvider'
import { useEffect } from 'react'

export default function AuthDebug() {
  const { user, loading } = useAuth()

  useEffect(() => {
    console.log('🔍 Auth Debug Info:')
    console.log('Loading:', loading)
    console.log('User:', user)
    console.log('Cookies:', document.cookie)
    
    // Test the /me endpoint directly
    fetch('/api/auth/me')
      .then(res => res.json())
      .then(data => {
        console.log('Direct /me call result:', data)
      })
      .catch(err => {
        console.error('Direct /me call error:', err)
      })
  }, [user, loading])

  return (
    <div className="p-4 bg-yellow-100 border border-yellow-400 rounded m-4">
      <h2 className="font-bold text-lg">🔍 Authentication Debug</h2>
      <div className="mt-2">
        <p><strong>Loading:</strong> {loading.toString()}</p>
        <p><strong>User:</strong> {user ? JSON.stringify(user) : 'null'}</p>
        <p><strong>Should show login:</strong> {(!user && !loading).toString()}</p>
      </div>
      <button 
        onClick={() => {
          console.log('🧹 Clearing cookies...')
          document.cookie = 'auth-token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
          window.location.reload()
        }}
        className="mt-2 px-4 py-2 bg-red-500 text-white rounded"
      >
        Clear Auth & Reload
      </button>
    </div>
  )
}
