'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  MessageSquare, 
  AlertTriangle, 
  CheckCircle, 
  Clock,
  ArrowUp,
  ArrowDown,
  TrendingUp,
  Search,
  Filter,
  Download,
  Eye,
  MoreVertical
} from 'lucide-react'

interface Feedback {
  id: string
  type: 'feedback' | 'complaint'
  subject: string
  description: string
  status: 'pending' | 'in-progress' | 'resolved' | 'closed'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  category: string
  submittedBy: string
  submittedAt: string
  updatedAt: string
  assignedTo?: string
}

export default function FeedbackDashboard() {
  const [feedbacks, setFeedbacks] = useState<Feedback[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'feedback' | 'complaint'>('all')
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    fetchFeedbacks()
  }, [])

  const fetchFeedbacks = async () => {
    try {
      // Simulated data - replace with actual API call
      const mockData: Feedback[] = [
        {
          id: 'FB001',
          type: 'feedback',
          subject: 'APEX System - Excellent Policy Guidance',
          description: 'APEX agents provide accurate and detailed policy information for POSH compliance.',
          status: 'resolved',
          priority: 'low',
          category: 'System Performance',
          submittedBy: 'Dr. Priya Sharma (Scientist-E)',
          submittedAt: '2025-11-20T10:30:00',
          updatedAt: '2025-11-21T14:20:00',
          assignedTo: 'APEX Support Team'
        },
        {
          id: 'GR001',
          type: 'complaint',
          subject: 'Voice Input Not Working on Lab Computers',
          description: 'Voice recording feature fails on secure lab workstations.',
          status: 'in-progress',
          priority: 'high',
          category: 'Technical Issue',
          submittedBy: 'Dr. Anita Desai (Scientist-D)',
          submittedAt: '2025-11-21T09:15:00',
          updatedAt: '2025-11-21T15:30:00',
          assignedTo: 'IT Security Team'
        },
        {
          id: 'GR002',
          type: 'complaint',
          subject: 'SSO Login Issues',
          description: 'Unable to login through DRDO SSO after recent security update.',
          status: 'pending',
          priority: 'urgent',
          category: 'Authentication',
          submittedBy: 'Dr. Meera Reddy (Scientist-F)',
          submittedAt: '2025-11-22T08:00:00',
          updatedAt: '2025-11-22T08:00:00'
        },
        {
          id: 'FB002',
          type: 'feedback',
          subject: 'Improved Knowledge Base Access',
          description: 'Easy access to all HR policies and regulations. Very helpful for administrative queries.',
          status: 'resolved',
          priority: 'low',
          category: 'User Experience',
          submittedBy: 'Sh. Rajesh Kumar (Admin Officer)',
          submittedAt: '2025-11-19T16:45:00',
          updatedAt: '2025-11-20T10:00:00',
          assignedTo: 'APEX Admin Team'
        },
        {
          id: 'GR003',
          type: 'complaint',
          subject: 'Slow Response During Peak Hours',
          description: 'APEX agents take longer to respond between 10 AM - 12 PM when most personnel are active.',
          status: 'in-progress',
          priority: 'medium',
          category: 'Performance',
          submittedBy: 'Dr. Ritu Verma (Scientist-C)',
          submittedAt: '2025-11-21T11:20:00',
          updatedAt: '2025-11-21T16:00:00',
          assignedTo: 'Infrastructure Team'
        }
      ]
      setFeedbacks(mockData)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching feedbacks:', error)
      setLoading(false)
    }
  }

  const stats = {
    total: feedbacks.length,
    feedback: feedbacks.filter(f => f.type === 'feedback').length,
    complaints: feedbacks.filter(f => f.type === 'complaint').length,
    pending: feedbacks.filter(f => f.status === 'pending').length,
    inProgress: feedbacks.filter(f => f.status === 'in-progress').length,
    resolved: feedbacks.filter(f => f.status === 'resolved').length,
    urgent: feedbacks.filter(f => f.priority === 'urgent').length
  }

  const filteredFeedbacks = feedbacks.filter(f => {
    const matchesType = filter === 'all' || f.type === filter
    const matchesStatus = statusFilter === 'all' || f.status === statusFilter
    const matchesSearch = f.subject.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          f.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          f.submittedBy.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesType && matchesStatus && matchesSearch
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'bg-yellow-50 text-yellow-700 border-yellow-200'
      case 'in-progress': return 'bg-blue-50 text-blue-700 border-blue-200'
      case 'resolved': return 'bg-green-50 text-green-700 border-green-200'
      case 'closed': return 'bg-gray-50 text-gray-700 border-gray-200'
      default: return 'bg-gray-50 text-gray-700 border-gray-200'
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'bg-red-100 text-red-700'
      case 'high': return 'bg-orange-100 text-orange-700'
      case 'medium': return 'bg-yellow-100 text-yellow-700'
      case 'low': return 'bg-gray-100 text-gray-700'
      default: return 'bg-gray-100 text-gray-700'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl text-brand-500 font-semibold">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            DRDO Grievance & Feedback Portal
          </h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            Internal feedback and grievance management system for DRDO personnel
          </p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-brand-500 text-white rounded-lg hover:bg-brand-600 transition-colors">
          <Download size={20} />
          Export Report
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400 font-medium">Total Items</p>
              <h3 className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{stats.total}</h3>
              <div className="flex items-center mt-2 text-sm text-green-600">
                <ArrowUp size={16} />
                <span className="ml-1">+8.2% from last week</span>
              </div>
            </div>
            <div className="w-12 h-12 bg-brand-100 dark:bg-brand-500/20 rounded-lg flex items-center justify-center">
              <MessageSquare className="text-brand-500" size={24} />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400 font-medium">Complaints</p>
              <h3 className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{stats.complaints}</h3>
              <div className="flex items-center mt-2 text-sm text-red-600">
                <ArrowUp size={16} />
                <span className="ml-1">{stats.urgent} urgent</span>
              </div>
            </div>
            <div className="w-12 h-12 bg-red-100 dark:bg-red-500/20 rounded-lg flex items-center justify-center">
              <AlertTriangle className="text-red-500" size={24} />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400 font-medium">In Progress</p>
              <h3 className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{stats.inProgress}</h3>
              <div className="flex items-center mt-2 text-sm text-blue-600">
                <Clock size={16} />
                <span className="ml-1">Being handled</span>
              </div>
            </div>
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-500/20 rounded-lg flex items-center justify-center">
              <Clock className="text-blue-500" size={24} />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400 font-medium">Resolved</p>
              <h3 className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{stats.resolved}</h3>
              <div className="flex items-center mt-2 text-sm text-green-600">
                <CheckCircle size={16} />
                <span className="ml-1">Successfully closed</span>
              </div>
            </div>
            <div className="w-12 h-12 bg-green-100 dark:bg-green-500/20 rounded-lg flex items-center justify-center">
              <CheckCircle className="text-green-500" size={24} />
            </div>
          </div>
        </motion.div>
      </div>

      {/* Filters */}
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Search by subject, description, or user..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
              />
            </div>
          </div>
          
          <div className="flex gap-2">
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value as any)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
            >
              <option value="all">All Types</option>
              <option value="feedback">Feedback Only</option>
              <option value="complaint">Complaints Only</option>
            </select>

            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
            >
              <option value="all">All Status</option>
              <option value="pending">Pending</option>
              <option value="in-progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="closed">Closed</option>
            </select>
          </div>
        </div>
      </div>

      {/* Feedback List */}
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                  ID
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                  Subject
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                  Submitted By
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                  Priority
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-4 text-right text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {filteredFeedbacks.map((feedback) => (
                <motion.tr
                  key={feedback.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="hover:bg-gray-50 dark:hover:bg-gray-900 transition-colors"
                >
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                    {feedback.id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      feedback.type === 'complaint' 
                        ? 'bg-red-100 text-red-700 dark:bg-red-500/20 dark:text-red-400' 
                        : 'bg-blue-100 text-blue-700 dark:bg-blue-500/20 dark:text-blue-400'
                    }`}>
                      {feedback.type === 'complaint' ? <AlertTriangle size={12} className="mr-1" /> : <MessageSquare size={12} className="mr-1" />}
                      {feedback.type}
                    </span>
                  </td>
                  <td className="px-6 py-4 max-w-xs">
                    <div className="text-sm font-medium text-gray-900 dark:text-white truncate">
                      {feedback.subject}
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400 truncate">
                      {feedback.category}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700 dark:text-gray-300">
                    {feedback.submittedBy}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(feedback.priority)}`}>
                      {feedback.priority}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium border ${getStatusColor(feedback.status)}`}>
                      {feedback.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {new Date(feedback.submittedAt).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button className="text-brand-500 hover:text-brand-700 dark:hover:text-brand-400 mr-3">
                      <Eye size={18} />
                    </button>
                    <button className="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">
                      <MoreVertical size={18} />
                    </button>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredFeedbacks.length === 0 && (
          <div className="text-center py-12">
            <MessageSquare className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">No items found</h3>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
              Try adjusting your search or filter criteria
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
