'use client'

import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Mic, MicOff, Bot, Clock, Loader2 } from 'lucide-react'
import { useAppStore } from '@/lib/store'
import { useAgents, useChatWithAgent, useSpeechToText, useDirectSpeechToText } from '@/lib/api/hooks'
import { toast } from 'sonner'
import MarkdownRenderer from './MarkdownRenderer'

interface Agent {
  id: string
  name: string
  role: string
  expertise: string
  icon: string
  specialty: string
  available: boolean
}

interface ChatMessage {
  id: string
  content: string
  role: 'user' | 'agent'
  agentName?: string
  timestamp: Date
  sources?: string[]
  citations?: any[]
}

const agents: Agent[] = [
  {
    id: 'athena',
    name: 'Athena',
    role: 'Policy & Procedure Guide',
    expertise: 'Government policies, POSH Act, Legal procedures',
    icon: '⚖️',
    specialty: 'Navigate complex government policies and procedures',
    available: true
  },
  {
    id: 'asha',
    name: 'Asha',
    role: 'Wellness & Support Companion',
    expertise: 'Emotional wellness, Work-life balance, Confidential support',
    icon: '🌸',
    specialty: 'Emotional support and wellness guidance',
    available: true
  },
  {
    id: 'scribe',
    name: 'Scribe',
    role: 'Documentation & Workflow Expert',
    expertise: 'Form generation, Document automation, Process guidance',
    icon: '📋',
    specialty: 'Document generation and administrative processes',
    available: true
  }
]

const agentMapping: { [key: string]: string } = {
  'athena': 'legal-guide',
  'asha': 'wellness', 
  'scribe': 'documentation'
}

