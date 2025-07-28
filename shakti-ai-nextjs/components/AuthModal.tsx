
'use client'
import { useState } from 'react'
import { useAuth } from './AuthProvider'

export default function AuthModal() {
  const [isLogin, setIsLogin] = useState(true)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const { login, register } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    try {
      if (isLogin) {
        const success = await login(email, password)
        if (!success) {
          setError('Invalid email or password')
        }
      } else {
        if (name.length < 2) {
          setError('Name must be at least 2 characters')
          return
        }
        const success = await register(name, email, password)
        if (!success) {
          setError('Registration failed. Email might already exist.')
        }
      }
    } catch (err) {
      console.error('Auth error:', err)
      setError('Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-8 rounded-lg max-w-md w-full mx-4">
        <h2 className="text-2xl font-bold mb-6">
          {isLogin ? 'Login to SHAKTI-AI' : 'Join SHAKTI-AI'}
        </h2>
        
        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <input
              type="text"
              placeholder="Your Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full p-3 border rounded focus:border-blue-500 focus:outline-none"
              required={!isLogin}
              disabled={loading}
            />
          )}
          
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-3 border rounded focus:border-blue-500 focus:outline-none"
            required
            disabled={loading}
          />
          
          <input
            type="password"
            placeholder="Password (min 6 characters)"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-3 border rounded focus:border-blue-500 focus:outline-none"
            required
            minLength={6}
            disabled={loading}
          />
          
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white p-3 rounded hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                {isLogin ? 'Logging in...' : 'Creating account...'}
              </>
            ) : (
              isLogin ? 'Login' : 'Sign Up'
            )}
          </button>
        </form>
        
        <button
          onClick={() => setIsLogin(!isLogin)}
          disabled={loading}
          className="w-full mt-4 text-blue-600 hover:underline disabled:text-gray-400"
        >
          {isLogin ? "Don't have an account? Sign Up" : "Already have an account? Login"}
        </button>
        
        {/* Test credentials hint */}
        {isLogin && (
          <div className="mt-4 p-3 bg-blue-50 border border-blue-200 text-blue-700 rounded text-sm">
            <strong>Test credentials:</strong><br />
            Email: test@example.com<br />
            Password: test123
          </div>
        )}
      </div>
    </div>
  )
}