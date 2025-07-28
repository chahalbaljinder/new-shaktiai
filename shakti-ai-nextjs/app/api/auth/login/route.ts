// This lets existing members back in
import { NextRequest, NextResponse } from 'next/server'
import { findUserByEmail, checkPassword, createToken } from '@/lib/auth/utils'

export async function POST(request: NextRequest) {
  const { email, password } = await request.json()
  
  // Find the user
  const user = await findUserByEmail(email)
  if (!user) {
    return NextResponse.json({ error: "Wrong email or password!" }, { status: 401 })
  }
  
  // Check if password is correct
  const isPasswordCorrect = await checkPassword(password, user.password)
  if (!isPasswordCorrect) {
    return NextResponse.json({ error: "Wrong email or password!" }, { status: 401 })
  }
  
  // Give them an ID card (token)
  const token = createToken(user.id)
  
  // Send response with cookie
  const response = NextResponse.json({ message: "Welcome back!", user })
  response.cookies.set('auth-token', token, { httpOnly: true, maxAge: 7 * 24 * 60 * 60 })
  
  return response
}