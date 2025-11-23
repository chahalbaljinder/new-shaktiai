'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  MessageSquare, 
  AlertTriangle, 
  ThumbsUp,
  Send,
  FileText,
  User,
  Mail,
  Building,
  CheckCircle,
  Clock,
  XCircle,
  Search,
  Filter,
  Plus,
  X
} from 'lucide-react'
import { feedbackAPI } from '@/lib/api'

interface FeedbackItem {
  id: string
  type: 'feedback' | 'grievance' | 'suggestion'
  title: string
  description: string
  category: string
  status: 'submitted' | 'under-review' | 'in-progress' | 'resolved' | 'closed'
  priority: 'low' | 'medium' | 'high' | 'critical'
  submittedBy: string
  designation: string
  establishment: string
  submittedAt: string
  lastUpdated: string
  responseText?: string
}

export default function FeedbackModule() {
  const [activeTab, setActiveTab] = useState<'submit' | 'my-feedback' | 'analytics'>('submit')
  const [showSubmitForm, setShowSubmitForm] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [filterType, setFilterType] = useState<'all' | 'feedback' | 'grievance' | 'suggestion'>('all')
  const [filterStatus, setFilterStatus] = useState<string>('all')

  // Form state
  const [formData, setFormData] = useState({
    type: 'feedback' as 'feedback' | 'grievance' | 'suggestion',
    title: '',
    description: '',
    category: '',
    priority: 'medium' as 'low' | 'medium' | 'high' | 'critical',
    isAnonymous: false
  })

  // Sample feedback data
  const feedbackList: FeedbackItem[] = [
    {
      id: 'FD001',
      type: 'feedback',
      title: 'APEX System - Excellent Response Quality',
      description: 'The APEX AI agents provide very accurate and helpful responses for POSH policy queries.',
      category: 'System Performance',
      status: 'resolved',
      priority: 'low',
      submittedBy: 'Dr. Priya Sharma',
      designation: 'Scientist-E',
      establishment: 'DRDO HQ, Delhi',
      submittedAt: '2025-11-18T10:30:00',
      lastUpdated: '2025-11-20T14:20:00',
      responseText: 'Thank you for your positive feedback! We are glad the system is meeting your expectations.'
    },
    {
      id: 'GR001',
      type: 'grievance',
      title: 'Voice Input Not Working on Secure Workstations',
      description: 'Unable to use voice input feature on lab computers due to security restrictions.',
      category: 'Technical Issue',
      status: 'in-progress',
      priority: 'high',
      submittedBy: 'Dr. Anita Desai',
      designation: 'Scientist-D',
      establishment: 'DRDL, Hyderabad',
      submittedAt: '2025-11-20T09:15:00',
      lastUpdated: '2025-11-21T16:30:00',
      responseText: 'IT Security Team is working on enabling voice input for classified networks.'
    },
    {
      id: 'SG001',
      type: 'suggestion',
      title: 'Add Support for Regional Languages',
      description: 'Request to add Hindi and other regional language support for better accessibility.',
      category: 'Feature Request',
      status: 'under-review',
      priority: 'medium',
      submittedBy: 'Sh. Rajesh Kumar',
      designation: 'Admin Officer',
      establishment: 'ADE, Bangalore',
      submittedAt: '2025-11-21T14:00:00',
      lastUpdated: '2025-11-22T09:00:00'
    }
  ]

  // Statistics
  const stats = {
    totalSubmitted: 47,
    underReview: 12,
    inProgress: 8,
    resolved: 23,
    avgResponseTime: '2.3 days',
    satisfactionRate: 94
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'submitted': return 'bg-blue-100 text-blue-700 border-blue-200'
      case 'under-review': return 'bg-yellow-100 text-yellow-700 border-yellow-200'
      case 'in-progress': return 'bg-purple-100 text-purple-700 border-purple-200'
      case 'resolved': return 'bg-green-100 text-green-700 border-green-200'
      case 'closed': return 'bg-gray-100 text-gray-700 border-gray-200'
      default: return 'bg-gray-100 text-gray-700 border-gray-200'
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'bg-red-500 text-white'
      case 'high': return 'bg-orange-500 text-white'
      case 'medium': return 'bg-yellow-500 text-white'
      case 'low': return 'bg-green-500 text-white'
      default: return 'bg-gray-500 text-white'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'feedback': return <ThumbsUp size={16} />
      case 'grievance': return <AlertTriangle size={16} />
      case 'suggestion': return <FileText size={16} />
      default: return <MessageSquare size={16} />
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      // Submit to API - using user_id 3 as demo (DRDO Admin)
      await feedbackAPI.submit({
        user_id: 3,
        type: formData.type,
        title: formData.title,
        description: formData.description,
        category: formData.category,
        priority: formData.priority,
        is_anonymous: formData.isAnonymous
      })
      
      alert('Feedback submitted successfully!')
      setShowSubmitForm(false)
      setFormData({
        type: 'feedback',
        title: '',
        description: '',
        category: '',
        priority: 'medium',
        isAnonymous: false
      })
    } catch (error) {
      console.error('Error submitting feedback:', error)
      alert('Failed to submit feedback. Please try again.')
    }
  }

  const filteredFeedback = feedbackList.filter(item => {
    const matchesType = filterType === 'all' || item.type === filterType
    const matchesStatus = filterStatus === 'all' || item.status === filterStatus
    const matchesSearch = item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          item.description.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesType && matchesStatus && matchesSearch
  })

  return (
    <div className="min-h-screen space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            DRDO Feedback & Grievance Module
          </h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            Submit feedback, report grievances, and track your submissions
          </p>
        </div>
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => setShowSubmitForm(true)}
          className="flex items-center gap-2 px-6 py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600 transition-colors shadow-md"
        >
          <Plus size={20} />
          Submit New
        </motion.button>
      </div>

      {/* Tabs */}
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-2">
        <div className="flex gap-2">
          <button
            onClick={() => setActiveTab('submit')}
            className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'submit'
                ? 'bg-brand-500 text-white'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            Submit Feedback
          </button>
          <button
            onClick={() => setActiveTab('my-feedback')}
            className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'my-feedback'
                ? 'bg-brand-500 text-white'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            My Submissions
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            className={`flex-1 px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'analytics'
                ? 'bg-brand-500 text-white'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            Analytics
          </button>
        </div>
      </div>

      {/* Submit Tab */}
      {activeTab === 'submit' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-1 lg:grid-cols-3 gap-6"
        >
          {/* Feedback Card */}
          <motion.div
            whileHover={{ y: -4 }}
            onClick={() => {
              setFormData({ ...formData, type: 'feedback' })
              setShowSubmitForm(true)
            }}
            className="bg-white dark:bg-gray-800 rounded-xl border-2 border-brand-200 dark:border-brand-800 p-6 cursor-pointer hover:border-brand-500 transition-colors"
          >
            <div className="w-12 h-12 bg-brand-100 dark:bg-brand-500/20 rounded-lg flex items-center justify-center mb-4">
              <ThumbsUp className="text-brand-500" size={24} />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
              Share Feedback
            </h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Share your positive experience or suggestions for improvement with the APEX system
            </p>
          </motion.div>

          {/* Grievance Card */}
          <motion.div
            whileHover={{ y: -4 }}
            onClick={() => {
              setFormData({ ...formData, type: 'grievance' })
              setShowSubmitForm(true)
            }}
            className="bg-white dark:bg-gray-800 rounded-xl border-2 border-red-200 dark:border-red-800 p-6 cursor-pointer hover:border-red-500 transition-colors"
          >
            <div className="w-12 h-12 bg-red-100 dark:bg-red-500/20 rounded-lg flex items-center justify-center mb-4">
              <AlertTriangle className="text-red-500" size={24} />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
              Report Grievance
            </h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Report any issues, concerns, or problems you're facing with the system or services
            </p>
          </motion.div>

          {/* Suggestion Card */}
          <motion.div
            whileHover={{ y: -4 }}
            onClick={() => {
              setFormData({ ...formData, type: 'suggestion' })
              setShowSubmitForm(true)
            }}
            className="bg-white dark:bg-gray-800 rounded-xl border-2 border-purple-200 dark:border-purple-800 p-6 cursor-pointer hover:border-purple-500 transition-colors"
          >
            <div className="w-12 h-12 bg-purple-100 dark:bg-purple-500/20 rounded-lg flex items-center justify-center mb-4">
              <FileText className="text-purple-500" size={24} />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
              Suggest Feature
            </h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Suggest new features or enhancements to make the system more useful and efficient
            </p>
          </motion.div>
        </motion.div>
      )}

      {/* My Submissions Tab */}
      {activeTab === 'my-feedback' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Filters */}
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-4">
            <div className="flex flex-col lg:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                  <input
                    type="text"
                    placeholder="Search your submissions..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                  />
                </div>
              </div>
              
              <div className="flex gap-2">
                <select
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value as any)}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                >
                  <option value="all">All Types</option>
                  <option value="feedback">Feedback</option>
                  <option value="grievance">Grievance</option>
                  <option value="suggestion">Suggestion</option>
                </select>

                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                >
                  <option value="all">All Status</option>
                  <option value="submitted">Submitted</option>
                  <option value="under-review">Under Review</option>
                  <option value="in-progress">In Progress</option>
                  <option value="resolved">Resolved</option>
                  <option value="closed">Closed</option>
                </select>
              </div>
            </div>
          </div>

          {/* Feedback List */}
          <div className="space-y-4">
            {filteredFeedback.map((item) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-start gap-4">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                      item.type === 'feedback' ? 'bg-brand-100 text-brand-500' :
                      item.type === 'grievance' ? 'bg-red-100 text-red-500' :
                      'bg-purple-100 text-purple-500'
                    }`}>
                      {getTypeIcon(item.type)}
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-1">
                        {item.title}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {item.description}
                      </p>
                      <div className="flex items-center gap-4 mt-3">
                        <span className="text-xs text-gray-500">
                          ID: {item.id}
                        </span>
                        <span className="text-xs text-gray-500">
                          {item.category}
                        </span>
                        <span className="text-xs text-gray-500">
                          Submitted: {new Date(item.submittedAt).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="flex flex-col items-end gap-2">
                    <span className={`inline-flex px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(item.status)}`}>
                      {item.status.replace('-', ' ').toUpperCase()}
                    </span>
                    <span className={`inline-flex px-2 py-1 rounded text-xs font-medium ${getPriorityColor(item.priority)}`}>
                      {item.priority.toUpperCase()}
                    </span>
                  </div>
                </div>

                {item.responseText && (
                  <div className="mt-4 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
                    <div className="flex items-start gap-2">
                      <CheckCircle className="text-green-500 mt-0.5" size={16} />
                      <div>
                        <p className="text-sm font-medium text-green-800 dark:text-green-400 mb-1">
                          Response from APEX Team:
                        </p>
                        <p className="text-sm text-green-700 dark:text-green-300">
                          {item.responseText}
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Analytics Tab */}
      {activeTab === 'analytics' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Submitted</h3>
                <MessageSquare className="text-brand-500" size={20} />
              </div>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.totalSubmitted}</p>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Under Review</h3>
                <Clock className="text-yellow-500" size={20} />
              </div>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.underReview}</p>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">In Progress</h3>
                <AlertTriangle className="text-purple-500" size={20} />
              </div>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.inProgress}</p>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Resolved</h3>
                <CheckCircle className="text-green-500" size={20} />
              </div>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.resolved}</p>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Avg Response Time</h3>
                <Clock className="text-brand-500" size={20} />
              </div>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.avgResponseTime}</p>
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Satisfaction Rate</h3>
                <ThumbsUp className="text-green-500" size={20} />
              </div>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.satisfactionRate}%</p>
            </div>
          </div>

          {/* Performance Chart Placeholder */}
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
              Feedback Trends (Last 30 Days)
            </h3>
            <div className="h-64 flex items-center justify-center text-gray-400">
              Chart will be displayed here
            </div>
          </div>
        </motion.div>
      )}

      {/* Submit Form Modal */}
      {showSubmitForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-white dark:bg-gray-800 rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
          >
            <div className="p-6 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between sticky top-0 bg-white dark:bg-gray-800 z-10">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                Submit {formData.type.charAt(0).toUpperCase() + formData.type.slice(1)}
              </h2>
              <button
                onClick={() => setShowSubmitForm(false)}
                className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-6">
              {/* Type Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Type
                </label>
                <div className="grid grid-cols-3 gap-4">
                  {['feedback', 'grievance', 'suggestion'].map((type) => (
                    <button
                      key={type}
                      type="button"
                      onClick={() => setFormData({ ...formData, type: type as any })}
                      className={`p-4 rounded-lg border-2 transition-colors ${
                        formData.type === type
                          ? 'border-brand-500 bg-brand-50 dark:bg-brand-900/20'
                          : 'border-gray-200 dark:border-gray-700 hover:border-brand-300'
                      }`}
                    >
                      <span className="text-sm font-medium capitalize">{type}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Title */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Title *
                </label>
                <input
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                  placeholder="Brief title for your submission"
                />
              </div>

              {/* Description */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Description *
                </label>
                <textarea
                  required
                  rows={6}
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white dark:bg-gray-900 text-gray-900 dark:text-white resize-none"
                  placeholder="Provide detailed information..."
                />
              </div>

              {/* Category */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Category *
                </label>
                <select
                  required
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                >
                  <option value="">Select category</option>
                  <option value="system-performance">System Performance</option>
                  <option value="technical-issue">Technical Issue</option>
                  <option value="feature-request">Feature Request</option>
                  <option value="user-experience">User Experience</option>
                  <option value="security">Security</option>
                  <option value="other">Other</option>
                </select>
              </div>

              {/* Priority */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Priority
                </label>
                <div className="grid grid-cols-4 gap-4">
                  {['low', 'medium', 'high', 'critical'].map((priority) => (
                    <button
                      key={priority}
                      type="button"
                      onClick={() => setFormData({ ...formData, priority: priority as any })}
                      className={`p-3 rounded-lg border-2 transition-colors ${
                        formData.priority === priority
                          ? 'border-brand-500 bg-brand-50 dark:bg-brand-900/20'
                          : 'border-gray-200 dark:border-gray-700 hover:border-brand-300'
                      }`}
                    >
                      <span className="text-sm font-medium capitalize">{priority}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Anonymous */}
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  id="anonymous"
                  checked={formData.isAnonymous}
                  onChange={(e) => setFormData({ ...formData, isAnonymous: e.target.checked })}
                  className="w-4 h-4 text-brand-500 border-gray-300 rounded focus:ring-brand-500"
                />
                <label htmlFor="anonymous" className="text-sm text-gray-700 dark:text-gray-300">
                  Submit anonymously
                </label>
              </div>

              {/* Submit Button */}
              <div className="flex gap-4">
                <button
                  type="button"
                  onClick={() => setShowSubmitForm(false)}
                  className="flex-1 px-6 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-6 py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600 transition-colors flex items-center justify-center gap-2"
                >
                  <Send size={20} />
                  Submit
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      )}
    </div>
  )
}
