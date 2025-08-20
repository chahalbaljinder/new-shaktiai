import bcrypt from 'bcryptjs'
import jwt from 'jsonwebtoken'
import { users, type User } from '@/lib/db'

export async function findUserByEmail(email: string): Promise<User | undefined> {
  return users.find(u => u.email.toLowerCase() === email.toLowerCase())
}

export async function checkPassword(plain: string, hashed: string): Promise<boolean> {
  try {
    return await bcrypt.compare(plain, hashed)
  } catch {
    return false
  }
}

export function createToken(userId: number): string {
  const secret = process.env.JWT_SECRET || 'your-super-secret-key'
  return jwt.sign({ userId }, secret, { expiresIn: '7d' })
}

export async function createUser(name: string, email: string, password: string): Promise<User> {
  const salt = await bcrypt.genSalt(10)
  const hash = await bcrypt.hash(password, salt)
  const user: User = {
    id: users.length > 0 ? users[users.length - 1].id + 1 : 1,
    name,
    email,
    password: hash,
  }
  users.push(user)
  return { ...user, password: user.password }
}
