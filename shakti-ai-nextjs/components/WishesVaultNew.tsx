'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useWishes, useCreateWish, useUpdateWish, useDeleteWish, useShareWish } from '@/lib/api/hooks'
import { Wish } from '@/lib/api/client'
import { toast } from 'sonner'
import { 
  Plus, 
  Lock, 
  Share, 
  Edit, 
  Trash2, 
  Search, 
  Filter,
  Heart,
  Star,
  Calendar,
  Tag,
  Shield,
  Eye,
  EyeOff,
  Loader2,
  Mail,
  MessageCircle,
  X
} from 'lucide-react'

export default function WishesVault() {
  const { data: wishesData, isLoading: wishesLoading, error: wishesError } = useWishes()
  const createWishMutation = useCreateWish()
  const updateWishMutation = useUpdateWish()
  const deleteWishMutation = useDeleteWish()
  const shareWishMutation = useShareWish()

  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingWish, setEditingWish] = useState<Wish | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [selectedPriority, setSelectedPriority] = useState('All')
  const [shareModalOpen, setShareModalOpen] = useState(false)
  const [shareWish, setShareWish] = useState<Wish | null>(null)

  // Form state
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    category: 'personal',
    priority: 'medium' as 'low' | 'medium' | 'high',
    reminder_date: '',
  })

  // Share form state
  const [shareData, setShareData] = useState({
    method: 'email' as 'email' | 'whatsapp',
    recipient: '',
    senderName: ''
  })

  const wishes = wishesData?.wishes || []

  // Filter wishes based on search and filters
  const filteredWishes = wishes.filter((wish: Wish) => {
    const matchesSearch = wish.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         wish.content.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = selectedCategory === 'All' || wish.category === selectedCategory
    const matchesPriority = selectedPriority === 'All' || wish.priority === selectedPriority

    return matchesSearch && matchesCategory && matchesPriority
  })

  const categories = ['All', ...Array.from(new Set(wishes.map((w: Wish) => w.category).filter(Boolean)))]
  const priorities = ['All', 'low', 'medium', 'high']

  const getPriorityColor = (priority?: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'low': return 'text-green-600 bg-green-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const resetForm = () => {
    setFormData({
      title: '',
      content: '',
      category: 'personal',
      priority: 'medium',
      reminder_date: '',
    })
    setEditingWish(null)
  }

  const openEditModal = (wish: Wish) => {
    setEditingWish(wish)
    setFormData({
      title: wish.title,
      content: wish.content,
      category: wish.category || 'personal',
      priority: (wish.priority as 'low' | 'medium' | 'high') || 'medium',
      reminder_date: wish.reminder_date || '',
    })
    setIsModalOpen(true)
  }

  const handleCreateOrUpdate = async () => {
    if (!formData.title.trim() || !formData.content.trim()) {
      toast.error('Please fill in all required fields')
      return
    }

    try {
      if (editingWish) {
        // Update existing wish
        await updateWishMutation.mutateAsync({
          wishId: editingWish.id!,
          updates: formData
        })
      } else {
        // Create new wish
        await createWishMutation.mutateAsync(formData)
      }

      setIsModalOpen(false)
      resetForm()
    } catch (error) {
      console.error('Failed to save wish:', error)
    }
  }

  const handleDeleteWish = async (wishId: number) => {
    if (!confirm('Are you sure you want to delete this wish?')) return
    
    try {
      await deleteWishMutation.mutateAsync(wishId)
    } catch (error) {
      console.error('Failed to delete wish:', error)
    }
  }

  const openShareModal = (wish: Wish) => {
    setShareWish(wish)
    setShareModalOpen(true)
  }

  const handleShareWish = async () => {
    if (!shareWish || !shareData.recipient.trim()) {
      toast.error('Please enter a recipient')
      return
    }

    try {
      await shareWishMutation.mutateAsync({
        wishId: shareWish.id!,
        method: shareData.method,
        recipient: shareData.recipient,
        senderName: shareData.senderName || 'SHAKTI-AI User'
      })
      
      setShareModalOpen(false)
      setShareData({ method: 'email', recipient: '', senderName: '' })
    } catch (error) {
      console.error('Failed to share wish:', error)
    }
  }

  if (wishesLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-indigo-50 p-6 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-purple-600" />
      </div>
    )
  }

  if (wishesError) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-indigo-50 p-6 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-2">Failed to load wishes</p>
          <button 
            onClick={() => window.location.reload()} 
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-indigo-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Wishes Vault</h1>
          <p className="text-gray-600">Your secure space for dreams, goals, and aspirations</p>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                placeholder="Search wishes..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>
            
            <div className="flex gap-4">
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
              >
                {categories.map(category => (
                  <option key={category} value={category}>{category}</option>
                ))}
              </select>
              
              <select
                value={selectedPriority}
                onChange={(e) => setSelectedPriority(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
              >
                {priorities.map(priority => (
                  <option key={priority} value={priority}>
                    {priority === 'All' ? 'All Priorities' : priority.charAt(0).toUpperCase() + priority.slice(1)}
                  </option>
                ))}
              </select>
              
              <button
                onClick={() => setIsModalOpen(true)}
                className="flex items-center gap-2 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors"
              >
                <Plus className="h-5 w-5" />
                Add Wish
              </button>
            </div>
          </div>
        </div>

        {/* Wishes Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <AnimatePresence>
            {filteredWishes.map((wish: Wish, index: number) => (
              <motion.div
                key={wish.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 overflow-hidden"
              >
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
                      {wish.title}
                    </h3>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(wish.priority)}`}>
                      {wish.priority || 'medium'}
                    </span>
                  </div>
                  
                  <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                    {wish.content}
                  </p>
                  
                  <div className="flex items-center justify-between text-xs text-gray-500 mb-4">
                    <span>{wish.category || 'personal'}</span>
                    <span>{wish.created_at ? new Date(wish.created_at).toLocaleDateString() : 'Unknown'}</span>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => openEditModal(wish)}
                      className="flex items-center gap-1 text-blue-600 hover:text-blue-700 text-sm"
                    >
                      <Edit className="h-4 w-4" />
                      Edit
                    </button>
                    <button
                      onClick={() => openShareModal(wish)}
                      className="flex items-center gap-1 text-green-600 hover:text-green-700 text-sm"
                    >
                      <Share className="h-4 w-4" />
                      Share
                    </button>
                    <button
                      onClick={() => handleDeleteWish(wish.id!)}
                      className="flex items-center gap-1 text-red-600 hover:text-red-700 text-sm"
                    >
                      <Trash2 className="h-4 w-4" />
                      Delete
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>

        {filteredWishes.length === 0 && (
          <div className="text-center py-12">
            <Heart className="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-600 mb-2">No wishes found</h3>
            <p className="text-gray-500">Start by creating your first wish!</p>
          </div>
        )}

        {/* Create/Edit Modal */}
        <AnimatePresence>
          {isModalOpen && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className="bg-white rounded-xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
              >
                <div className="p-6">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-2xl font-bold text-gray-900">
                      {editingWish ? 'Edit Wish' : 'Create New Wish'}
                    </h2>
                    <button
                      onClick={() => {
                        setIsModalOpen(false)
                        resetForm()
                      }}
                      className="text-gray-500 hover:text-gray-700"
                    >
                      <X className="h-6 w-6" />
                    </button>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Title *
                      </label>
                      <input
                        type="text"
                        value={formData.title}
                        onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                        placeholder="What is your wish?"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Description *
                      </label>
                      <textarea
                        value={formData.content}
                        onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                        rows={4}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                        placeholder="Describe your wish in detail..."
                      />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Category
                        </label>
                        <select
                          value={formData.category}
                          onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                        >
                          <option value="personal">Personal</option>
                          <option value="career">Career</option>
                          <option value="education">Education</option>
                          <option value="health">Health</option>
                          <option value="travel">Travel</option>
                          <option value="relationships">Relationships</option>
                          <option value="other">Other</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Priority
                        </label>
                        <select
                          value={formData.priority}
                          onChange={(e) => setFormData({ ...formData, priority: e.target.value as 'low' | 'medium' | 'high' })}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                        >
                          <option value="low">Low</option>
                          <option value="medium">Medium</option>
                          <option value="high">High</option>
                        </select>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Reminder Date (Optional)
                      </label>
                      <input
                        type="date"
                        value={formData.reminder_date}
                        onChange={(e) => setFormData({ ...formData, reminder_date: e.target.value })}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                      />
                    </div>
                  </div>

                  <div className="flex gap-4 mt-6">
                    <button
                      onClick={() => {
                        setIsModalOpen(false)
                        resetForm()
                      }}
                      className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={handleCreateOrUpdate}
                      disabled={createWishMutation.isPending || updateWishMutation.isPending}
                      className="flex-1 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                    >
                      {(createWishMutation.isPending || updateWishMutation.isPending) && (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      )}
                      {editingWish ? 'Update Wish' : 'Create Wish'}
                    </button>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Share Modal */}
        <AnimatePresence>
          {shareModalOpen && shareWish && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className="bg-white rounded-xl shadow-2xl w-full max-w-md"
              >
                <div className="p-6">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-bold text-gray-900">Share Wish</h2>
                    <button
                      onClick={() => setShareModalOpen(false)}
                      className="text-gray-500 hover:text-gray-700"
                    >
                      <X className="h-6 w-6" />
                    </button>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Share via
                      </label>
                      <div className="flex gap-4">
                        <button
                          onClick={() => setShareData({ ...shareData, method: 'email' })}
                          className={`flex items-center gap-2 px-4 py-2 rounded-lg border ${
                            shareData.method === 'email' 
                              ? 'border-purple-500 bg-purple-50 text-purple-700' 
                              : 'border-gray-300 text-gray-700'
                          }`}
                        >
                          <Mail className="h-4 w-4" />
                          Email
                        </button>
                        <button
                          onClick={() => setShareData({ ...shareData, method: 'whatsapp' })}
                          className={`flex items-center gap-2 px-4 py-2 rounded-lg border ${
                            shareData.method === 'whatsapp' 
                              ? 'border-purple-500 bg-purple-50 text-purple-700' 
                              : 'border-gray-300 text-gray-700'
                          }`}
                        >
                          <MessageCircle className="h-4 w-4" />
                          WhatsApp
                        </button>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        {shareData.method === 'email' ? 'Email Address' : 'Phone Number'}
                      </label>
                      <input
                        type={shareData.method === 'email' ? 'email' : 'tel'}
                        value={shareData.recipient}
                        onChange={(e) => setShareData({ ...shareData, recipient: e.target.value })}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                        placeholder={shareData.method === 'email' ? 'Enter email address' : 'Enter phone number'}
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Your Name (Optional)
                      </label>
                      <input
                        type="text"
                        value={shareData.senderName}
                        onChange={(e) => setShareData({ ...shareData, senderName: e.target.value })}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                        placeholder="Your name"
                      />
                    </div>
                  </div>

                  <div className="flex gap-4 mt-6">
                    <button
                      onClick={() => setShareModalOpen(false)}
                      className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={handleShareWish}
                      disabled={shareWishMutation.isPending}
                      className="flex-1 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                    >
                      {shareWishMutation.isPending && (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      )}
                      Share Wish
                    </button>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
