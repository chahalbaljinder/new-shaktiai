'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Search, 
  FileText, 
  Clock, 
  CheckCircle, 
  Send, 
  Sparkles,
  FileCheck,
  Download,
  ArrowRight,
  Brain,
  BookOpen,
  Users,
  AlertCircle,
  Loader2
} from 'lucide-react'

interface PolicyQuery {
  id: string
  query: string
  category: string
  responseTime: string
  status: 'completed' | 'processing' | 'pending'
  response?: string
  sources?: Array<{
    document: string
    page: string
    relevance: number
  }>
  createdAt: string
}

interface ApplicationForm {
  applicationType: string
  status: string
  generatedText?: string
}

const TABS = [
  { id: 'ask', label: 'Ask Policy', icon: Search },
  { id: 'history', label: 'Query History', icon: Clock },
  { id: 'applications', label: 'Applications', icon: FileCheck },
  { id: 'resources', label: 'Resources', icon: BookOpen }
]

const POLICY_CATEGORIES = [
  { id: 'posh', label: 'POSH Act', icon: Users },
  { id: 'leave', label: 'Leave Policies', icon: FileText },
  { id: 'maternity', label: 'Maternity Benefits', icon: FileCheck },
  { id: 'transfer', label: 'Transfer Guidelines', icon: ArrowRight },
  { id: 'general', label: 'General Policies', icon: BookOpen }
]

const APPLICATION_TYPES = [
  { id: 'maternity-leave', label: 'Maternity Leave Application' },
  { id: 'ccl', label: 'Child Care Leave (CCL)' },
  { id: 'transfer', label: 'Transfer Request' },
  { id: 'grievance', label: 'Grievance Application' },
  { id: 'policy-clarification', label: 'Policy Clarification Request' }
]

