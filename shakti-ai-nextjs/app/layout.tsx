import './globals.css'
import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import { Providers } from './providers'
import { Toaster } from 'sonner'
import SaheliChatbot from '@/components/SaheliChatbot'
import type { ReactNode } from 'react'



const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'SHAKTI-AI - Your AI Wellness Companion',
  description: 'AI-powered support for women\'s health, legal rights, and well-being',
  keywords: ['AI', 'health', 'wellness', 'women', 'support', 'mental health', 'legal rights'],
  authors: [{ name: 'SHAKTI-AI Team' }],
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

interface RootLayoutProps {
  children: ReactNode
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} h-full antialiased`}>
        <Providers>
          {children}
          <Toaster position="top-right" richColors closeButton />
          <SaheliChatbot />
        </Providers>
      </body>
    </html>
  )
}
