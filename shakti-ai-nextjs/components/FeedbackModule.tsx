'use client'

import { useState, useEffect } from 'react'
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
  X,
  AlertCircle
} from 'lucide-react'
import { feedbackAPI } from '@/lib/api'

interface FeedbackItem {
  id: string
  type: 'feedback' | 'complaint' | 'grievance' | 'suggestion'
  title: string
  description: string
  category: string
  status: 'submitted' | 'under-review' | 'in-progress' | 'resolved' | 'closed'
  priority: 'low' | 'medium' | 'high' | 'urgent' | 'critical'
  submittedBy: string
  designation: string
  establishment: string
  department?: string
  submittedAt: string
  lastUpdated: string
  responseText?: string
  trackingNumber?: string
  escalationLevel?: number
  assignedTo?: string
  attachments?: string[]
}

export default function FeedbackModule() {
  const [activeTab, setActiveTab] = useState<'submit' | 'my-feedback' | 'complaint-box' | 'analytics'>('submit')
  const [showSubmitForm, setShowSubmitForm] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [filterType, setFilterType] = useState<'all' | 'feedback' | 'complaint' | 'grievance' | 'suggestion'>('all')
  const [filterStatus, setFilterStatus] = useState<string>('all')
  const [selectedItem, setSelectedItem] = useState<FeedbackItem | null>(null)
  const [showTrackingModal, setShowTrackingModal] = useState(false)
  const [feedbackList, setFeedbackList] = useState<FeedbackItem[]>([])
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState({
    totalSubmitted: 0,
    underReview: 0,
    inProgress: 0,
    resolved: 0,
    avgResponseTime: '0 days',
    satisfactionRate: 0
  })

  // Form state
  const [formData, setFormData] = useState({
    type: 'feedback' as 'feedback' | 'complaint' | 'grievance' | 'suggestion',
    title: '',
    description: '',
    category: '',
    priority: 'medium' as 'low' | 'medium' | 'high' | 'urgent' | 'critical',
    isAnonymous: false,
    department: '',
    againstPerson: '',
    witnesses: ''
  })

  // Fetch feedback data on component mount
  useEffect(() => {
    if (activeTab === 'my-feedback' || activeTab === 'analytics') {
      fetchFeedbackData()
    }
  }, [activeTab])

  const fetchFeedbackData = async () => {
    try {
      setLoading(true)
      const data = await feedbackAPI.getAll({})
      
      // Transform API data to match component interface
      const transformed: FeedbackItem[] = data.map((item: any) => ({
        id: item.id ? `${item.type === 'complaint' ? 'COMP' : item.type === 'grievance' ? 'GR' : item.type === 'suggestion' ? 'SG' : 'FB'}${String(item.id).padStart(3, '0')}` : 'FB000',
        type: item.type || 'feedback',
        title: item.title || item.subject || 'No Subject',
        description: item.description || 'No Description',
        category: item.category || 'general',
        status: item.status || 'submitted',
        priority: item.priority || 'medium',
        submittedBy: item.user_name || item.submittedBy || 'Unknown User',
        designation: item.designation || 'N/A',
        establishment: item.establishment || 'N/A',
        department: item.department,
        submittedAt: item.created_at || item.submittedAt || new Date().toISOString(),
        lastUpdated: item.updated_at || item.updatedAt || new Date().toISOString(),
        responseText: item.response_text || item.responseText,
        trackingNumber: item.tracking_number,
        escalationLevel: item.escalation_level,
        assignedTo: item.assigned_to_name || item.assignedTo
      }))
      
      setFeedbackList(transformed)
      
      // Calculate stats from actual data
      setStats({
        totalSubmitted: transformed.length,
        underReview: transformed.filter(f => f.status === 'under-review').length,
        inProgress: transformed.filter(f => f.status === 'in-progress').length,
        resolved: transformed.filter(f => f.status === 'resolved').length,
        avgResponseTime: calculateAvgResponseTime(transformed),
        satisfactionRate: 0 // Calculate based on resolved items
      })
      
      setLoading(false)
    } catch (error) {
      console.error('Error fetching feedback:', error)
      setLoading(false)
    }
  }

  const calculateAvgResponseTime = (items: FeedbackItem[]): string => {
    const resolvedItems = items.filter(f => f.status === 'resolved')
    if (resolvedItems.length === 0) return '0 days'
    
    let totalDays = 0
    resolvedItems.forEach(item => {
      const submitted = new Date(item.submittedAt)
      const resolved = new Date(item.lastUpdated)
      const days = Math.floor((resolved.getTime() - submitted.getTime()) / (1000 * 60 * 60 * 24))
      totalDays += days
    })
    
    const avgDays = Math.round(totalDays / resolvedItems.length)
    return `${avgDays} day${avgDays !== 1 ? 's' : ''}`
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
      case 'complaint': return <AlertTriangle size={16} />
      case 'grievance': return <AlertTriangle size={16} />
      case 'suggestion': return <FileText size={16} />
      default: return <MessageSquare size={16} />
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      // Build enhanced description for complaints
      let enhancedDescription = formData.description;
      if (formData.type === 'complaint') {
        if (formData.department) enhancedDescription += `\n\nDepartment: ${formData.department}`;
        if (formData.againstPerson) enhancedDescription += `\nPerson(s) Involved: ${formData.againstPerson}`;
        if (formData.witnesses) enhancedDescription += `\nWitnesses: ${formData.witnesses}`;
      }
      
      // Submit to API - using user_id 3 as demo (DRDO Admin)
      const response = await feedbackAPI.submit({
        user_id: 3,
        type: formData.type,
        title: formData.title,
        description: enhancedDescription,
        category: formData.category,
        priority: formData.priority,
        is_anonymous: formData.isAnonymous
      })
      
      // Show success message with tracking number for complaints
      if (formData.type === 'complaint' && response.tracking_number) {
        alert(`✅ Complaint submitted successfully!\n\n🔢 Your Tracking Number: ${response.tracking_number}\n\n📧 This has been sent to your registered email.\n⏱️ Expected response time: Within 24 hours\n🔒 Your complaint is confidential and will be handled by the ICC.`)
      } else {
        alert('✅ ' + (response.message || 'Feedback submitted successfully!'))
      }
      
      setShowSubmitForm(false)
      setFormData({
        type: 'feedback',
        title: '',
        description: '',
        category: '',
        priority: 'medium',
        isAnonymous: false,
        department: '',
        againstPerson: '',
        witnesses: ''
      })
      
      // Refresh feedback list
      fetchFeedbackData()
    } catch (error) {
      console.error('Error submitting feedback:', error)
      alert('❌ Failed to submit. Please try again or contact support.')
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
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-2">
          <button
            onClick={() => setActiveTab('submit')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'submit'
                ? 'bg-brand-500 text-white'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            Submit Feedback
          </button>
          <button
            onClick={() => setActiveTab('complaint-box')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'complaint-box'
                ? 'bg-red-500 text-white'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            📋 Complaint Box
          </button>
          <button
            onClick={() => setActiveTab('my-feedback')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'my-feedback'
                ? 'bg-brand-500 text-white'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            My Submissions
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
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

      {/* Complaint Box Tab */}
      {activeTab === 'complaint-box' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Complaint Box Header */}
          <div className="bg-gradient-to-r from-red-500 to-orange-500 rounded-xl p-8 text-white">
            <h2 className="text-3xl font-bold mb-3">📋 Organization Complaint Box</h2>
            <p className="text-lg opacity-90 mb-4">
              File confidential complaints about workplace issues, harassment, discrimination, or policy violations
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
              <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4">
                <h3 className="font-semibold mb-1">🔒 Confidential</h3>
                <p className="text-sm opacity-90">Your identity is protected</p>
              </div>
              <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4">
                <h3 className="font-semibold mb-1">⚡ Fast Response</h3>
                <p className="text-sm opacity-90">Priority handling within 24hrs</p>
              </div>
              <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4">
                <h3 className="font-semibold mb-1">👁️ Track Status</h3>
                <p className="text-sm opacity-90">Monitor your complaint progress</p>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* File New Complaint */}
            <motion.div
              whileHover={{ scale: 1.02 }}
              onClick={() => {
                setFormData({ ...formData, type: 'complaint', priority: 'urgent' })
                setShowSubmitForm(true)
              }}
              className="bg-white dark:bg-gray-800 rounded-xl border-2 border-red-300 dark:border-red-700 p-6 cursor-pointer hover:border-red-500 hover:shadow-lg transition-all"
            >
              <div className="flex items-start gap-4">
                <div className="w-14 h-14 bg-red-100 dark:bg-red-500/20 rounded-xl flex items-center justify-center flex-shrink-0">
                  <AlertTriangle className="text-red-500" size={28} />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                    File a Complaint
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 text-sm mb-3">
                    Report harassment, discrimination, workplace safety, or any policy violations
                  </p>
                  <div className="flex flex-wrap gap-2">
                    <span className="px-2 py-1 bg-red-100 text-red-700 rounded text-xs font-medium">
                      Harassment
                    </span>
                    <span className="px-2 py-1 bg-orange-100 text-orange-700 rounded text-xs font-medium">
                      Discrimination
                    </span>
                    <span className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded text-xs font-medium">
                      Safety Issues
                    </span>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Track Complaint */}
            <motion.div
              whileHover={{ scale: 1.02 }}
              onClick={() => setShowTrackingModal(true)}
              className="bg-white dark:bg-gray-800 rounded-xl border-2 border-blue-300 dark:border-blue-700 p-6 cursor-pointer hover:border-blue-500 hover:shadow-lg transition-all"
            >
              <div className="flex items-start gap-4">
                <div className="w-14 h-14 bg-blue-100 dark:bg-blue-500/20 rounded-xl flex items-center justify-center flex-shrink-0">
                  <Search className="text-blue-500" size={28} />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                    Track Your Complaint
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 text-sm mb-3">
                    Enter your tracking number to check the status and updates on your complaint
                  </p>
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    Format: <span className="font-mono bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">COMP-XXXX-XXXX</span>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Complaint Categories */}
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
              What can you report?
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {[
                { title: 'Workplace Harassment', icon: '⚠️', desc: 'Sexual harassment, bullying, verbal abuse' },
                { title: 'Discrimination', icon: '🚫', desc: 'Gender, caste, religion, age discrimination' },
                { title: 'Safety Violations', icon: '🛡️', desc: 'Unsafe working conditions, security issues' },
                { title: 'Policy Violations', icon: '📋', desc: 'Breach of organizational policies' },
                { title: 'Ethical Concerns', icon: '⚖️', desc: 'Corruption, fraud, misconduct' },
                { title: 'Other Issues', icon: '📌', desc: 'Any other workplace concern' }
              ].map((category, index) => (
                <div key={index} className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-brand-500 transition-colors">
                  <div className="text-2xl mb-2">{category.icon}</div>
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-1">{category.title}</h4>
                  <p className="text-xs text-gray-600 dark:text-gray-400">{category.desc}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Important Information */}
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-6">
            <h3 className="text-lg font-bold text-blue-900 dark:text-blue-400 mb-3 flex items-center gap-2">
              <AlertCircle size={20} />
              Important Information
            </h3>
            <ul className="space-y-2 text-sm text-blue-800 dark:text-blue-300">
              <li className="flex items-start gap-2">
                <CheckCircle size={16} className="mt-0.5 flex-shrink-0" />
                <span>All complaints are treated with strict confidentiality</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle size={16} className="mt-0.5 flex-shrink-0" />
                <span>You can choose to remain anonymous</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle size={16} className="mt-0.5 flex-shrink-0" />
                <span>Complaints are reviewed by the Internal Complaints Committee (ICC)</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle size={16} className="mt-0.5 flex-shrink-0" />
                <span>You will receive a unique tracking number for status updates</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle size={16} className="mt-0.5 flex-shrink-0" />
                <span>False or malicious complaints may result in disciplinary action</span>
              </li>
            </ul>
          </div>
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
                  <option value="complaint">Complaint</option>
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
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-500 mx-auto mb-4"></div>
                <p className="text-gray-600 dark:text-gray-400">Loading your submissions...</p>
              </div>
            </div>
          ) : filteredFeedback.length === 0 ? (
            <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-12 text-center">
              <MessageSquare className="h-16 w-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                No submissions found
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                {searchQuery || filterType !== 'all' || filterStatus !== 'all' 
                  ? 'Try adjusting your filters or search query'
                  : 'You haven\'t submitted any feedback yet'}
              </p>
              {!searchQuery && filterType === 'all' && filterStatus === 'all' && (
                <button
                  onClick={() => setShowSubmitForm(true)}
                  className="px-6 py-2 bg-brand-500 text-white rounded-lg hover:bg-brand-600 transition-colors"
                >
                  Submit Your First Feedback
                </button>
              )}
            </div>
          ) : (
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
                      item.type === 'complaint' ? 'bg-red-100 text-red-600' :
                      item.type === 'grievance' ? 'bg-orange-100 text-orange-600' :
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
          )}
        </motion.div>
      )}

      {/* Analytics Tab */}
      {activeTab === 'analytics' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-500 mx-auto mb-4"></div>
                <p className="text-gray-600 dark:text-gray-400">Loading analytics...</p>
              </div>
            </div>
          ) : (
            <>
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
          </>
          )}
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
                <div className="grid grid-cols-4 gap-4">
                  {['feedback', 'complaint', 'grievance', 'suggestion'].map((type) => (
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
                  {formData.type === 'complaint' ? (
                    <>
                      <option value="harassment">Workplace Harassment</option>
                      <option value="discrimination">Discrimination</option>
                      <option value="safety-violation">Safety Violations</option>
                      <option value="policy-violation">Policy Violations</option>
                      <option value="ethical-concern">Ethical Concerns</option>
                      <option value="retaliation">Retaliation</option>
                      <option value="misconduct">Misconduct</option>
                      <option value="other">Other</option>
                    </>
                  ) : (
                    <>
                      <option value="system-performance">System Performance</option>
                      <option value="technical-issue">Technical Issue</option>
                      <option value="feature-request">Feature Request</option>
                      <option value="user-experience">User Experience</option>
                      <option value="security">Security</option>
                      <option value="other">Other</option>
                    </>
                  )}
                </select>
              </div>

              {/* Complaint-specific fields */}
              {formData.type === 'complaint' && (
                <>
                  {/* Department */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Department/Division
                    </label>
                    <input
                      type="text"
                      value={formData.department}
                      onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                      placeholder="Department where incident occurred"
                    />
                  </div>

                  {/* Against Person (Optional) */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Person(s) Involved (Optional)
                    </label>
                    <input
                      type="text"
                      value={formData.againstPerson}
                      onChange={(e) => setFormData({ ...formData, againstPerson: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                      placeholder="Name(s) or designation (if applicable)"
                    />
                  </div>

                  {/* Witnesses */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Witnesses (Optional)
                    </label>
                    <input
                      type="text"
                      value={formData.witnesses}
                      onChange={(e) => setFormData({ ...formData, witnesses: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white dark:bg-gray-900 text-gray-900 dark:text-white"
                      placeholder="Names of any witnesses"
                    />
                  </div>

                  {/* Important Notice for Complaints */}
                  <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                    <p className="text-sm text-red-800 dark:text-red-300">
                      <strong>Important:</strong> This complaint will be reviewed by the Internal Complaints Committee (ICC). 
                      Providing false information may result in disciplinary action. Your complaint will be handled confidentially.
                    </p>
                  </div>
                </>
              )}

              {/* Priority */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Priority
                </label>
                <div className="grid grid-cols-4 gap-4">
                  {(formData.type === 'complaint' ? ['low', 'medium', 'high', 'urgent'] : ['low', 'medium', 'high', 'critical']).map((priority) => (
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

      {/* Tracking Modal */}
      {showTrackingModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-white dark:bg-gray-800 rounded-xl max-w-md w-full"
          >
            <div className="p-6 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                Track Your Complaint
              </h2>
              <button
                onClick={() => setShowTrackingModal(false)}
                className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Enter Tracking Number
                </label>
                <input
                  type="text"
                  placeholder="COMP-XXXX-XXXX"
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent bg-white dark:bg-gray-900 text-gray-900 dark:text-white font-mono"
                />
              </div>

              <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                <p className="text-sm text-blue-800 dark:text-blue-300">
                  💡 You received a tracking number via email when you submitted your complaint. 
                  Check your registered email or the confirmation screen.
                </p>
              </div>

              <button
                onClick={() => {
                  alert('Tracking feature will search for your complaint');
                  setShowTrackingModal(false);
                }}
                className="w-full px-6 py-3 bg-brand-500 text-white rounded-lg hover:bg-brand-600 transition-colors flex items-center justify-center gap-2"
              >
                <Search size={20} />
                Track Status
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  )
}

