'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  User, 
  Bell, 
  Palette, 
  Shield, 
  Download, 
  RotateCcw,
  Globe,
  Moon,
  Sun,
  Volume2,
  VolumeX,
  Lock,
  Key
} from 'lucide-react'

interface SettingsProps {
  // Add props as needed
}

export default function Settings({}: SettingsProps) {
  const [profile, setProfile] = useState({
    displayName: 'Sarah Johnson',
    email: 'sarah@example.com',
    ageRange: '25-30',
    language: 'english',
    location: 'New Delhi, India'
  })

  const [appearance, setAppearance] = useState({
    theme: 'auto',
    colorScheme: 'warm',
    fontSize: 'medium'
  })

  const [notifications, setNotifications] = useState({
    expertResponses: true,
    wishReminders: true,
    weeklyCheckins: true,
    communityUpdates: false,
    emergencyAlerts: true,
    voiceConfirmations: true
  })

  const [privacy, setPrivacy] = useState({
    autoLockTime: '5',
    encryptionLevel: 'maximum',
    dataRetention: '1-year'
  })

  const handleProfileUpdate = (field: string, value: string) => {
    setProfile(prev => ({ ...prev, [field]: value }))
  }

  const handleAppearanceUpdate = (field: string, value: string) => {
    setAppearance(prev => ({ ...prev, [field]: value }))
  }

  const handleNotificationToggle = (field: string) => {
    setNotifications(prev => ({ ...prev, [field]: !prev[field as keyof typeof prev] }))
  }

  const handlePrivacyUpdate = (field: string, value: string) => {
    setPrivacy(prev => ({ ...prev, [field]: value }))
  }

  return (
    <div className="p-6 lg:p-8 max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-primary rounded-3xl p-8 text-white"
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl lg:text-4xl font-bold mb-2">Settings & Preferences</h1>
            <p className="text-lg opacity-90">Customize your SHAKTI-AI experience</p>
          </div>
          <div className="hidden lg:flex items-center space-x-4">
            <div className="bg-white/20 rounded-full px-4 py-2">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-emerald-400 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium">All settings saved</span>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Profile Settings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-3xl p-8 shadow-sm border border-gray-200"
        >
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-white">
              <User size={24} />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Profile Settings</h2>
          </div>

          <div className="space-y-6">
            <div>
              <label htmlFor="displayName" className="block text-sm font-medium text-gray-700 mb-2">
                Display Name
              </label>
              <input
                id="displayName"
                type="text"
                value={profile.displayName}
                onChange={(e) => handleProfileUpdate('displayName', e.target.value)}
                className="shakti-input"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                value={profile.email}
                onChange={(e) => handleProfileUpdate('email', e.target.value)}
                className="shakti-input"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="ageRange" className="block text-sm font-medium text-gray-700 mb-2">
                  Age Range
                </label>
                <select
                  id="ageRange"
                  value={profile.ageRange}
                  onChange={(e) => handleProfileUpdate('ageRange', e.target.value)}
                  className="shakti-input"
                >
                  <option value="18-25">18-25</option>
                  <option value="25-30">25-30</option>
                  <option value="30-35">30-35</option>
                  <option value="35-45">35-45</option>
                  <option value="45-55">45-55</option>
                  <option value="55+">55+</option>
                </select>
              </div>

              <div>
                <label htmlFor="language" className="block text-sm font-medium text-gray-700 mb-2">
                  Preferred Language
                </label>
                <select
                  id="language"
                  value={profile.language}
                  onChange={(e) => handleProfileUpdate('language', e.target.value)}
                  className="shakti-input"
                >
                  <option value="english">English</option>
                  <option value="hindi">Hindi</option>
                  <option value="bengali">Bengali</option>
                  <option value="tamil">Tamil</option>
                  <option value="telugu">Telugu</option>
                </select>
              </div>
            </div>

            <div>
              <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
                Location
              </label>
              <input
                id="location"
                type="text"
                value={profile.location}
                onChange={(e) => handleProfileUpdate('location', e.target.value)}
                className="shakti-input"
                placeholder="City, State, Country"
              />
            </div>

            <button className="shakti-button w-full">
              💾 Save Profile
            </button>
          </div>
        </motion.div>

        {/* Appearance Settings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-3xl p-8 shadow-sm border border-gray-200"
        >
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl flex items-center justify-center text-white">
              <Palette size={24} />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Appearance</h2>
          </div>

          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-4">Theme</label>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { value: 'light', label: 'Light', icon: Sun },
                  { value: 'dark', label: 'Dark', icon: Moon },
                  { value: 'auto', label: 'Auto', icon: Globe }
                ].map(({ value, label, icon: Icon }) => (
                  <button
                    key={value}
                    onClick={() => handleAppearanceUpdate('theme', value)}
                    className={`p-4 rounded-xl border-2 transition-all duration-200 ${
                      appearance.theme === value
                        ? 'border-primary-500 bg-primary-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <Icon size={20} className="mx-auto mb-2" />
                    <span className="text-sm font-medium">{label}</span>
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label htmlFor="colorScheme" className="block text-sm font-medium text-gray-700 mb-2">
                Color Scheme
              </label>
              <select
                id="colorScheme"
                value={appearance.colorScheme}
                onChange={(e) => handleAppearanceUpdate('colorScheme', e.target.value)}
                className="shakti-input"
              >
                <option value="warm">Warm</option>
                <option value="cool">Cool</option>
                <option value="neutral">Neutral</option>
                <option value="vibrant">Vibrant</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-4">Font Size</label>
              <div className="flex items-center space-x-4">
                <span className="text-sm">Small</span>
                <input
                  type="range"
                  min="small"
                  max="large"
                  value={appearance.fontSize}
                  onChange={(e) => handleAppearanceUpdate('fontSize', e.target.value)}
                  className="flex-1"
                />
                <span className="text-sm">Large</span>
              </div>
              <div className="mt-2 text-center">
                <span className="text-sm text-gray-500 capitalize">{appearance.fontSize}</span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Notifications */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-3xl p-8 shadow-sm border border-gray-200"
        >
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-12 h-12 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl flex items-center justify-center text-white">
              <Bell size={24} />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Notifications</h2>
          </div>

          <div className="space-y-4">
            {[
              { key: 'expertResponses', label: 'Expert responses', description: 'Get notified when AI experts respond' },
              { key: 'wishReminders', label: 'Wish reminders', description: 'Periodic reminders about your goals' },
              { key: 'weeklyCheckins', label: 'Weekly check-ins', description: 'Weekly wellness check-in prompts' },
              { key: 'communityUpdates', label: 'Community updates', description: 'Updates from the SHAKTI-AI community' },
              { key: 'emergencyAlerts', label: 'Emergency alerts', description: 'Important safety and emergency notifications' },
              { key: 'voiceConfirmations', label: 'Voice input confirmations', description: 'Audio feedback for voice interactions' }
            ].map(({ key, label, description }) => (
              <div key={key} className="flex items-center justify-between p-4 rounded-xl bg-gray-50">
                <div className="flex-1">
                  <div className="font-medium text-gray-900">{label}</div>
                  <div className="text-sm text-gray-500">{description}</div>
                </div>
                <button
                  onClick={() => handleNotificationToggle(key)}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    notifications[key as keyof typeof notifications]
                      ? 'bg-primary-500'
                      : 'bg-gray-300'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      notifications[key as keyof typeof notifications]
                        ? 'translate-x-6'
                        : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Privacy & Security */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-3xl p-8 shadow-sm border border-gray-200"
        >
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-12 h-12 bg-gradient-to-br from-red-500 to-pink-600 rounded-xl flex items-center justify-center text-white">
              <Shield size={24} />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Privacy & Security</h2>
          </div>

          <div className="space-y-6">
            <div>
              <label htmlFor="autoLock" className="block text-sm font-medium text-gray-700 mb-2">
                Auto-lock Vault
              </label>
              <select
                id="autoLock"
                value={privacy.autoLockTime}
                onChange={(e) => handlePrivacyUpdate('autoLockTime', e.target.value)}
                className="shakti-input"
              >
                <option value="1">1 minute</option>
                <option value="5">5 minutes</option>
                <option value="15">15 minutes</option>
                <option value="30">30 minutes</option>
                <option value="60">1 hour</option>
                <option value="never">Never</option>
              </select>
            </div>

            <div>
              <label htmlFor="encryption" className="block text-sm font-medium text-gray-700 mb-2">
                Encryption Level
              </label>
              <select
                id="encryption"
                value={privacy.encryptionLevel}
                onChange={(e) => handlePrivacyUpdate('encryptionLevel', e.target.value)}
                className="shakti-input"
              >
                <option value="standard">Standard</option>
                <option value="high">High</option>
                <option value="maximum">Maximum</option>
              </select>
            </div>

            <div>
              <label htmlFor="dataRetention" className="block text-sm font-medium text-gray-700 mb-2">
                Data Retention
              </label>
              <select
                id="dataRetention"
                value={privacy.dataRetention}
                onChange={(e) => handlePrivacyUpdate('dataRetention', e.target.value)}
                className="shakti-input"
              >
                <option value="3-months">3 months</option>
                <option value="6-months">6 months</option>
                <option value="1-year">1 year</option>
                <option value="2-years">2 years</option>
                <option value="indefinite">Indefinite</option>
              </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <button className="shakti-button-secondary flex items-center justify-center space-x-2">
                <Key size={16} />
                <span>Change Password</span>
              </button>
              <button className="shakti-button-secondary flex items-center justify-center space-x-2">
                <Download size={16} />
                <span>Export Data</span>
              </button>
              <button className="bg-red-50 text-red-700 border-2 border-red-200 rounded-xl px-4 py-3 font-semibold hover:bg-red-100 transition-colors flex items-center justify-center space-x-2">
                <RotateCcw size={16} />
                <span>Reset</span>
              </button>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Additional Settings */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="bg-white rounded-3xl p-8 shadow-sm border border-gray-200"
      >
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Additional Options</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <button className="p-6 rounded-2xl bg-blue-50 hover:bg-blue-100 transition-colors text-left">
            <div className="text-2xl mb-2">🔄</div>
            <div className="font-semibold text-gray-900 mb-1">Sync Data</div>
            <div className="text-sm text-gray-600">Synchronize across devices</div>
          </button>
          
          <button className="p-6 rounded-2xl bg-green-50 hover:bg-green-100 transition-colors text-left">
            <div className="text-2xl mb-2">📊</div>
            <div className="font-semibold text-gray-900 mb-1">Analytics</div>
            <div className="text-sm text-gray-600">View usage statistics</div>
          </button>
          
          <button className="p-6 rounded-2xl bg-purple-50 hover:bg-purple-100 transition-colors text-left">
            <div className="text-2xl mb-2">🎯</div>
            <div className="font-semibold text-gray-900 mb-1">Goals</div>
            <div className="text-sm text-gray-600">Manage your objectives</div>
          </button>
          
          <button className="p-6 rounded-2xl bg-orange-50 hover:bg-orange-100 transition-colors text-left">
            <div className="text-2xl mb-2">📱</div>
            <div className="font-semibold text-gray-900 mb-1">Install App</div>
            <div className="text-sm text-gray-600">Add to home screen</div>
          </button>
        </div>
      </motion.div>
    </div>
  )
}
