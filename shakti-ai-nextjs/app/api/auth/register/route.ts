// This lets new people join the club
import { NextRequest, NextResponse } from 'next/server'
import { createUser, findUserByEmail } from '@/lib/auth/utils'
import { registerSchema } from '@/lib/auth/schemas'

export async function POST(request: NextRequest) {
  const body = await request.json()
  
  // Check if they filled out the form correctly
  const validation = registerSchema.safeParse(body)
  if (!validation.success) {
    return NextResponse.json({ error: "Please fill out the form correctly" }, { status: 400 })
  }
  
  // Check if someone already has that email
  const existingUser = await findUserByEmail(body.email)
  if (existingUser) {
    return NextResponse.json({ error: "Someone already has that email!" }, { status: 400 })
  }
  
  // Create the new user
  const user = await createUser(body.name, body.email, body.password)
  
  return NextResponse.json({ message: "Welcome to SHAKTI-AI!", user })
}