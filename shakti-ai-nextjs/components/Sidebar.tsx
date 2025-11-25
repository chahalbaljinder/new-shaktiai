'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Home, 
  Brain, 
  Lock, 
  Settings, 
  AlertTriangle,
  Menu,
  X,
  User,
  LogOut,
  MessageSquare,
  Shield,
  FileText
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { useAppStore } from '@/lib/store'
import { useAuth } from './AuthProvider'
import { useRouter } from 'next/navigation'

const getNavigation = (userRole?: string) => {
  const baseNav = [
    { id: 'dashboard', name: 'Dashboard', icon: Home, emoji: '🏠' },
    { id: 'knowledge', name: 'Knowledge Base', icon: Brain, emoji: '🧠' },
    { id: 'policy-queries', name: 'Policy Queries', icon: FileText, emoji: '📋' },
    { id: 'wishes', name: 'Wishes Vault', icon: Lock, emoji: '🔐' },
    { id: 'feedback-module', name: 'Submit Feedback', icon: MessageSquare, emoji: '✍️' },
    { id: 'feedback', name: 'Grievance Dashboard', icon: AlertTriangle, emoji: '📊' },
    { id: 'settings', name: 'Settings', icon: Settings, emoji: '⚙️' },
  ];
  
  // Add SuperAdmin panel only for superadmin role
  if (userRole === 'superadmin') {
    baseNav.splice(baseNav.length - 1, 0, {
      id: 'admin',
      name: 'Admin Panel',
      icon: Shield,
      emoji: '🛡️',
      href: '/admin'
    });
  }
  
  return baseNav;
}

export default function Sidebar() {
  const { 
    currentPage, 
    setCurrentPage, 
    sidebarOpen, 
    setSidebarOpen, 
    emergencyMode, 
    setEmergencyMode 
  } = useAppStore()
  
  const { user, logout } = useAuth()
  const router = useRouter()
  
  const navigation = getNavigation(user?.role)

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
        className="fixed left-0 top-0 h-screen w-70 bg-[#1C2434] border-r border-[#2E3A47] shadow-xl z-50 lg:relative lg:translate-x-0 overflow-y-auto"
      >
        <div className="flex flex-col min-h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-[#2E3A47]">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-[#3C50E0] rounded-lg flex items-center justify-center text-white text-xl font-bold">
                🧬
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">APEX</h1>
                <p className="text-sm text-gray-400">Your AI Support</p>
              </div>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden p-2 rounded-lg hover:bg-[#2E3A47] transition-colors text-white"
            >
              <X size={20} />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-1">
            {navigation.map((item) => {
              const isActive = currentPage === item.id
              
              // Handle items with href (external links/pages)
              if (item.href) {
                return (
                  <motion.button
                    key={item.id}
                    onClick={() => {
                      router.push(item.href)
                      if (window.innerWidth < 1024) {
                        setSidebarOpen(false)
                      }
                    }}
                    whileHover={{ x: 4 }}
                    whileTap={{ scale: 0.98 }}
                    className={cn(
                      'w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 text-left',
                      'text-gray-300 hover:bg-[#2E3A47] hover:text-white'
                    )}
                  >
                    <item.icon size={20} />
                    <span className="font-medium">{item.name}</span>
                  </motion.button>
                )
              }
              
              return (
                <motion.button
                  key={item.id}
                  whileHover={{ x: 4 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => {
                    setCurrentPage(item.id)
                    // Auto-close sidebar on mobile after selection
                    if (window.innerWidth < 1024) {
                      setSidebarOpen(false)
                    }
                  }}
                  className={cn(
                    'w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 text-left group',
                    isActive
                      ? 'bg-[#3C50E0] text-white shadow-lg'
                      : 'text-gray-300 hover:bg-[#2E3A47] hover:text-white'
                  )}
                >
                  <item.icon size={20} />
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
          <div className="p-4 border-t border-[#2E3A47] space-y-3">
            {/* Emergency */}
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setEmergencyMode(!emergencyMode)}
              className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg bg-[#2E3A47] text-red-400 hover:bg-red-500 hover:text-white transition-all duration-200"
            >
              <AlertTriangle size={20} />
              <span className="font-medium">Emergency</span>
            </motion.button>

            {/* User Profile */}
            <div className="space-y-2">
              <div className="flex items-center space-x-3 px-4 py-3 rounded-lg bg-[#2E3A47]">
                <div className="w-8 h-8 bg-[#3C50E0] rounded-full flex items-center justify-center text-white">
                  <User size={16} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-white truncate">
                    {user?.name || 'User'}
                  </p>
                  <p className="text-xs text-gray-400 truncate">
                    {user?.email}
                  </p>
                </div>
              </div>
              
              {/* Logout Button */}
              <button
                onClick={() => {
                  logout()
                  setSidebarOpen(false)
                }}
                className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-red-400 hover:bg-red-500 hover:text-white transition-colors group"
              >
                <LogOut size={18} className="group-hover:scale-110 transition-transform" />
                <span className="font-medium">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Mobile menu button */}
      <button
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="fixed top-4 left-4 z-50 lg:hidden p-3 bg-white rounded-lg shadow-lg border border-gray-200"
      >
        <Menu size={20} className="text-gray-700" />
      </button>
    </>
  )
}
