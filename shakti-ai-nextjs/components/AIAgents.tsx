'use client'

import { motion } from 'framer-motion'
import { useAppStore } from '@/lib/store'
import { ArrowLeft, Brain, Heart, Shield, Users, Crown } from 'lucide-react'

const agents = [
  {
    id: 'athena',
    name: 'Athena - Policy & Procedure Guide',
    emoji: '⚖️',
    expertise: 'Government policies, legal procedures, and rights guidance',
    description: 'Athena is your policy expert — trained on HR circulars, POSH Act, leave policies, and government regulations to guide you through complex procedures with precision.',
    color: 'from-blue-500 to-indigo-600',
    icon: Shield,
    specialties: [
      'Maternity Leave guidance',
      'Child Care Leave (CCL)',
      'POSH Act compliance',
      'Transfer policies',
      'Legal rights education',
      'Government regulations'
    ]
  },
  {
    id: 'asha',
    name: 'Asha - Wellness & Support Companion',
    emoji: '🌸',
    expertise: 'Emotional wellness, work-life balance, and confidential support',
    description: 'Asha is your empathetic companion — providing confidential emotional support, wellness resources, and guidance for work-life integration challenges.',
    color: 'from-purple-500 to-pink-600',
    icon: Heart,
    specialties: [
      'Emotional wellness',
      'Work-life balance',
      'Stress management',
      'Confidential support',
      'Mental health resources',
      'Career guidance'
    ]
  },
  {
    id: 'scribe',
    name: 'Scribe - Documentation & Workflow Expert',
    emoji: '📋',
    expertise: 'Document generation, form filling, and process automation',
    description: 'Scribe is your documentation specialist — helping generate official forms, create checklists, and streamline complex administrative processes efficiently.',
    color: 'from-emerald-500 to-teal-600',
    icon: Brain,
    specialties: [
      'Form generation',
      'Leave applications',
      'Transfer requests',
      'Grievance filing',
      'Process checklists',
      'Document automation'
    ]
  }
]

export default function AIAgents() {
  const { setCurrentPage } = useAppStore()

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800">
      <div className="p-6 lg:p-8 max-w-7xl mx-auto space-y-8 pb-20">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center space-x-4"
        >
          <button
            onClick={() => setCurrentPage('dashboard')}
            className="p-2 hover:bg-white/10 rounded-xl transition-colors"
          >
            <ArrowLeft className="w-6 h-6 text-gray-600" />
          </button>
          <div>
            <h1 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white">
              Meet Your APEX AI Support Team
            </h1>
            <p className="text-gray-600 dark:text-gray-300 mt-2">
              Three specialized experts ready to help women scientists navigate government organizations
            </p>
          </div>
        </motion.div>

        {/* AI Agents Grid */}
        <div className="grid gap-4 lg:gap-6">
          {agents.map((agent, index) => (
            <motion.div
              key={agent.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="bg-white dark:bg-slate-800 rounded-xl p-5 shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-all duration-200 relative group overflow-hidden"
            >
              {/* Background decoration */}
              <div className={`absolute top-0 right-0 w-20 h-20 bg-gradient-to-br ${agent.color} opacity-5 group-hover:opacity-10 rounded-full blur-xl transition-opacity`}></div>
              
              <div className="relative z-10 grid lg:grid-cols-12 gap-4 items-start">
                {/* Left: Avatar & Basic Info */}
                <div className="lg:col-span-8 flex items-start space-x-3">
                  <div className={`w-10 h-10 bg-gradient-to-r ${agent.color} rounded-lg flex items-center justify-center text-base shadow-sm flex-shrink-0`}>
                    {agent.emoji}
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-lg font-bold text-gray-900 dark:text-white truncate pr-2">
                        {agent.name}
                      </h3>
                      <button
                        onClick={() => setCurrentPage('knowledge')}
                        className={`lg:hidden px-3 py-1.5 bg-gradient-to-r ${agent.color} text-white rounded-md text-xs font-medium hover:shadow-sm transition-all flex-shrink-0`}
                      >
                        Chat
                      </button>
                    </div>
                    
                    <div className="flex items-center space-x-2 mb-3">
                      <Brain className="w-3.5 h-3.5 text-gray-500 flex-shrink-0" />
                      <span className="text-gray-600 dark:text-gray-300 text-xs font-medium line-clamp-1">
                        {agent.expertise}
                      </span>
                    </div>
                    
                    <p className="text-gray-700 dark:text-gray-300 text-xs leading-relaxed line-clamp-2 mb-3">
                      {agent.description}
                    </p>
                    
                    {/* Specialties - Compact Tags */}
                    <div className="flex flex-wrap gap-1.5">
                      {agent.specialties.slice(0, 4).map((specialty, idx) => (
                        <span
                          key={idx}
                          className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gradient-to-r ${agent.color} bg-opacity-10 text-gray-700 dark:text-gray-300`}
                        >
                          {specialty}
                        </span>
                      ))}
                      {agent.specialties.length > 4 && (
                        <span className="text-xs text-gray-500 px-1">
                          +{agent.specialties.length - 4} more
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Right: Action Button */}
                <div className="lg:col-span-4 hidden lg:flex justify-end">
                  <button
                    onClick={() => setCurrentPage('knowledge')}
                    className={`px-4 py-2 bg-gradient-to-r ${agent.color} text-white rounded-lg text-sm font-medium hover:shadow-lg transform hover:scale-105 transition-all whitespace-nowrap`}
                  >
                    Chat Now
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-gradient-to-r from-purple-500 to-pink-600 rounded-xl p-5 text-white text-center"
        >
          <h3 className="text-lg font-bold mb-2">Ready to get started?</h3>
          <p className="text-sm opacity-90 mb-4">
            Choose any agent and start your conversation. They're here to support you in your scientific career.
          </p>
          <button
            onClick={() => setCurrentPage('knowledge')}
            className="bg-white text-purple-600 px-5 py-2 rounded-lg text-sm font-semibold hover:bg-gray-100 transform hover:scale-105 transition-all"
          >
            Start Chatting
          </button>
        </motion.div>
      </div>
    </div>
  )
}
