// This logs people out
import { NextResponse } from 'next/server'

export async function POST() {
  const response = NextResponse.json({ message: "You've been logged out!" })
  
  // Clear the auth cookie
  response.cookies.set('auth-token', '', { 
    httpOnly: true, 
    expires: new Date(0) // This deletes the cookie
  })
  
  return response
}