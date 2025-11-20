import './globals.css'
import type { Metadata, Viewport } from 'next'
import { Outfit } from 'next/font/google'
import { Providers } from './providers'
import { Toaster } from 'sonner'
import SaheliChatbot from '@/components/SaheliChatbot'
import type { ReactNode } from 'react'



const outfit = Outfit({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Project APEX - AI Companion for Women Scientists',
  description: 'AI-powered support for women scientists in Indian government organizations',
  keywords: ['AI', 'women scientists', 'government', 'DRDO', 'ISRO', 'CSIR', 'policy guidance', 'wellness'],
  authors: [{ name: 'APEX Team' }],
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
      <body className={`${outfit.className} h-full antialiased`}>
        <Providers>
          {children}
          <Toaster position="top-right" richColors closeButton />
          <SaheliChatbot />
        </Providers>
      </body>
    </html>
  )
}
