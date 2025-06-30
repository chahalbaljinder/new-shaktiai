'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Mic, MicOff, Volume2, VolumeX, Settings, Loader2 } from 'lucide-react'
import { useAppStore } from '@/lib/store'
import { useSpeechToText, useTextToSpeech } from '@/lib/api/hooks'
import { toast } from 'sonner'

export default function VoiceInterface() {
  const { voiceActive, setVoiceActive } = useAppStore()
  const speechToTextMutation = useSpeechToText()
  const textToSpeechMutation = useTextToSpeech()
  
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [volume, setVolume] = useState(0.8)
  const [muted, setMuted] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const chunksRef = useRef<Blob[]>([])

  // Initialize media recorder
  useEffect(() => {
    const initMediaRecorder = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        const recorder = new MediaRecorder(stream)
        
        recorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            chunksRef.current.push(event.data)
          }
        }
        
        recorder.onstop = async () => {
          const audioBlob = new Blob(chunksRef.current, { type: 'audio/wav' })
          chunksRef.current = []
          
          // Convert to File object
          const audioFile = new File([audioBlob], 'recording.wav', { type: 'audio/wav' })
          
          try {
            const result = await speechToTextMutation.mutateAsync(audioFile)
            if (result.success && result.text) {
              setTranscript(result.text)
              toast.success('Speech converted to text!')
            } else {
              toast.error('Could not understand speech')
            }
          } catch (error) {
            toast.error('Failed to process speech')
          }
        }
        
        setMediaRecorder(recorder)
      } catch (error) {
        console.error('Failed to initialize media recorder:', error)
        toast.error('Could not access microphone')
      }
    }

    if (voiceActive) {
      initMediaRecorder()
    }
  }, [voiceActive, speechToTextMutation])

  const startListening = () => {
    if (!voiceActive || !mediaRecorder) {
      toast.error('Voice interface not available')
      return
    }
    
    if (mediaRecorder.state === 'inactive') {
      chunksRef.current = []
      mediaRecorder.start()
      setIsListening(true)
      setIsRecording(true)
      setTranscript('')
      toast.info('Listening...')
    }
  }

  const stopListening = () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      mediaRecorder.stop()
      setIsListening(false)
      setIsRecording(false)
    }
  }

  const speakText = async (text: string) => {
    if (muted || !text.trim()) return
    
    try {
      // First try Web Speech API (faster, works offline)
      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text)
        utterance.volume = volume
        utterance.rate = 0.9
        utterance.pitch = 1.1
        speechSynthesis.speak(utterance)
      } else {
        // Fallback to backend TTS
        const audioBlob = await textToSpeechMutation.mutateAsync({ text })
        const audioUrl = URL.createObjectURL(audioBlob)
        
        if (audioRef.current) {
          audioRef.current.src = audioUrl
          audioRef.current.volume = volume
          audioRef.current.play()
        }
      }
    } catch (error) {
      console.error('Failed to speak text:', error)
      toast.error('Failed to generate speech')
    }
  }

  return (
    <AnimatePresence>
      {voiceActive && (
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 50 }}
          className="fixed bottom-4 right-4 bg-white rounded-xl shadow-2xl border border-gray-200 p-4 z-50 min-w-80"
        >
          {/* Header */}
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900">Voice Assistant</h3>
            <button
              onClick={() => setVoiceActive(false)}
              className="p-1 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <Settings className="w-4 h-4 text-gray-500" />
            </button>
          </div>

          {/* Voice Visualization */}
          <div className="flex items-center justify-center mb-4">
            <motion.div
              animate={{
                scale: isListening ? [1, 1.2, 1] : 1,
                opacity: isListening ? [0.6, 1, 0.6] : 1,
              }}
              transition={{
                duration: 1,
                repeat: isListening ? Infinity : 0,
              }}
              className={`w-16 h-16 rounded-full flex items-center justify-center ${
                isListening 
                  ? 'bg-red-500 text-white' 
                  : speechToTextMutation.isPending
                  ? 'bg-yellow-500 text-white'
                  : 'bg-blue-500 text-white hover:bg-blue-600'
              } cursor-pointer transition-colors`}
              onClick={isListening ? stopListening : startListening}
            >
              {speechToTextMutation.isPending ? (
                <Loader2 className="w-6 h-6 animate-spin" />
              ) : isListening ? (
                <MicOff className="w-6 h-6" />
              ) : (
                <Mic className="w-6 h-6" />
              )}
            </motion.div>
          </div>

          {/* Status */}
          <div className="text-center mb-4">
            <p className={`text-sm font-medium ${
              speechToTextMutation.isPending 
                ? 'text-yellow-600'
                : isListening 
                ? 'text-red-600' 
                : 'text-gray-600'
            }`}>
              {speechToTextMutation.isPending 
                ? 'Processing speech...'
                : isListening 
                ? 'Listening...' 
                : 'Tap microphone to speak'
              }
            </p>
            {transcript && (
              <p className="text-xs text-gray-500 mt-1 p-2 bg-gray-50 rounded">"{transcript}"</p>
            )}
          </div>

          {/* Controls */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setMuted(!muted)}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                {muted ? (
                  <VolumeX className="w-4 h-4 text-gray-500" />
                ) : (
                  <Volume2 className="w-4 h-4 text-gray-500" />
                )}
              </button>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={volume}
                onChange={(e) => setVolume(parseFloat(e.target.value))}
                className="w-16 h-1 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                disabled={muted}
              />
            </div>
            
            <button
              onClick={() => speakText('Voice assistant is ready to help you.')}
              className="px-3 py-1 bg-blue-100 text-blue-700 rounded-lg text-sm hover:bg-blue-200 transition-colors"
              disabled={muted}
            >
              Test Voice
            </button>
          </div>

          {/* Quick Actions */}
          <div className="mt-4 pt-4 border-t border-gray-200">
            <p className="text-xs text-gray-500 mb-2">Quick Commands:</p>
            <div className="grid grid-cols-2 gap-2">
              {['Ask question', 'Add wish', 'Get help', 'Emergency'].map((command) => (
                <button
                  key={command}
                  onClick={() => speakText(`${command} activated`)}
                  className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs hover:bg-gray-200 transition-colors"
                  disabled={muted}
                >
                  {command}
                </button>
              ))}
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
