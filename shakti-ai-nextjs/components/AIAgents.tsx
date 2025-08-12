'use client'

import { motion } from 'framer-motion'
import { useAppStore } from '@/lib/store'
import { ArrowLeft, Brain, Heart, Shield, Users, Crown } from 'lucide-react'

const agents = [
  {
    id: 'maaya',
    name: 'Maaya - For Moms, By Heart',
    emoji: '🤱',
    expertise: 'Pregnancy, childbirth, and baby care',
    description: 'Maaya is your comforting pregnancy guide — here to cut through myths, answer every "is this normal?", and keep you calm from bump to baby, with advice that actually makes sense for you.',
    color: 'from-pink-500 to-rose-600',
    icon: Heart,
    specialties: [
      'Pregnancy guidance',
      'Childbirth preparation', 
      'Baby care tips',
      'Postpartum support',
      'Breastfeeding help',
      'Newborn development'
    ]
  },
  {
    id: 'gynika',
    name: 'Gynika - Flow Friend',
    emoji: '🌸',
    expertise: 'Menstruation, puberty, and contraception',
    description: 'Gynika is your real talk reproductive guide — ditching the whispers and giving you straight-up truth on your cycle, contraception, and more.',
    color: 'from-purple-500 to-pink-600',
    icon: Users,
    specialties: [
      'Menstrual health',
      'Puberty guidance',
      'Contraception advice',
      'Reproductive health',
      'Period management',
      'Body positivity'
    ]
  },
  {
    id: 'meher',
    name: 'Meher - Gentle Guide',
    emoji: '🫂',
    expertise: 'Emotional support for trauma, anxiety, and abuse',
    description: 'Meher is your gentle guide — here to listen without judging, name what hurts, and remind you you\'re never too much, even on your hardest days.',
    color: 'from-amber-500 to-orange-600',
    icon: Shield,
    specialties: [
      'Trauma support',
      'Anxiety management',
      'Abuse recovery',
      'Emotional wellness',
      'Mental health',
      'Crisis support'
    ]
  },
  {
    id: 'nyaya',
    name: 'Nyaya - Rights Ally',
    emoji: '⚖️',
    expertise: 'Indian laws on consent, abortion, and family rights',
    description: 'Nyaya is your rights ally — here to break down India\'s messy laws, decode your choices, and make sure you know exactly what\'s yours to fight for.',
    color: 'from-blue-500 to-indigo-600',
    icon: Shield,
    specialties: [
      'Legal rights education',
      'Consent laws',
      'Abortion rights',
      'Family law',
      'Women\'s rights',
      'Legal advocacy'
    ]
  },
  {
    id: 'vaanya',
    name: 'Vaanya - Age Rebel',
    emoji: '👑',
    expertise: 'Menopause, hormonal health, and women\'s empowerment',
    description: 'Vaanya is your health rebel — here to smash taboos, keep you clued up on your body, and remind you that ageing strong is your superpower.',
    color: 'from-emerald-500 to-teal-600',
    icon: Crown,
    specialties: [
      'Menopause guidance',
      'Hormonal health',
      'Women\'s empowerment',
      'Aging wellness',
      'Health advocacy',
      'Body confidence'
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
              Meet Your AI Support Team
            </h1>
            <p className="text-gray-600 dark:text-gray-300 mt-2">
              Five specialized experts ready to help with your wellness journey
            </p>
          </div>
        </motion.div>

        {/* AI Agents Grid */}
        <div className="space-y-6">
          {agents.map((agent, index) => (
            <motion.div
              key={agent.id}
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white dark:bg-slate-800 rounded-3xl p-8 shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden relative"
            >
              {/* Background decoration */}
              <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${agent.color} opacity-10 rounded-full blur-2xl`}></div>
              
              {/* Agent Header */}
              <div className="flex items-start justify-between mb-6 relative z-10">
                <div className="flex items-center space-x-4">
                  <div className={`w-16 h-16 bg-gradient-to-r ${agent.color} rounded-2xl flex items-center justify-center text-2xl shadow-lg`}>
                    {agent.emoji}
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                      {agent.name}
                    </h3>
                    <div className="flex items-center space-x-2">
                      <Brain className="w-5 h-5 text-gray-500" />
                      <span className="text-gray-600 dark:text-gray-300 font-medium">
                        Expertise: {agent.expertise}
                      </span>
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => setCurrentPage('knowledge')}
                  className={`px-6 py-3 bg-gradient-to-r ${agent.color} text-white rounded-xl font-medium hover:shadow-lg transform hover:scale-105 transition-all`}
                >
                  Chat Now
                </button>
              </div>

              {/* Agent Description */}
              <div className="mb-6 relative z-10">
                <p className="text-gray-700 dark:text-gray-300 text-lg leading-relaxed">
                  {agent.description}
                </p>
              </div>

              {/* Specialties */}
              <div className="relative z-10">
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                  Specializes in:
                </h4>
                <div className="grid grid-cols-2 lg:grid-cols-3 gap-3">
                  {agent.specialties.map((specialty, idx) => (
                    <div
                      key={idx}
                      className="flex items-center space-x-2 text-gray-600 dark:text-gray-300"
                    >
                      <div className={`w-2 h-2 bg-gradient-to-r ${agent.color} rounded-full`}></div>
                      <span className="text-sm">{specialty}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Hover effect overlay */}
              <motion.div
                className={`absolute inset-0 bg-gradient-to-r ${agent.color} opacity-0 hover:opacity-5 transition-opacity duration-300 rounded-3xl`}
                whileHover={{ opacity: 0.05 }}
              />
            </motion.div>
          ))}
        </div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-gradient-to-r from-purple-500 to-pink-600 rounded-3xl p-8 text-white text-center"
        >
          <h3 className="text-2xl font-bold mb-4">Ready to get started?</h3>
          <p className="text-lg opacity-90 mb-6">
            Choose any agent and start your conversation. They're here to support you 24/7.
          </p>
          <button
            onClick={() => setCurrentPage('knowledge')}
            className="bg-white text-purple-600 px-8 py-3 rounded-xl font-semibold hover:bg-gray-100 transform hover:scale-105 transition-all"
          >
            Start Chatting
          </button>
        </motion.div>
      </div>
    </div>
  )
}
