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
import { feedbackAPI } from '@/lib/api'

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
  const [stats, setStats] = useState<any>(null)
  const [selectedFeedback, setSelectedFeedback] = useState<Feedback | null>(null)
  const [showViewModal, setShowViewModal] = useState(false)
  const [showActionsMenu, setShowActionsMenu] = useState<string | null>(null)
  const [showStatusModal, setShowStatusModal] = useState(false)
  const [newStatus, setNewStatus] = useState('')
  const [responseText, setResponseText] = useState('')
  const [updating, setUpdating] = useState(false)

  useEffect(() => {
    fetchFeedbacks()
    fetchStats()
  }, [filter, statusFilter, searchQuery])

  const fetchFeedbacks = async () => {
    try {
      setLoading(true)
      const filters: any = {}
      if (filter !== 'all') filters.type = filter
      if (statusFilter !== 'all') filters.status = statusFilter
      if (searchQuery) filters.search = searchQuery

      const data = await feedbackAPI.getAll(filters)
      
      // Transform API data to match component interface
      const transformedData: Feedback[] = data.map((item: any) => ({
        id: item.id ? `FB${String(item.id).padStart(3, '0')}` : 'FB000',
        type: item.type || 'feedback',
        subject: item.title || item.subject || 'No Subject',
        description: item.description || 'No Description',
        status: item.status || 'pending',
        priority: item.priority || 'medium',
        category: item.category || 'general',
        submittedBy: item.user_name || item.submittedBy || 'Unknown User',
        submittedAt: item.created_at || item.submittedAt || new Date().toISOString(),
        updatedAt: item.updated_at || item.updatedAt || new Date().toISOString(),
        assignedTo: item.assigned_to_name || item.assignedTo || undefined
      }))
      
      setFeedbacks(transformedData)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching feedbacks:', error)
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const data = await feedbackAPI.getStats()
      setStats(data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const displayStats = stats ? {
    total: stats.total,
    feedback: feedbacks.filter(f => f.type === 'feedback').length,
    complaints: feedbacks.filter(f => f.type === 'complaint').length,
    pending: stats.under_review || 0,
    inProgress: stats.in_progress || 0,
    resolved: stats.resolved || 0,
    urgent: stats.urgent || 0
  } : {
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
    const matchesSearch = !searchQuery || 
                          (f.subject || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
                          (f.description || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
                          (f.submittedBy || '').toLowerCase().includes(searchQuery.toLowerCase())
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
              <h3 className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{displayStats.total}</h3>
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
              <h3 className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{displayStats.complaints}</h3>
              <div className="flex items-center mt-2 text-sm text-red-600">
                <ArrowUp size={16} />
                <span className="ml-1">{displayStats.urgent} urgent</span>
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
              <h3 className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{displayStats.inProgress}</h3>
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
              <h3 className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{displayStats.resolved}</h3>
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
                    <div className="flex items-center justify-end gap-2">
                      <button 
                        onClick={() => {
                          setSelectedFeedback(feedback)
                          setShowViewModal(true)
                        }}
                        className="text-brand-500 hover:text-brand-700 dark:hover:text-brand-400"
                        title="View Details"
                      >
                        <Eye size={18} />
                      </button>
                      <button
                        onClick={() => {
                          setSelectedFeedback(feedback)
                          setNewStatus(feedback.status)
                          setResponseText('')
                          setShowStatusModal(true)
                        }}
                        className="px-3 py-1 bg-brand-500 text-white rounded hover:bg-brand-600 transition-colors text-xs font-medium"
                        title="Update Status"
                      >
                        Update Status
                      </button>
                    </div>
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

      {/* View Details Modal */}
      {showViewModal && selectedFeedback && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 overflow-y-auto">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-white dark:bg-gray-800 rounded-xl max-w-2xl w-full my-auto"
          >
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  {selectedFeedback.type === 'complaint' ? 'Complaint' : 'Feedback'} Details
                </h2>
                <button
                  onClick={() => setShowViewModal(false)}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  ✕
                </button>
              </div>
            </div>

            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                  ID
                </label>
                <p className="text-gray-900 dark:text-white font-mono">{selectedFeedback.id}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                  Subject
                </label>
                <p className="text-gray-900 dark:text-white font-semibold">{selectedFeedback.subject}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                  Description
                </label>
                <p className="text-gray-900 dark:text-white whitespace-pre-wrap">{selectedFeedback.description}</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Type
                  </label>
                  <span className={`inline-flex px-3 py-1 rounded-full text-xs font-medium ${
                    selectedFeedback.type === 'complaint' 
                      ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                      : 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
                  }`}>
                    {selectedFeedback.type.toUpperCase()}
                  </span>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Priority
                  </label>
                  <span className={`inline-flex px-3 py-1 rounded-full text-xs font-medium ${
                    selectedFeedback.priority === 'urgent' || selectedFeedback.priority === 'high'
                      ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                      : selectedFeedback.priority === 'medium'
                      ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400'
                      : 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                  }`}>
                    {selectedFeedback.priority.toUpperCase()}
                  </span>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Status
                  </label>
                  <span className={`inline-flex px-3 py-1 rounded-full text-xs font-medium border ${
                    selectedFeedback.status === 'resolved'
                      ? 'bg-green-50 text-green-700 border-green-200 dark:bg-green-900/20 dark:text-green-400 dark:border-green-800'
                      : selectedFeedback.status === 'in-progress'
                      ? 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-900/20 dark:text-blue-400 dark:border-blue-800'
                      : 'bg-yellow-50 text-yellow-700 border-yellow-200 dark:bg-yellow-900/20 dark:text-yellow-400 dark:border-yellow-800'
                  }`}>
                    {selectedFeedback.status.replace('-', ' ').toUpperCase()}
                  </span>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Category
                  </label>
                  <p className="text-gray-900 dark:text-white">{selectedFeedback.category}</p>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                  Submitted By
                </label>
                <p className="text-gray-900 dark:text-white">{selectedFeedback.submittedBy}</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Submitted At
                  </label>
                  <p className="text-gray-900 dark:text-white">{new Date(selectedFeedback.submittedAt).toLocaleString()}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Last Updated
                  </label>
                  <p className="text-gray-900 dark:text-white">{new Date(selectedFeedback.updatedAt).toLocaleString()}</p>
                </div>
              </div>

              {selectedFeedback.assignedTo && (
                <div>
                  <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                    Assigned To
                  </label>
                  <p className="text-gray-900 dark:text-white">{selectedFeedback.assignedTo}</p>
                </div>
              )}
            </div>

            <div className="p-6 border-t border-gray-200 dark:border-gray-700 flex justify-end">
              <button
                onClick={() => setShowViewModal(false)}
                className="px-6 py-2 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
              >
                Close
              </button>
            </div>
          </motion.div>
        </div>
      )}

      {/* Update Status Modal */}
      {showStatusModal && selectedFeedback && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 overflow-y-auto">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-white dark:bg-gray-800 rounded-xl max-w-lg w-full my-auto"
          >
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                  Update Status
                </h2>
                <button
                  onClick={() => setShowStatusModal(false)}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  ✕
                </button>
              </div>
            </div>

            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Feedback ID
                </label>
                <p className="text-gray-900 dark:text-white font-mono">{selectedFeedback.id}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Subject
                </label>
                <p className="text-gray-900 dark:text-white">{selectedFeedback.subject}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Current Status
                </label>
                <span className={`inline-flex px-3 py-1 rounded-full text-xs font-medium border ${
                  selectedFeedback.status === 'resolved'
                    ? 'bg-green-50 text-green-700 border-green-200 dark:bg-green-900/20 dark:text-green-400 dark:border-green-800'
                    : selectedFeedback.status === 'in-progress'
                    ? 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-900/20 dark:text-blue-400 dark:border-blue-800'
                    : 'bg-yellow-50 text-yellow-700 border-yellow-200 dark:bg-yellow-900/20 dark:text-yellow-400 dark:border-yellow-800'
                }`}>
                  {selectedFeedback.status.replace('-', ' ').toUpperCase()}
                </span>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  New Status *
                </label>
                <select
                  value={newStatus}
                  onChange={(e) => setNewStatus(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                >
                  <option value="pending">Pending</option>
                  <option value="under-review">Under Review</option>
                  <option value="in-progress">In Progress</option>
                  <option value="resolved">Resolved</option>
                  <option value="closed">Closed</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Response / Comments (Optional)
                </label>
                <textarea
                  value={responseText}
                  onChange={(e) => setResponseText(e.target.value)}
                  rows={4}
                  placeholder="Add your response or comments here..."
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white dark:bg-gray-900 text-gray-900 dark:text-white resize-none"
                />
              </div>
            </div>

            <div className="p-6 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-3">
              <button
                onClick={() => setShowStatusModal(false)}
                disabled={updating}
                className="px-6 py-2 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={async () => {
                  setUpdating(true)
                  try {
                    const feedbackId = selectedFeedback.id.replace('FB', '').replace(/^0+/, '')
                    const response = await fetch(`http://localhost:8000/api/feedback/${feedbackId}`, {
                      method: 'PUT',
                      headers: {
                        'Content-Type': 'application/json',
                      },
                      body: JSON.stringify({
                        status: newStatus,
                        response_text: responseText || undefined
                      })
                    })
                    
                    if (response.ok) {
                      // Update the local state immediately
                      setFeedbacks(prevFeedbacks => 
                        prevFeedbacks.map(f => 
                          f.id === selectedFeedback.id 
                            ? { ...f, status: newStatus as any }
                            : f
                        )
                      )
                      setShowStatusModal(false)
                      setSelectedFeedback(null)
                      // Also refresh from server to get any other updates
                      fetchFeedbacks()
                      alert('Status updated successfully!')
                    } else {
                      const errorData = await response.json()
                      alert(`Failed to update status: ${errorData.error || 'Unknown error'}`)
                    }
                  } catch (error) {
                    console.error('Error updating status:', error)
                    alert('Failed to update status')
                  } finally {
                    setUpdating(false)
                  }
                }}
                disabled={updating || !newStatus}
                className="px-6 py-2 bg-brand-500 text-white rounded-lg hover:bg-brand-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {updating ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent" />
                    Updating...
                  </>
                ) : (
                  'Update Status'
                )}
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  )
}
