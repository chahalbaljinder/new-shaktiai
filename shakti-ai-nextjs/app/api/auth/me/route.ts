// This checks if someone is already logged in
import { NextRequest, NextResponse } from 'next/server'
import jwt from 'jsonwebtoken'
import { pool } from '@/lib/db'

export async function GET(request: NextRequest) {
  try {
    // Get the auth token from cookies
    const token = request.cookies.get('auth-token')?.value
    
    if (!token) {
      return NextResponse.json({ user: null })
    }
    
    // Check if the token is valid
    const secret = process.env.JWT_SECRET || 'your-super-secret-key'
    const decoded = jwt.verify(token, secret) as { userId: number }
    
    // Get user from database
    const result = await pool.query('SELECT id, name, email FROM users WHERE id = $1', [decoded.userId])
    const user = result.rows[0]
    
    if (!user) {
      return NextResponse.json({ user: null })
    }
    
    return NextResponse.json({ user })
    
  } catch (error) {
    console.error('Auth verification error:', error)
    return NextResponse.json({ user: null })
  }
}