export default function KnowledgeBase() {
  const { selectedAgents, setSelectedAgents } = useAppStore()
  const { data: agentsData, isLoading: agentsLoading } = useAgents()
  const chatMutation = useChatWithAgent()
  const speechToTextMutation = useSpeechToText()
  const directSpeechMutation = useDirectSpeechToText()
  
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      content: 'Welcome to Project APEX! I\'m here to support women scientists in government organizations with policy guidance, wellness support, and documentation help. Select the experts you\'d like to consult with, and let\'s start the conversation.',
      role: 'agent',
      agentName: 'APEX Team',
      timestamp: new Date(),
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [voiceActive, setVoiceActive] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null)
  const [recordedChunks, setRecordedChunks] = useState<Blob[]>([])
  const [useDirectMicrophone, setUseDirectMicrophone] = useState(true) // Prefer direct method like Streamlit
  const [speechRecognition, setSpeechRecognition] = useState<any>(null)
  const [browserSpeechSupported, setBrowserSpeechSupported] = useState(false)
  const [useBrowserSpeech, setUseBrowserSpeech] = useState(false) // Option to use browser's native speech recognition
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Initialize browser speech recognition if available
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
      if (SpeechRecognition) {
        setBrowserSpeechSupported(true)
        const recognition = new SpeechRecognition()
        recognition.continuous = false
        recognition.interimResults = false
        recognition.lang = 'en-US'
        recognition.maxAlternatives = 1
        
        recognition.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript
          if (transcript.trim()) {
            setInputValue(prev => prev + (prev ? ' ' : '') + transcript.trim())
            toast.success('Voice input transcribed successfully')
          }
        }
        
        recognition.onerror = (event: any) => {
          console.error('Speech recognition error:', event.error)
          if (event.error === 'not-allowed') {
            toast.error('Microphone access denied. Please enable microphone permissions.')
          } else if (event.error === 'no-speech') {
            toast.error('No speech detected. Please try again.')
          } else {
            toast.error('Speech recognition failed. Please try again.')
          }
          setVoiceActive(false)
        }
        
        recognition.onend = () => {
          setVoiceActive(false)
        }
        
        setSpeechRecognition(recognition)
      }
    }
  }, [])

  // Cleanup recording on unmount
  useEffect(() => {
    return () => {
      if (mediaRecorder && isRecording) {
        mediaRecorder.stop()
      }
    }
  }, [mediaRecorder, isRecording])

  // Voice recording functionality
  const startRecording = async () => {
    // Check for browser support
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      toast.error('Voice input is not supported in this browser')
      setVoiceActive(false)
      return
    }

    if (!window.MediaRecorder) {
      toast.error('Voice recording is not supported in this browser')
      setVoiceActive(false)
      return
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
          sampleRate: 16000
        } 
      })
      
      // Try to use a compatible format for speech recognition
      let mimeType = ''
      let fileExtension = '.wav'
      
      // Check for supported formats in order of preference for speech recognition
      // Prefer formats that work with SpeechRecognition library without ffmpeg
      const preferredFormats = [
        'audio/wav',           // Best for speech recognition, no conversion needed
        'audio/webm;codecs=pcm', // PCM in WebM container, might work directly
        'audio/ogg;codecs=vorbis', // OGG Vorbis, pydub can handle without ffmpeg
        'audio/mpeg',          // MP3, pydub can handle without ffmpeg  
        'audio/webm;codecs=opus', // Opus codec, needs ffmpeg
        'audio/mp4',           // MP4, needs ffmpeg
        'audio/webm',          // Generic WebM, needs ffmpeg
        'audio/ogg'            // Generic OGG
      ]
      
      for (const format of preferredFormats) {
        if (MediaRecorder.isTypeSupported(format)) {
          mimeType = format
          if (format.includes('wav')) fileExtension = '.wav'
          else if (format.includes('mp4')) fileExtension = '.mp4'
          else if (format.includes('mpeg')) fileExtension = '.mp3'
          else if (format.includes('webm')) fileExtension = '.webm'
          else if (format.includes('ogg')) fileExtension = '.ogg'
          break
        }
      }
      
      // Create recorder with time slicing to ensure data collection
      const recorder = new MediaRecorder(stream, mimeType ? { 
        mimeType,
        audioBitsPerSecond: 16000 
      } : {
        audioBitsPerSecond: 16000
      })
      
      console.log(`Recording with format: ${mimeType || 'default'}`)
      
      // Clear previous chunks
      setRecordedChunks([])
      
      recorder.ondataavailable = (event) => {
        console.log(`Data chunk received: ${event.data.size} bytes`)
        if (event.data.size > 0) {
          setRecordedChunks(prev => [...prev, event.data])
        }
      }
      
      recorder.onstop = async () => {
        // Wait a moment to ensure all data is collected
        setTimeout(async () => {
          console.log(`Recording stopped. Processing ${recordedChunks.length} chunks`)
          
          if (recordedChunks.length === 0) {
            toast.error('No audio was recorded. Please try again.')
            stream.getTracks().forEach(track => track.stop())
            setIsRecording(false)
            setVoiceActive(false)
            return
          }
          
          const audioBlob = new Blob(recordedChunks, { type: mimeType || 'audio/webm' })
          
          if (audioBlob.size === 0) {
            toast.error('Empty recording. Please speak louder and try again.')
            stream.getTracks().forEach(track => track.stop())
            setIsRecording(false)
            setVoiceActive(false)
            return
          }
          
          const audioFile = new File([audioBlob], `recording${fileExtension}`, { 
            type: mimeType || 'audio/webm' 
          })
          
          console.log(`Created audio file: ${audioFile.name}, size: ${audioFile.size}, type: ${audioFile.type}`)
          
          try {
            const response = await speechToTextMutation.mutateAsync(audioFile)
            if (response.success && response.text.trim()) {
              setInputValue(prev => prev + (prev ? ' ' : '') + response.text.trim())
              toast.success('Voice input transcribed successfully')
            } else {
              console.error('Speech to text failed:', response.error)
              const errorMessage = response.error || 'Could not transcribe voice input'
              
              // Provide helpful suggestions based on common errors
              if (errorMessage.includes('format')) {
                toast.error('Audio format not supported. Please try speaking again or use text input.')
              } else if (errorMessage.includes('understand')) {
                toast.error('Could not understand speech. Please speak more clearly and try again.')
              } else if (errorMessage.includes('service')) {
                toast.error('Speech service unavailable. Please try again later or use text input.')
              } else {
                toast.error(errorMessage)
              }
            }
          } catch (error) {
            console.error('Speech to text error:', error)
            toast.error('Failed to process voice input. Please try again or use text input.')
          }
          
          // Clean up
          stream.getTracks().forEach(track => track.stop())
          setRecordedChunks([])
          setIsRecording(false)
          setVoiceActive(false)
        }, 200)
      }
      
      setMediaRecorder(recorder)
      
      // Start recording with time slicing (collect data every second)
      recorder.start(1000)
      setIsRecording(true)
      toast.success('Recording started... Speak now!')
      
    } catch (error) {
      console.error('Error starting recording:', error)
      if (error instanceof DOMException && error.name === 'NotAllowedError') {
        toast.error('Microphone access denied. Please enable microphone permissions.')
      } else if (error instanceof DOMException && error.name === 'NotFoundError') {
        toast.error('No microphone found. Please connect a microphone.')
      } else {
        toast.error('Could not access microphone')
      }
      setVoiceActive(false)
    }
  }

  const stopRecording = () => {
    if (mediaRecorder && isRecording) {
      mediaRecorder.stop()
      toast.info('Processing voice input...')
    }
  }

  const handleVoiceToggle = () => {
    if (selectedAgents.length === 0) {
      toast.error('Please select at least one expert before using voice input')
      return
    }
    
    if (voiceActive && isRecording) {
      stopRecording()
    } else if (!voiceActive) {
      setVoiceActive(true)
      
      // Use browser speech recognition if available and preferred
      if (browserSpeechSupported && speechRecognition && !useBrowserSpeech) {
        try {
          speechRecognition.start()
          toast.info('🎤 Browser speech recognition started. Speak now!')
        } catch (error) {
          console.error('Browser speech recognition failed:', error)
          toast.error('Browser speech failed. Trying microphone recording...')
          startRecording()
        }
      } else {
        // Fall back to microphone recording
        startRecording()
      }
    }
  }

  // Browser speech recognition handler
  const handleBrowserSpeech = () => {
    if (selectedAgents.length === 0) {
      toast.error('Please select at least one expert before using voice input')
      return
    }

    if (speechRecognition) {
      try {
        setVoiceActive(true)
        speechRecognition.start()
        toast.info('🎤 Browser speech recognition started. Speak now!')
      } catch (error) {
        console.error('Browser speech recognition failed:', error)
        toast.error('Browser speech recognition failed. Please try again.')
        setVoiceActive(false)
      }
    }
  }

  const handleAgentToggle = (agentId: string) => {
    setSelectedAgents(
      selectedAgents.includes(agentId) 
        ? selectedAgents.filter((id: string) => id !== agentId)
        : [...selectedAgents, agentId]
    )
  }

  const handleSendMessage = async () => {
    if (!inputValue.trim() || selectedAgents.length === 0) {
      if (selectedAgents.length === 0) {
        toast.error('Please select at least one agent to chat with');
      }
      return;
    }

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: inputValue,
      role: 'user',
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    const currentInput = inputValue
    setInputValue('')
    setIsLoading(true)

    try {
      // Chat with each selected agent
      const responses = await Promise.all(
        selectedAgents.map(async (agentId: string) => {
          const agentType = agentMapping[agentId]
          if (!agentType) return null
          
          return chatMutation.mutateAsync({
            message: currentInput,
            agentType
          })
        })
      )

      // Filter out null responses and create response messages
      const validResponses = responses.filter(Boolean)
      
      if (validResponses.length > 0) {
        validResponses.forEach((response, index) => {
          const responseMessage: ChatMessage = {
            id: (Date.now() + index + 1).toString(),
            content: response!.response,
            role: 'agent',
            agentName: response!.agent_name,
            timestamp: new Date(),
            citations: response!.citations,
            sources: response!.citations?.map((c: any) => c.doc_title).filter(Boolean) || []
          }
          
          setMessages(prev => [...prev, responseMessage])
        })
      }
      
    } catch (error) {
      console.error('Chat error:', error)
      toast.error('Failed to get response from agents')
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  // Direct microphone voice input (like original Streamlit app)
  const handleDirectVoiceInput = async () => {
    if (selectedAgents.length === 0) {
      toast.error('Please select at least one expert before using voice input')
      return
    }

    try {
      setVoiceActive(true)
      toast.info('🎤 Listening... Speak now! (This uses direct microphone access like the original app)')
      
      const response = await directSpeechMutation.mutateAsync()
      
      if (response.success && response.text.trim()) {
        setInputValue(prev => prev + (prev ? ' ' : '') + response.text.trim())
        toast.success('Voice input transcribed successfully')
      } else {
        const errorMessage = response.error || 'Could not transcribe voice input'
        
        // Provide helpful suggestions based on common errors
        if (errorMessage.includes('format')) {
          toast.error('Audio format not supported. Trying browser recording...')
          setUseDirectMicrophone(false) // Fall back to browser recording
        } else if (errorMessage.includes('understand')) {
          toast.error('Could not understand speech. Please speak more clearly and try again.')
        } else if (errorMessage.includes('service')) {
          toast.error('Speech service unavailable. Please try again later or use text input.')
        } else {
          toast.error(errorMessage)
        }
      }
    } catch (error) {
      console.error('Direct speech error:', error)
      toast.error('Direct microphone access failed. Falling back to browser recording...')
      setUseDirectMicrophone(false) // Fall back to browser recording
    } finally {
      setVoiceActive(false)
    }
  }

  return (
    <div className="h-screen max-h-screen flex flex-col bg-white overflow-hidden">
      {/* Header */}
      <div className="border-b border-gray-200 p-4 lg:p-6 flex-shrink-0">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Knowledge Base</h1>
          <p className="text-gray-600">Chat with our AI experts for personalized guidance</p>
          <div className="mt-2 text-sm text-blue-600 bg-blue-50 border border-blue-200 rounded-lg p-2 flex items-center">
            <Mic className="w-4 h-4 mr-2" />
            <span>💡 Tip: Use the microphone button to speak your questions directly! {browserSpeechSupported ? 'Browser speech recognition available for best results.' : 'Audio recording will be used.'}</span>
          </div>
          {browserSpeechSupported && (
            <div className="mt-2 text-sm text-green-600 bg-green-50 border border-green-200 rounded-lg p-2 flex items-center justify-between">
              <div className="flex items-center">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                <span>Browser speech recognition is available for instant transcription</span>
              </div>
              <button
                onClick={handleBrowserSpeech}
                disabled={selectedAgents.length === 0}
                className="text-xs bg-green-100 hover:bg-green-200 px-2 py-1 rounded border border-green-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Try it
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Agent Selection */}
      <div className="border-b border-gray-200 p-4 bg-gray-50 flex-shrink-0">
        <div className="max-w-4xl mx-auto">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Select Experts to Consult:</h3>
          <div className="flex flex-wrap gap-2">
            {agents.map((agent) => (
              <motion.button
                key={agent.id}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => handleAgentToggle(agent.id)}
                className={`px-3 py-2 rounded-full text-sm font-medium border transition-colors ${
                  selectedAgents.includes(agent.id)
                    ? 'bg-blue-500 text-white border-blue-500'
                    : 'bg-white text-gray-700 border-gray-300 hover:border-blue-300'
                }`}
              >
                <span className="mr-1">{agent.icon}</span>
                {agent.name}
              </motion.button>
            ))}
          </div>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 lg:p-6">
        <div className="max-w-4xl mx-auto space-y-6">
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-xs lg:max-w-2xl xl:max-w-3xl px-4 py-3 rounded-2xl ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white ml-auto'
                    : 'bg-white border border-gray-200 text-gray-900 shadow-sm'
                }`}>
                  {message.role === 'agent' && (
                    <div className="flex items-center mb-2 text-sm font-medium text-blue-600">
                      <Bot className="w-4 h-4 mr-2" />
                      {message.agentName}
                    </div>
                  )}
                  <div className="text-sm leading-relaxed">
                    {message.role === 'agent' ? (
                      <MarkdownRenderer 
                        content={message.content} 
                        className="text-gray-900"
                      />
                    ) : (
                      <div className="whitespace-pre-wrap">{message.content}</div>
                    )}
                  </div>
                  {message.sources && message.sources.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <p className="text-xs text-gray-500 font-medium mb-1">Sources:</p>
                      <p className="text-xs text-gray-500">{message.sources.join(', ')}</p>
                    </div>
                  )}
                  <div className={`mt-2 text-xs flex items-center ${
                    message.role === 'user' ? 'text-blue-100' : 'text-gray-400'
                  }`}>
                    <Clock className="w-3 h-3 mr-1" />
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          
          {isLoading && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-start"
            >
              <div className="bg-white border border-gray-200 px-4 py-3 rounded-2xl shadow-sm">
                <div className="flex items-center space-x-1 text-blue-600 mb-1">
                  <Bot className="w-4 h-4" />
                  <span className="text-sm font-medium">AI Agent is thinking...</span>
                </div>
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </motion.div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 p-4 lg:p-6 bg-white flex-shrink-0">
        <div className="max-w-4xl mx-auto">
          {/* Recording indicator */}
          <AnimatePresence>
            {isRecording && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="mb-3 flex items-center justify-center"
              >
                <div className="bg-red-100 border border-red-300 rounded-lg px-4 py-2 flex items-center space-x-2">
                  <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                  <span className="text-red-700 text-sm font-medium">Recording... Speak now</span>
                  <button
                    onClick={stopRecording}
                    className="text-red-600 hover:text-red-800 text-xs underline"
                  >
                    Stop & Process
                  </button>
                </div>
              </motion.div>
            )}
            {speechToTextMutation.isPending && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="mb-3 flex items-center justify-center"
              >
                <div className="bg-blue-100 border border-blue-300 rounded-lg px-4 py-2 flex items-center space-x-2">
                  <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                  <span className="text-blue-700 text-sm font-medium">Processing voice input...</span>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          
          <div className="flex items-end space-x-3">
            <div className="flex-1 relative">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={
                  selectedAgents.length === 0
                    ? "Please select an expert first..."
                    : isRecording 
                    ? "🎤 Recording... Speak now and click the microphone to stop"
                    : speechToTextMutation.isPending
                    ? "Processing voice input..."
                    : "Message SHAKTI AI experts... (or use voice input 🎤)"
                }
                className={`w-full px-4 py-3 border rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all ${
                  isRecording ? 'border-red-300 bg-red-50' : 
                  selectedAgents.length === 0 ? 'border-gray-200 bg-gray-50' :
                  'border-gray-300 bg-white hover:border-gray-400'
                }`}
                rows={Math.min(Math.max(inputValue.split('\n').length, 1), 4)}
                disabled={isLoading || selectedAgents.length === 0}
              />
              {selectedAgents.length === 0 && (
                <div className="absolute inset-0 bg-gray-50 bg-opacity-50 rounded-2xl flex items-center justify-center pointer-events-none">
                  <p className="text-sm text-gray-500">Select an expert above to start chatting</p>
                </div>
              )}
            </div>
            <button
              onClick={handleVoiceToggle}
              disabled={isLoading || speechToTextMutation.isPending || selectedAgents.length === 0}
              className={`p-3 rounded-full transition-colors ${
                voiceActive && isRecording 
                  ? 'bg-red-500 text-white animate-pulse' 
                  : voiceActive
                  ? 'bg-orange-500 text-white'
                  : selectedAgents.length === 0
                  ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
              title={
                selectedAgents.length === 0 
                  ? "Select experts first to use voice input"
                  : isRecording 
                  ? "Click to stop recording and process voice"
                  : "Click to start voice input"
              }
            >
              {voiceActive && isRecording ? (
                <div className="flex items-center">
                  <MicOff className="w-5 h-5" />
                </div>
              ) : (
                <Mic className="w-5 h-5" />
              )}
            </button>
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isLoading || selectedAgents.length === 0}
              className={`p-3 rounded-full transition-colors ${
                !inputValue.trim() || selectedAgents.length === 0 || isLoading
                  ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                  : 'bg-blue-500 text-white hover:bg-blue-600'
              }`}
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </button>
          </div>
          
          {/* Expert selection hint */}
          {selectedAgents.length === 0 && (
            <div className="mt-3 text-center">
              <p className="text-sm text-gray-500">👆 Select one or more experts above to start your conversation</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
