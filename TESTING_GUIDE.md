# SHAKTI-AI ChatGPT-Like Interface Testing Guide

## Current Status
✅ **Authentication System**: Complete login/logout functionality
✅ **Backend Service**: FastAPI server with AI agent endpoints
✅ **Enhanced Chat UI**: ChatGPT-like conversation interface
✅ **Agent Integration**: 5 AI experts ready to respond

## How to Test the Chat Interface

### 1. Start the Application
```bash
# Run the full-stack startup script
cd "c:\Users\anjal\SHAKTI AII\new-shaktiai"
.\start-full-app.bat
```

### 2. Access the Interface
- Open browser to: http://localhost:3000
- Login with your credentials
- Navigate to "Knowledge Base" from the sidebar

### 3. Test Agent Conversations

#### Available Experts:
1. **Dr. Gynika** - Reproductive Health Specialist
2. **Advocate Vaanya** - Feminist Rights & Legal Expert  
3. **Counselor Nyaya** - Legal Rights Advisor
4. **Maya** - Maternal Health Specialist
5. **Life Coach Meher** - Mental Health & Wellness Expert

#### Testing Steps:
1. **Select Expert(s)**: Click on one or more expert cards at the top
2. **Start Conversation**: Type your question in the ChatGPT-like input box
3. **Send Message**: Click send button or press Enter
4. **Voice Input**: Click microphone icon to use speech-to-text
5. **View Response**: See AI expert responses in conversation bubbles

### 4. ChatGPT-Like Features to Test

#### Message Display:
- Your messages appear on the right (blue bubbles)
- Agent responses appear on the left (white bubbles with expert info)
- Conversation history is preserved
- Smooth animations and transitions

#### Input Features:
- Auto-resizing textarea (like ChatGPT)
- Disabled state when no expert selected
- Visual feedback for different states
- Voice input with recording indicator
- Loading states during processing

#### Expert Selection:
- Multiple expert selection support
- Visual feedback when experts are selected
- Each response shows which expert answered
- Color-coded expert badges

### 5. Sample Questions to Test

#### For Dr. Gynika (Reproductive Health):
- "What are the signs of a healthy pregnancy?"
- "Can you explain different contraception methods?"

#### For Advocate Vaanya (Feminist Rights):
- "What are my rights in the workplace?"
- "How can I report gender discrimination?"

#### For Counselor Nyaya (Legal Rights):
- "What legal protections do I have?"
- "How do I understand my constitutional rights?"

#### For Maya (Maternal Health):
- "What should I know about postpartum care?"
- "How can I prepare for childbirth?"

#### For Life Coach Meher (Mental Health):
- "How can I manage stress and anxiety?"
- "What are some wellness practices I should follow?"

### 6. Expected Behavior

#### ✅ Working Features:
- Smooth conversation flow like ChatGPT
- Expert responses with contextual knowledge
- Voice input processing
- Message history preservation
- Responsive design for all devices
- Loading indicators during processing

#### 🔄 Backend Processing:
- Messages sent to: http://localhost:8000/api/agents/chat
- Agent responses generated using SHAKTI-AI crew
- Conversation context maintained

### 7. Troubleshooting

#### If Agents Don't Respond:
1. Check backend service is running (port 8000)
2. Verify environment variables in `.env.local`
3. Ensure Python dependencies are installed
4. Check browser console for API errors

#### If UI Issues:
1. Refresh the page
2. Clear browser cache
3. Check if experts are selected
4. Verify input field isn't disabled

### 8. Technical Notes

#### Backend Service:
- Runs on: http://localhost:8000
- Endpoint: /api/agents/chat
- Agent Types: reproductive, feminist, legal, maternal, mental

#### Frontend Service:  
- Runs on: http://localhost:3000
- Framework: Next.js 14 with TypeScript
- Styling: Tailwind CSS with Framer Motion

#### Environment Configuration:
- `NEXT_PUBLIC_API_URL=http://localhost:8000`
- Database credentials in `.env.local`
- All authentication tokens configured

## Success Criteria

The ChatGPT-like interface is working correctly when:
1. ✅ You can select experts and see visual feedback
2. ✅ Messages send successfully and show in conversation bubbles
3. ✅ AI experts respond with relevant, helpful information
4. ✅ Conversation history is maintained and scrollable
5. ✅ Voice input works and converts speech to text
6. ✅ Interface is responsive and smooth like ChatGPT
7. ✅ Loading states show during processing
8. ✅ Error states handle gracefully

---

**Next Steps**: Start the application and test the ChatGPT-like conversation interface with the AI experts!
</content>
</invoke>
