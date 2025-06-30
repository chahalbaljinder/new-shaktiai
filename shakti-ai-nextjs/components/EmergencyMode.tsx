'use client'

import { motion } from 'framer-motion'
import { AlertTriangle, Phone, MessageSquare, Navigation } from 'lucide-react'

export default function EmergencyMode() {
  const emergencyContacts = [
    { name: 'Mental Health Helpline', number: '1-800-950-NAMI', available: '24/7' },
    { name: 'Crisis Text Line', number: 'Text HOME to 741741', available: '24/7' },
    { name: 'National Suicide Prevention', number: '988', available: '24/7' },
    { name: 'Emergency Services', number: '911', available: '24/7' }
  ]

  const quickActions = [
    { title: 'Breathing Exercise', action: 'Start guided breathing', icon: '🫁' },
    { title: 'Find Therapist', action: 'Locate nearby support', icon: '👨‍⚕️' },
    { title: 'Crisis Chat', action: 'Connect with counselor', icon: '💬' },
    { title: 'Emergency Plan', action: 'View your safety plan', icon: '📋' }
  ]

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="fixed inset-0 bg-red-50 z-50 p-6 overflow-y-auto"
    >
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-red-500 text-white p-6 rounded-xl mb-6">
          <div className="flex items-center space-x-3 mb-4">
            <AlertTriangle className="w-8 h-8" />
            <h1 className="text-2xl font-bold">Emergency Support Mode</h1>
          </div>
          <p className="text-red-100">
            You're not alone. Immediate help and resources are available. Your safety matters.
          </p>
        </div>

        {/* Emergency Contacts */}
        <div className="bg-white rounded-xl p-6 mb-6 shadow-lg">
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <Phone className="w-5 h-5 mr-2 text-red-500" />
            Emergency Contacts
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {emergencyContacts.map((contact, index) => (
              <motion.div
                key={index}
                whileHover={{ scale: 1.02 }}
                className="border border-red-200 rounded-lg p-4 hover:bg-red-50 transition-colors cursor-pointer"
              >
                <div className="font-semibold text-gray-900">{contact.name}</div>
                <div className="text-red-600 font-mono text-lg">{contact.number}</div>
                <div className="text-sm text-gray-500">{contact.available}</div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <MessageSquare className="w-5 h-5 mr-2 text-red-500" />
            Immediate Support
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {quickActions.map((action, index) => (
              <motion.button
                key={index}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="border border-gray-200 rounded-lg p-4 text-left hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{action.icon}</span>
                  <div>
                    <div className="font-semibold text-gray-900">{action.title}</div>
                    <div className="text-sm text-gray-600">{action.action}</div>
                  </div>
                </div>
              </motion.button>
            ))}
          </div>
        </div>

        {/* Breathing Exercise */}
        <div className="bg-blue-50 rounded-xl p-6 mt-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-4">Quick Breathing Exercise</h3>
          <div className="text-blue-800">
            <p className="mb-2">1. Breathe in slowly through your nose for 4 counts</p>
            <p className="mb-2">2. Hold your breath for 4 counts</p>
            <p className="mb-2">3. Breathe out slowly through your mouth for 6 counts</p>
            <p>4. Repeat 5-10 times</p>
          </div>
        </div>
      </div>
    </motion.div>
  )
}