export default function PolicyQueries() {
  const [activeTab, setActiveTab] = useState('ask')
  const [query, setQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('general')
  const [loading, setLoading] = useState(false)
  const [queries, setQueries] = useState<PolicyQuery[]>([])
  const [currentResponse, setCurrentResponse] = useState<PolicyQuery | null>(null)
  const [currentApplication, setCurrentApplication] = useState<ApplicationForm | null>(null)
  const [selectedAppType, setSelectedAppType] = useState('')
  const [appDetails, setAppDetails] = useState('')
  const [selectedQuery, setSelectedQuery] = useState<PolicyQuery | null>(null)
  const [showQueryModal, setShowQueryModal] = useState(false)

  // Format markdown text to HTML
  const formatMarkdown = (text: string) => {
    let formatted = text
    
    // Convert ## Heading to <h2>
    formatted = formatted.replace(/^## (.+)$/gm, '<h2 class="text-xl font-bold text-gray-900 dark:text-white mt-6 mb-3">$1</h2>')
    
    // Convert ### Heading to <h3>
    formatted = formatted.replace(/^### (.+)$/gm, '<h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200 mt-4 mb-2">$1</h3>')
    
    // Convert **bold** to <strong> with proper styling
    formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong style="font-weight: 700; color: inherit;">$1</strong>')
    
    // Convert numbered lists (1., 2., etc.)
    formatted = formatted.replace(/^\d+\.\s+(.+)$/gm, '<li class="ml-6">$1</li>')
    
    // Convert * bullet points to <li>
    formatted = formatted.replace(/^\*\s+(.+)$/gm, '<li class="ml-6">$1</li>')
    
    // Wrap consecutive <li> items in <ul> with better spacing
    formatted = formatted.replace(/(<li class="ml-6">.*?<\/li>\n?)+/g, '<ul class="list-disc space-y-2 my-4 ml-4">$&</ul>')
    
    // Add paragraph breaks with spacing
    formatted = formatted.replace(/\n\n/g, '</p><p class="mb-4 leading-relaxed">')
    formatted = '<p class="mb-4 leading-relaxed">' + formatted + '</p>'
    
    // Clean up empty paragraphs
    formatted = formatted.replace(/<p class="mb-4 leading-relaxed"><\/p>/g, '')
    formatted = formatted.replace(/<p class="mb-4 leading-relaxed">(<h[23])/g, '$1')
    formatted = formatted.replace(/(<\/h[23]>)<\/p>/g, '$1')
    formatted = formatted.replace(/<p class="mb-4 leading-relaxed">(<ul)/g, '$1')
    formatted = formatted.replace(/(<\/ul>)<\/p>/g, '$1')
    
    return formatted
  }

  // Load query history
  useEffect(() => {
    if (activeTab === 'history') {
      fetchQueryHistory()
    }
  }, [activeTab])

  const fetchQueryHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/policy-queries', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        // Transform snake_case to camelCase
        const transformedQueries = (data.queries || []).map((q: any) => ({
          id: q.id,
          query: q.query,
          category: q.category,
          response: q.response,
          status: q.status,
          responseTime: q.response_time || 'N/A',
          createdAt: q.created_at || new Date().toISOString()
        }))
        setQueries(transformedQueries)
      }
    } catch (error) {
      console.error('Error fetching query history:', error)
    }
  }

  const handleSubmitQuery = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setCurrentResponse(null)

    try {
      const response = await fetch('http://localhost:8000/api/policy-queries', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          query,
          category: selectedCategory
        })
      })

      if (response.ok) {
        const data = await response.json()
        // Transform response data
        const transformedQuery = {
          id: data.query.id,
          query: data.query.query,
          category: data.query.category,
          response: data.query.response,
          status: data.query.status,
          responseTime: data.query.response_time || 'N/A',
          createdAt: data.query.created_at || new Date().toISOString()
        }
        setCurrentResponse(transformedQuery)
        setQuery('')
        // Refresh history
        fetchQueryHistory()
      } else {
        const error = await response.json()
        alert(error.error || 'Failed to submit query')
      }
    } catch (error) {
      console.error('Error submitting query:', error)
      alert('Failed to submit query. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateApplication = async () => {
    if (!selectedAppType) {
      alert('Please select application type')
      return
    }

    setLoading(true)

    try {
      const response = await fetch('http://localhost:8000/api/generate-application', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          applicationType: selectedAppType,
          details: appDetails || 'Standard application request'
        })
      })

      if (response.ok) {
        const data = await response.json()
        setCurrentApplication({
          applicationType: selectedAppType,
          status: 'generated',
          generatedText: data.application
        })
        setSelectedAppType('')
        setAppDetails('')
      } else {
        const error = await response.json()
        alert(error.error || 'Failed to generate application')
      }
    } catch (error) {
      console.error('Error generating application:', error)
      alert('Failed to generate application. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const downloadApplication = (app: ApplicationForm) => {
    // Create a simple HTML document for Word compatibility
    const htmlContent = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>${APPLICATION_TYPES.find(t => t.id === app.applicationType)?.label || 'Application'}</title>
  <style>
    body { font-family: 'Times New Roman', serif; font-size: 12pt; line-height: 1.5; margin: 1in; }
    p { margin-bottom: 12pt; }
  </style>
</head>
<body>
  <pre style="font-family: 'Times New Roman', serif; white-space: pre-wrap;">${app.generatedText || ''}</pre>
</body>
</html>
    `
    const blob = new Blob([htmlContent], { type: 'application/vnd.ms-word' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${app.applicationType}-application.doc`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const openQueryModal = (query: PolicyQuery) => {
    setSelectedQuery(query)
    setShowQueryModal(true)
  }

  const closeQueryModal = () => {
    setShowQueryModal(false)
    setSelectedQuery(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center">
              <Brain className="text-white" size={24} />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Policy Queries</h1>
              <p className="text-gray-600 dark:text-gray-400">AI-powered policy assistance with APEX RAG system</p>
            </div>
          </div>
        </motion.div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 overflow-x-auto">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-blue-500 text-white shadow-lg'
                  : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
              }`}
            >
              <tab.icon size={18} />
              {tab.label}
            </button>
          ))}
        </div>

        <AnimatePresence mode="wait">
          {/* Ask Policy Tab */}
          {activeTab === 'ask' && (
            <motion.div
              key="ask"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-6"
            >
              {/* Category Selection */}
              <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Select Policy Category</h3>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                  {POLICY_CATEGORIES.map((cat) => (
                    <button
                      key={cat.id}
                      onClick={() => setSelectedCategory(cat.id)}
                      className={`flex flex-col items-center gap-2 p-4 rounded-lg transition-all ${
                        selectedCategory === cat.id
                          ? 'bg-blue-100 dark:bg-blue-900 border-2 border-blue-500'
                          : 'bg-gray-50 dark:bg-gray-700 border-2 border-transparent hover:border-gray-300 dark:hover:border-gray-600'
                      }`}
                    >
                      <cat.icon size={24} className={selectedCategory === cat.id ? 'text-blue-600 dark:text-blue-400' : 'text-gray-600 dark:text-gray-400'} />
                      <span className={`text-sm font-medium text-center ${selectedCategory === cat.id ? 'text-blue-700 dark:text-blue-300' : 'text-gray-700 dark:text-gray-300'}`}>
                        {cat.label}
                      </span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Query Input */}
              <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
                <form onSubmit={handleSubmitQuery} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Your Policy Question
                    </label>
                    <textarea
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      rows={4}
                      className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                      placeholder="e.g., What are the maternity leave entitlements for DRDO employees?"
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={loading || !query.trim()}
                    className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-blue-500 to-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-600 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                  >
                    {loading ? (
                      <>
                        <Loader2 size={20} className="animate-spin" />
                        Processing with APEX AI...
                      </>
                    ) : (
                      <>
                        <Send size={20} />
                        Submit Query
                      </>
                    )}
                  </button>
                </form>
              </div>

              {/* Current Response */}
              {currentResponse && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-700 rounded-xl p-6 shadow-lg"
                >
                  <div className="flex items-start gap-3 mb-4">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center flex-shrink-0">
                      <Sparkles className="text-white" size={20} />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">APEX Response</h3>
                      <div className="text-base text-gray-700 dark:text-gray-300">
                        <div dangerouslySetInnerHTML={{ __html: formatMarkdown(currentResponse.response || '') }} />
                      </div>
                    </div>
                  </div>

                  {/* Sources */}
                  {currentResponse.sources && currentResponse.sources.length > 0 && (
                    <div className="mt-6 pt-6 border-t border-blue-200 dark:border-gray-600">
                      <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">📚 Sources Referenced:</h4>
                      <div className="space-y-2">
                        {currentResponse.sources.map((source, idx) => (
                          <div key={idx} className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                            <FileText size={16} />
                            <span>{source.document} - {source.page}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </motion.div>
              )}
            </motion.div>
          )}

          {/* Query History Tab */}
          {activeTab === 'history' && (
            <motion.div
              key="history"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden"
            >
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Query History</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">Your past policy questions and answers</p>
              </div>
              
              <div className="divide-y divide-gray-200 dark:divide-gray-700">
                {queries.length === 0 ? (
                  <div className="p-12 text-center text-gray-500 dark:text-gray-400">
                    <Clock size={48} className="mx-auto mb-4 opacity-50" />
                    <p>No queries yet. Ask your first policy question!</p>
                  </div>
                ) : (
                  queries.map((q) => (
                    <div 
                      key={q.id} 
                      onClick={() => openQueryModal(q)}
                      className="p-6 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors cursor-pointer"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-2">{q.query}</h4>
                          <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${
                            q.category === 'posh' ? 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300' :
                            q.category === 'leave' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300' :
                            q.category === 'maternity' ? 'bg-pink-100 text-pink-700 dark:bg-pink-900 dark:text-pink-300' :
                            q.category === 'transfer' ? 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300' :
                            'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
                          }`}>
                            {q.category === 'posh' ? 'POSH Act' :
                             q.category === 'leave' ? 'Leave Policies' :
                             q.category === 'maternity' ? 'Maternity Benefits' :
                             q.category === 'transfer' ? 'Transfer Guidelines' :
                             'General Policies'}
                          </span>
                        </div>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          q.status === 'completed'
                            ? 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300'
                            : q.status === 'processing'
                            ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300'
                            : 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
                        }`}>
                          {q.status}
                        </span>
                      </div>
                      <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
                        <span className="flex items-center gap-1">
                          <Clock size={14} />
                          {q.responseTime}
                        </span>
                        <span>{new Date(q.createdAt).toLocaleString()}</span>
                      </div>
                      {q.response && (
                        <div className="mt-3 text-sm text-gray-700 dark:text-gray-300 line-clamp-3" dangerouslySetInnerHTML={{ __html: formatMarkdown(q.response.substring(0, 200) + '...') }} />
                      )}
                    </div>
                  ))
                )}
              </div>
            </motion.div>
          )}

          {/* Applications Tab */}
          {activeTab === 'applications' && (
            <motion.div
              key="applications"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-6"
            >
              {/* Generate New Application */}
              <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Generate Application</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Application Type
                    </label>
                    <select
                      value={selectedAppType}
                      onChange={(e) => setSelectedAppType(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                    >
                      <option value="">Select type...</option>
                      {APPLICATION_TYPES.map((type) => (
                        <option key={type.id} value={type.id}>{type.label}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Details <span className="text-gray-500 dark:text-gray-400 text-xs">(Optional)</span>
                    </label>
                    <textarea
                      value={appDetails}
                      onChange={(e) => setAppDetails(e.target.value)}
                      rows={4}
                      className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                      placeholder="Provide details like dates, reasons, etc. (Optional)"
                    />
                  </div>
                  <button
                    onClick={handleGenerateApplication}
                    disabled={loading}
                    className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-green-500 to-emerald-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-green-600 hover:to-emerald-700 disabled:opacity-50 transition-all"
                  >
                    {loading ? (
                      <>
                        <Loader2 size={20} className="animate-spin" />
                        Generating...
                      </>
                    ) : (
                      <>
                        <Sparkles size={20} />
                        Generate with AI
                      </>
                    )}
                  </button>
                </div>
              </div>

              {/* Current Generated Application */}
              {currentApplication && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden"
                >
                  <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Generated Application</h3>
                  </div>
                  <div className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h4 className="font-semibold text-gray-900 dark:text-white">
                          {APPLICATION_TYPES.find(t => t.id === currentApplication.applicationType)?.label}
                        </h4>
                        <span className="text-sm text-green-600 dark:text-green-400">Generated Successfully</span>
                      </div>
                      <button
                        onClick={() => downloadApplication(currentApplication)}
                        className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                      >
                        <Download size={16} />
                        Download
                      </button>
                    </div>
                    <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6">
                      <div className="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap font-sans leading-relaxed">
                        <div dangerouslySetInnerHTML={{ __html: formatMarkdown(currentApplication.generatedText || '') }} />
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}
            </motion.div>
          )}

          {/* Resources Tab */}
          {activeTab === 'resources' && (
            <motion.div
              key="resources"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg"
            >
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">Policy Resources</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  { title: 'POSH Act Guidelines', category: 'Legal', color: 'from-red-500 to-orange-500' },
                  { title: 'Maternity Benefit Act', category: 'Benefits', color: 'from-pink-500 to-rose-500' },
                  { title: 'Leave Policy Manual', category: 'HR', color: 'from-blue-500 to-indigo-500' },
                  { title: 'Transfer Guidelines', category: 'Administrative', color: 'from-green-500 to-emerald-500' },
                  { title: 'CCL Entitlements', category: 'Benefits', color: 'from-purple-500 to-violet-500' },
                  { title: 'Grievance Procedures', category: 'HR', color: 'from-yellow-500 to-amber-500' }
                ].map((resource, idx) => (
                  <div key={idx} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-lg transition-shadow">
                    <div className={`w-12 h-12 bg-gradient-to-br ${resource.color} rounded-lg flex items-center justify-center mb-3`}>
                      <FileText className="text-white" size={24} />
                    </div>
                    <h4 className="font-semibold text-gray-900 dark:text-white mb-1">{resource.title}</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">{resource.category}</p>
                    <button className="text-sm text-blue-600 dark:text-blue-400 hover:underline">
                      View Document →
                    </button>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Query Details Modal */}
        {showQueryModal && selectedQuery && (
          <div 
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
            onClick={closeQueryModal}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col"
            >
              {/* Modal Header */}
              <div className="p-6 border-b border-gray-200 dark:border-gray-700 flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
                      <Sparkles className="text-white" size={20} />
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">Query Details</h3>
                  </div>
                  <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400 mt-3">
                    <span className="flex items-center gap-1">
                      <Clock size={14} />
                      {selectedQuery.responseTime}
                    </span>
                    <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded-full text-xs font-medium">
                      {selectedQuery.category}
                    </span>
                    <span>{new Date(selectedQuery.createdAt).toLocaleString()}</span>
                  </div>
                </div>
                <button
                  onClick={closeQueryModal}
                  className="ml-4 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                >
                  <svg className="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              {/* Modal Body */}
              <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {/* Question Section */}
                <div className="bg-blue-50 dark:bg-gray-700 rounded-xl p-4">
                  <h4 className="text-sm font-semibold text-blue-900 dark:text-blue-300 mb-2">Question:</h4>
                  <p className="text-gray-800 dark:text-gray-200">{selectedQuery.query}</p>
                </div>

                {/* Answer Section */}
                {selectedQuery.response && (
                  <div className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-700 rounded-xl p-6">
                    <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                      <Brain size={18} className="text-blue-600 dark:text-blue-400" />
                      APEX Response:
                    </h4>
                    <div className="text-base text-gray-700 dark:text-gray-300">
                      <div dangerouslySetInnerHTML={{ __html: formatMarkdown(selectedQuery.response) }} />
                    </div>
                  </div>
                )}

                {/* Sources Section */}
                {selectedQuery.sources && selectedQuery.sources.length > 0 && (
                  <div className="bg-gray-50 dark:bg-gray-700 rounded-xl p-4">
                    <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 flex items-center gap-2">
                      <BookOpen size={18} />
                      Sources Referenced:
                    </h4>
                    <div className="space-y-2">
                      {selectedQuery.sources.map((source, idx) => (
                        <div key={idx} className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 bg-white dark:bg-gray-600 p-3 rounded-lg">
                          <FileText size={16} />
                          <span>{source.document} - {source.page}</span>
                          <span className="ml-auto text-xs px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded-full">
                            {Math.round(source.relevance * 100)}% relevant
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Modal Footer */}
              <div className="p-4 border-t border-gray-200 dark:border-gray-700 flex justify-end">
                <button
                  onClick={closeQueryModal}
                  className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors font-medium"
                >
                  Close
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </div>
    </div>
  )
}
