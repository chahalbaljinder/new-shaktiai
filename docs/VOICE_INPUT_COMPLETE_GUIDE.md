# SHAKTI-AI Voice Input Complete Guide

## Overview
SHAKTI-AI now features comprehensive voice input functionality that works seamlessly in the Knowledge Base, providing multiple options for speech-to-text conversion with intelligent fallbacks.

## Voice Input Methods

### 1. Browser-Based Speech Recognition (Recommended)
- **How it works**: Uses the browser's native Web Speech API for instant, real-time transcription
- **Availability**: Chrome, Edge, Safari (with microphone permissions)
- **Advantages**: 
  - Instant transcription (no file upload needed)
  - High accuracy
  - Works entirely in the browser
  - No server processing required
- **How to use**: Click the "Try it" button in the green banner or use the main microphone button

### 2. Audio Recording & Upload
- **How it works**: Records audio in the browser, uploads to backend for transcription using SpeechRecognition library
- **Availability**: All modern browsers with microphone access
- **Advantages**: 
  - Works even when browser speech recognition is unavailable
  - Processes audio on the server
  - Supports multiple audio formats
- **How to use**: Click the microphone button when browser speech is not available

### 3. Direct Server Microphone (Backend Only)
- **How it works**: Uses the server's direct microphone access (like original Streamlit app)
- **Availability**: Server-side only (not accessible from browser due to security)
- **Use case**: Administrative/testing purposes, desktop applications
- **How to use**: Available via `/api/voice/direct-speech-to-text` endpoint

## User Interface Features

### Visual Indicators
- **Green banner**: Shows when browser speech recognition is available
- **Blue banner**: General voice input tips and guidance
- **Recording indicator**: Red pulsing animation when recording
- **Processing indicator**: Blue loading animation during transcription

### Smart Fallbacks
- If browser speech fails → automatically tries audio recording
- If audio format unsupported → provides clear error messages with suggestions
- If microphone access denied → guides user to enable permissions

## Step-by-Step Usage

### For Best Experience (Browser Speech):
1. Open Knowledge Base in Chrome, Edge, or Safari
2. Select at least one expert/agent
3. Look for the green banner indicating browser speech is available
4. Click "Try it" or use the microphone button
5. Allow microphone permissions when prompted
6. Speak clearly and naturally
7. Transcription appears instantly in the text input

### For Audio Recording Method:
1. Select at least one expert/agent
2. Click the microphone button (🎤)
3. Allow microphone permissions when prompted
4. Speak when you see "Recording... Speak now"
5. Click the microphone again to stop recording
6. Wait for processing (blue loading indicator)
7. Transcription appears in the text input

## Troubleshooting

### Common Issues & Solutions

**"Microphone access denied"**
- Enable microphone permissions in browser settings
- Refresh the page and try again
- Check if other apps are using the microphone

**"No speech detected"**
- Speak louder and more clearly
- Check microphone is working in other apps
- Try moving closer to the microphone

**"Audio format not supported"**
- Browser will automatically try alternative recording formats
- Try using Chrome or Edge for better format support

**"Speech recognition failed"**
- Check internet connection (browser speech needs online access)
- Try the audio recording method as fallback
- Refresh the page and try again

**Voice input not appearing**
- Make sure you've selected at least one expert first
- Check that the transcribed text appears in the input field
- Try typing to confirm the input field is working

## Browser Compatibility

| Browser | Browser Speech | Audio Recording | Recommended |
|---------|----------------|-----------------|-------------|
| Chrome | ✅ Full support | ✅ Yes | ⭐ Best |
| Edge | ✅ Full support | ✅ Yes | ⭐ Best |
| Firefox | ❌ Limited | ✅ Yes | ⚠️ Recording only |
| Safari | ✅ iOS/macOS | ✅ Yes | ✅ Good |

## Technical Implementation

### Frontend (Next.js)
- **Components**: Enhanced KnowledgeBase.tsx with dual voice input methods
- **APIs**: React Query hooks for both speech methods
- **UI**: Animated indicators, error handling, accessibility features

### Backend (FastAPI)
- **Endpoints**: 
  - `/api/voice/speech-to-text` (file upload method)
  - `/api/voice/direct-speech-to-text` (server microphone)
- **Libraries**: SpeechRecognition, pydub for audio processing
- **Formats**: Supports WAV, MP3, WebM, OGG audio formats

### Audio Processing Pipeline
1. **Browser Capture**: MediaRecorder API with optimized settings
2. **Format Selection**: Automatic format detection and preference ordering
3. **Server Processing**: SpeechRecognition with Google Speech API
4. **Error Handling**: Comprehensive error messages and fallback options

## Privacy & Security
- Voice data is processed locally when using browser speech recognition
- Audio files are temporarily uploaded and immediately deleted after processing
- No voice data is stored permanently
- All microphone access requires explicit user permission

## Performance Optimization
- Automatic format selection for best processing compatibility
- Intelligent chunking for longer audio recordings
- Real-time feedback during recording and processing
- Graceful degradation when features are unavailable

## Future Enhancements
- Offline speech recognition capabilities
- Multiple language support
- Voice command recognition
- Custom vocabulary for medical/legal terms
- Voice-activated agent selection

## Support
For issues or questions about voice input:
1. Check this guide for common solutions
2. Verify browser compatibility
3. Test microphone with other applications
4. Check browser console for technical error details

---

**Last Updated**: July 2025  
**Version**: 1.0  
**Status**: Fully Implemented and Tested
