'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useAppStore } from '@/lib/store'
import { useAuth } from '@/components/AuthProvider'
import AuthModal from '@/components/AuthModal'
import Sidebar from '@/components/Sidebar'
import Dashboard from '@/components/Dashboard'
import KnowledgeBase from '@/components/KnowledgeBase'
import WishesVault from '@/components/WishesVault'
import Settings from '@/components/Settings'
import VoiceInterface from '@/components/VoiceInterface'
import EmergencyMode from '@/components/EmergencyMode'
import AIAgents from '@/components/AIAgents'

const pageVariants = {
  initial: { opacity: 0, x: 20 },
  in: { opacity: 1, x: 0 },
  out: { opacity: 0, x: -20 }
}

const pageTransition = {
  type: 'tween',
  ease: 'anticipate',
  duration: 0.3
}

export default function HomePage() {
  const { currentPage, sidebarOpen, emergencyMode } = useAppStore()
  const { user, loading } = useAuth()

  // Show loading while checking authentication
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#F1F5F9]">
        <div className="text-xl text-[#3C50E0] font-semibold">Loading APEX...</div>
      </div>
    )
  }

  // Show authentication modal if not logged in
  if (!user) {
    return <AuthModal />
  }

  // If emergency mode is active, show only emergency interface
  if (emergencyMode) {
    return <EmergencyMode />
  }

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard userName="Apex" />
      case 'knowledge':
        return <KnowledgeBase />
      case 'wishes':
        return <WishesVault />
      case 'settings':
        return <Settings />
      case 'agents':
        return <AIAgents />
      default:
        return <Dashboard userName="Apex" />
    }
  }

  return (
    <div className="flex h-screen bg-[#F1F5F9] dark:bg-[#1C2434] overflow-hidden">
      {/* Sidebar */}
      <Sidebar />
      
      {/* Main Content */}
      <main 
        className={`flex-1 transition-all duration-300 ease-in-out lg:ml-0 overflow-y-auto`}
      >
        <AnimatePresence mode="wait">
          <motion.div
            key={currentPage}
            initial="initial"
            animate="in"
            exit="out"
            variants={pageVariants}
            transition={pageTransition}
            className="p-4 sm:p-6 lg:p-8"
          >
            {renderCurrentPage()}
          </motion.div>
        </AnimatePresence>
      </main>

      {/* Mobile Overlay */}
      {sidebarOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => useAppStore.getState().setSidebarOpen(false)}
        />
      )}

      {/* Voice Interface */}
      <VoiceInterface />
    </div>
  )
}
