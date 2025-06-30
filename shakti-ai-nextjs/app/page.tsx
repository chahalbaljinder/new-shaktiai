'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useAppStore } from '@/lib/store'
import Sidebar from '@/components/Sidebar'
import Dashboard from '@/components/Dashboard'
import KnowledgeBase from '@/components/KnowledgeBase'
import WishesVault from '@/components/WishesVault'
import Settings from '@/components/Settings'
import VoiceInterface from '@/components/VoiceInterface'
import EmergencyMode from '@/components/EmergencyMode'

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

  // If emergency mode is active, show only emergency interface
  if (emergencyMode) {
    return <EmergencyMode />
  }

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard userName="Shakti" />
      case 'knowledge':
        return <KnowledgeBase />
      case 'wishes':
        return <WishesVault />
      case 'settings':
        return <Settings />
      default:
        return <Dashboard userName="Shakti" />
    }
  }

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
      {/* Sidebar */}
      <Sidebar />
      
      {/* Main Content */}
      <main 
        className={`flex-1 transition-all duration-300 ease-in-out ${
          sidebarOpen ? 'ml-0' : 'ml-0'
        } lg:ml-0`}
      >
        <div className="min-h-screen overflow-y-auto">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentPage}
              initial="initial"
              animate="in"
              exit="out"
              variants={pageVariants}
              transition={pageTransition}
              className="min-h-screen"
            >
              {renderCurrentPage()}
            </motion.div>
          </AnimatePresence>
        </div>
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
