'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Home, 
  Brain, 
  Lock, 
  Settings, 
  Mic, 
  AlertTriangle,
  Menu,
  X,
  Sun,
  Moon,
  User
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { useAppStore } from '@/lib/store'

const navigation = [
  { id: 'dashboard', name: 'Dashboard', icon: Home, emoji: '🏠' },
  { id: 'knowledge', name: 'Knowledge Base', icon: Brain, emoji: '🧠' },
  { id: 'wishes', name: 'Wishes Vault', icon: Lock, emoji: '🔐' },
  { id: 'settings', name: 'Settings', icon: Settings, emoji: '⚙️' },
]

export default function Sidebar() {
  const { 
    currentPage, 
    setCurrentPage, 
    sidebarOpen, 
    setSidebarOpen, 
    voiceActive, 
    setVoiceActive, 
    emergencyMode, 
    setEmergencyMode 
  } = useAppStore()
  
  const [theme, setTheme] = useState<'light' | 'dark'>('light')

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light')
  }

  return (
    <>
      {/* Mobile backdrop */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <motion.div
        initial={false}
        animate={{ x: sidebarOpen ? 0 : -280 }}
        transition={{ type: 'spring', damping: 30, stiffness: 300 }}
        className="fixed left-0 top-0 h-full w-70 bg-white border-r border-gray-200 shadow-xl z-50 lg:relative lg:translate-x-0"
      >
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-gray-200">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-primary rounded-xl flex items-center justify-center text-white text-xl font-bold">
                🧬
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">SHAKTI-AI</h1>
                <p className="text-sm text-gray-500">Your AI Support</p>
              </div>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <X size={20} />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-2">
            {navigation.map((item) => {
              const isActive = currentPage === item.id
              return (
                <motion.button
                  key={item.id}
                  whileHover={{ x: 4 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setCurrentPage(item.id)}
                  className={cn(
                    'w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 text-left',
                    isActive
                      ? 'bg-gradient-primary text-white shadow-lg'
                      : 'text-gray-700 hover:bg-gray-100'
                  )}
                >
                  <span className="text-xl">{item.emoji}</span>
                  <span className="font-medium">{item.name}</span>
                  {isActive && (
                    <motion.div
                      layoutId="activeTab"
                      className="ml-auto w-2 h-2 bg-white rounded-full"
                    />
                  )}
                </motion.button>
              )
            })}
          </nav>

          {/* Bottom Actions */}
          <div className="p-4 border-t border-gray-200 space-y-3">
            {/* Voice Input */}
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setVoiceActive(!voiceActive)}
              className={cn(
                'w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200',
                voiceActive
                  ? 'bg-gradient-secondary text-white animate-pulse'
                  : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100'
              )}
            >
              <Mic size={20} />
              <span className="font-medium">
                {voiceActive ? 'Listening...' : 'Voice Input'}
              </span>
            </motion.button>

            {/* Emergency */}
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setEmergencyMode(!emergencyMode)}
              className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl bg-red-50 text-red-700 hover:bg-red-100 transition-all duration-200"
            >
              <AlertTriangle size={20} />
              <span className="font-medium">Emergency</span>
            </motion.button>

            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-gray-700 hover:bg-gray-100 transition-all duration-200"
            >
              {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
              <span className="font-medium">
                {theme === 'light' ? 'Dark Mode' : 'Light Mode'}
              </span>
            </button>

            {/* User Profile */}
            <div className="flex items-center space-x-3 px-4 py-3 rounded-xl bg-gray-50">
              <div className="w-8 h-8 bg-gradient-primary rounded-full flex items-center justify-center text-white">
                <User size={16} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  Welcome User
                </p>
                <p className="text-xs text-gray-500">Online</p>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Mobile menu button */}
      <button
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="fixed top-4 left-4 z-50 lg:hidden p-3 bg-white rounded-xl shadow-lg border border-gray-200"
      >
        <Menu size={20} />
      </button>
    </>
  )
}
