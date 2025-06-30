'use client'

import { motion } from 'framer-motion'
import { Bell, Sun, Cloud, CloudRain, Thermometer } from 'lucide-react'

interface DashboardProps {
  userName?: string
}

const weatherData = {
  location: 'New Delhi',
  temperature: 28,
  condition: 'Clear Sky',
  humidity: 65,
  windSpeed: 12,
  icon: '☀️'
}

const quickStats = [
  {
    label: 'AI Experts',
    value: '5',
    icon: '🧠',
    color: 'from-blue-500 to-purple-600'
  },
  {
    label: 'Available',
    value: '24/7',
    icon: '💬',
    color: 'from-green-500 to-emerald-600'
  },
  {
    label: 'Secure',
    value: 'Private',
    icon: '🔐',
    color: 'from-purple-500 to-pink-600'
  },
  {
    label: 'Voice',
    value: 'Ready',
    icon: '🎤',
    color: 'from-amber-500 to-orange-600'
  }
]

const quickActions = [
  {
    title: 'Ask Expert',
    description: 'Get instant guidance from AI specialists',
    icon: '💬',
    color: 'from-blue-500 to-blue-600',
    action: 'knowledge'
  },
  {
    title: 'New Wish',
    description: 'Create and save your personal goals',
    icon: '📝',
    color: 'from-purple-500 to-purple-600',
    action: 'vault'
  },
  {
    title: 'Voice Chat',
    description: 'Talk directly with our AI team',
    icon: '🎤',
    color: 'from-emerald-500 to-emerald-600',
    action: 'voice'
  },
  {
    title: 'Health Log',
    description: 'Track your wellness journey',
    icon: '📊',
    color: 'from-pink-500 to-rose-600',
    action: 'health'
  },
  {
    title: 'Know Rights',
    description: 'Learn about your legal protections',
    icon: '⚖️',
    color: 'from-indigo-500 to-indigo-600',
    action: 'rights'
  },
  {
    title: 'Emergency',
    description: 'Quick access to emergency resources',
    icon: '🆘',
    color: 'from-red-500 to-red-600',
    action: 'emergency'
  }
]

const recentActivity = [
  {
    type: 'chat',
    title: 'Chat with Gynika about periods',
    time: '2 hours ago',
    icon: '💬'
  },
  {
    type: 'wish',
    title: 'New wish: "Learn meditation"',
    time: 'Yesterday',
    icon: '✨'
  },
  {
    type: 'share',
    title: 'Shared wish with friend',
    time: '2 days ago',
    icon: '📤'
  }
]

export default function Dashboard({ userName = 'User' }: DashboardProps) {
  return (
    <div className="min-h-screen overflow-y-auto">
      <div className="p-6 lg:p-8 max-w-7xl mx-auto space-y-8 pb-20">
        {/* Welcome Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-primary rounded-3xl p-8 text-white relative overflow-hidden"
        >
          <div className="relative z-10">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl lg:text-4xl font-bold mb-2">
                  Welcome back, {userName}! 👋
                </h1>
                <p className="text-lg opacity-90">
                  Your AI wellness companion is ready to help
                </p>
              </div>
            <div className="hidden lg:flex items-center space-x-6">
              <div className="flex items-center space-x-2 bg-white/20 rounded-full px-4 py-2">
                <span className="text-2xl">{weatherData.icon}</span>
                <div>
                  <div className="font-semibold">{weatherData.temperature}°C</div>
                  <div className="text-sm opacity-75">{weatherData.condition}</div>
                </div>
              </div>
              <div className="flex items-center space-x-2 bg-white/20 rounded-full px-4 py-2">
                <div className="w-3 h-3 bg-emerald-400 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium">All Systems Ready</span>
              </div>
            </div>
          </div>
        </div>
        
        {/* Background decoration */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-32 -right-32 w-64 h-64 bg-white/10 rounded-full blur-3xl"></div>
      </motion.div>

      {/* Quick Stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-2 lg:grid-cols-4 gap-4"
      >
        {quickStats.map((stat, index) => (
          <motion.div
            key={stat.label}
            whileHover={{ scale: 1.02, y: -2 }}
            className="bg-white rounded-2xl p-6 shadow-sm border border-gray-200 text-center"
          >
            <div className="text-3xl mb-2">{stat.icon}</div>
            <div className="text-2xl font-bold text-gray-900 mb-1">{stat.value}</div>
            <div className="text-sm text-gray-500">{stat.label}</div>
          </motion.div>
        ))}
      </motion.div>

      {/* Weather Widget */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="lg:hidden bg-gradient-accent rounded-2xl p-6 text-white"
      >
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <span className="text-2xl">{weatherData.icon}</span>
              <div>
                <div className="font-semibold text-lg">{weatherData.location}</div>
                <div className="text-sm opacity-75">{weatherData.condition}</div>
              </div>
            </div>
            <div className="text-3xl font-light">{weatherData.temperature}°C</div>
          </div>
          <div className="text-right">
            <div className="text-sm opacity-75">Humidity</div>
            <div className="font-semibold">{weatherData.humidity}%</div>
            <div className="text-sm opacity-75 mt-2">Wind</div>
            <div className="font-semibold">{weatherData.windSpeed} km/h</div>
          </div>
        </div>
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-white rounded-3xl p-8 shadow-sm border border-gray-200"
      >
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {quickActions.map((action, index) => (
            <motion.button
              key={action.title}
              whileHover={{ scale: 1.02, y: -2 }}
              whileTap={{ scale: 0.98 }}
              className="group bg-gradient-to-br from-gray-50 to-gray-100 hover:from-white hover:to-gray-50 rounded-2xl p-6 text-left transition-all duration-200 border border-gray-200 hover:border-gray-300 hover:shadow-md"
            >
              <div className="flex items-start space-x-4">
                <div className={`w-12 h-12 bg-gradient-to-br ${action.color} rounded-xl flex items-center justify-center text-2xl shadow-lg`}>
                  {action.icon}
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 mb-1 group-hover:text-gray-700">
                    {action.title}
                  </h3>
                  <p className="text-sm text-gray-500 group-hover:text-gray-600">
                    {action.description}
                  </p>
                </div>
              </div>
            </motion.button>
          ))}
        </div>
      </motion.div>

      {/* Recent Activity */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-white rounded-3xl p-8 shadow-sm border border-gray-200"
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Recent Activity</h2>
          <span className="text-sm text-gray-500">Today</span>
        </div>
        
        <div className="space-y-4">
          {recentActivity.map((activity, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 + index * 0.1 }}
              className="flex items-center space-x-4 p-4 rounded-xl hover:bg-gray-50 transition-colors cursor-pointer"
            >
              <div className="w-10 h-10 bg-gradient-primary rounded-xl flex items-center justify-center text-white">
                {activity.icon}
              </div>
              <div className="flex-1">
                <p className="font-medium text-gray-900">{activity.title}</p>
                <p className="text-sm text-gray-500">{activity.time}</p>
              </div>
              <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
            </motion.div>
          ))}
        </div>
        
        {recentActivity.length === 0 && (
          <div className="text-center py-8">
            <div className="text-6xl mb-4">✨</div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No recent activity</h3>
            <p className="text-gray-500">Start your wellness journey today!</p>
          </div>
        )}
      </motion.div>
      </div>
    </div>
  )
}
