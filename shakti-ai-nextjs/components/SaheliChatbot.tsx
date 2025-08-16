'use client';

import React, { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';

interface ChatMessage {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

interface QuickAction {
  label: string;
  action: () => void;
}

const SaheliChatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const pathname = usePathname();

  // Predefined responses based on context
  const getContextualHelp = () => {
    switch (pathname) {
      case '/':
      case '/dashboard':
        return {
          welcome: "Welcome to SHAKTI-AI! I'm Saheli, your personal guide. How can I help you explore our health experts today? 🌟",
          suggestions: [
            { label: "Choose an Expert", action: () => handleQuickResponse("How do I choose the right expert?") },
            { label: "Voice Input", action: () => handleQuickResponse("How does voice input work?") },
            { label: "App Features", action: () => handleQuickResponse("What features are available?") },
            { label: "Privacy Info", action: () => handleQuickResponse("Is my information private?") }
          ]
        };
      case '/knowledge-base':
        return {
          welcome: "I can help you navigate our Knowledge Base! What would you like to learn about? 📚",
          suggestions: [
            { label: "Search Tips", action: () => handleQuickResponse("How do I search effectively?") },
            { label: "Document Types", action: () => handleQuickResponse("What documents are available?") },
            { label: "Back to Experts", action: () => handleQuickResponse("How do I chat with experts?") }
          ]
        };
      case '/wishes-vault':
        return {
          welcome: "The Wishes Vault is your personal space! Let me help you get started. ✨",
          suggestions: [
            { label: "Create Wish", action: () => handleQuickResponse("How do I create a wish?") },
            { label: "Organize Wishes", action: () => handleQuickResponse("How do I organize my wishes?") },
            { label: "Privacy", action: () => handleQuickResponse("Are my wishes private?") }
          ]
        };
      default:
        return {
          welcome: "Hi! I'm Saheli, your SHAKTI-AI guide. How can I assist you today? 🌟",
          suggestions: [
            { label: "Get Started", action: () => handleQuickResponse("How do I get started?") },
            { label: "Choose Expert", action: () => handleQuickResponse("How do I choose the right expert?") },
            { label: "App Tour", action: () => handleQuickResponse("Give me a tour of the app") }
          ]
        };
    }
  };

  // Predefined responses database
  const getResponse = (userMessage: string): string => {
    const message = userMessage.toLowerCase();

    // Expert selection help
    if (message.includes('expert') || message.includes('choose') || message.includes('select')) {
      return `Great question! Here's how to choose the right expert:

👩‍⚕️ **Dr. Gynika** - For reproductive health, periods, contraception, PCOS
🤱 **Maya** - For pregnancy, childbirth, breastfeeding, maternal care
💭 **Meher** - For mental health, anxiety, stress, emotional support
⚖️ **Nyaya** - For legal rights, workplace issues, family law
💪 **Vaanya** - For empowerment, menopause, career guidance

Just click on the expert button that matches your needs! Each expert specializes in their area and will give you personalized guidance.`;
    }

    // Voice input help
    if (message.includes('voice') || message.includes('microphone') || message.includes('speak')) {
      return `Voice input makes chatting easier! Here's how:

🎤 **Click the microphone button** in the chat area
🗣️ **Speak your question clearly** - the app will transcribe it
✏️ **Review and edit** if needed before sending
📱 **Works on most modern browsers** with microphone access

Voice input is especially helpful for longer questions or when typing is difficult. Your voice is processed securely and not stored.`;
    }

    // Privacy and security
    if (message.includes('private') || message.includes('security') || message.includes('safe') || message.includes('confidential')) {
      return `Your privacy is our top priority! 🔒

✅ **All conversations** are encrypted and secure
✅ **No personal data** is shared with third parties  
✅ **Local storage** keeps your wishes vault private
✅ **Professional confidentiality** maintained by all experts
✅ **You control your data** - delete anytime

SHAKTI-AI follows medical privacy standards. Your health information stays between you and your chosen expert.`;
    }

    // App features
    if (message.includes('feature') || message.includes('what can') || message.includes('capabilities')) {
      return `SHAKTI-AI offers comprehensive women's health support:

🏥 **Expert Consultations** - Chat with 5 specialized health experts
📚 **Knowledge Base** - Search health documents and resources  
🗣️ **Voice Input** - Speak your questions naturally
✨ **Wishes Vault** - Personal goal and wish tracking
🚨 **Emergency Mode** - Quick access to urgent resources
⚙️ **Settings** - Customize your experience

Everything is designed to empower your health journey with professional, caring support.`;
    }

    // Getting started
    if (message.includes('start') || message.includes('begin') || message.includes('how do i')) {
      return `Welcome to SHAKTI-AI! Here's how to get started:

1️⃣ **Choose your expert** - Select the specialist that matches your needs
2️⃣ **Ask your question** - Type or speak your health concern
3️⃣ **Get expert guidance** - Receive personalized, professional advice
4️⃣ **Explore more** - Check out Knowledge Base and Wishes Vault

💡 **Tip**: Don't worry about asking "the right question" - our experts are here to help with any women's health topic, big or small!`;
    }

    // Wishes vault help
    if (message.includes('wish') || message.includes('vault') || message.includes('goal')) {
      return `The Wishes Vault is your personal empowerment space! ✨

📝 **Create wishes** - Set health, career, and personal goals
🗂️ **Organize by category** - Health, career, relationships, personal
📅 **Set reminders** - Get gentle nudges toward your goals
📊 **Track progress** - See how you're growing and achieving
🔒 **Stay private** - Only you can see your wishes

Use it for anything from "drink more water" to "start my own business" - every wish matters!`;
    }

    // Knowledge base help
    if (message.includes('knowledge') || message.includes('search') || message.includes('document')) {
      return `Our Knowledge Base is packed with helpful resources! 📚

🔍 **Search by topic** - Find specific health information quickly
📄 **Browse documents** - Expert-curated women's health content
🏷️ **Filter by category** - Reproductive, maternal, mental health, legal
💡 **Evidence-based** - All content is medically reviewed

**Search Tips**:
• Use specific terms like "PCOS symptoms" or "pregnancy nutrition"
• Try different keywords if you don't find what you need
• Browse categories when you're not sure what to search for`;
    }

    // App tour
    if (message.includes('tour') || message.includes('around') || message.includes('show me')) {
      return `Let me give you a quick tour of SHAKTI-AI! 🚀

🏠 **Dashboard** - Your home base with expert selection
👩‍⚕️ **AI Experts** - Chat with 5 specialized health professionals
📚 **Knowledge Base** - Search our comprehensive health library
✨ **Wishes Vault** - Your personal goal and empowerment tracker
🗣️ **Voice Input** - Available throughout the app for easy interaction
🚨 **Emergency** - Quick access to urgent health resources
⚙️ **Settings** - Customize your experience

Each section is designed to support different aspects of your health and wellness journey!`;
    }

    // Default helpful response
    return `I'm here to help! I can assist you with:

🌟 **Choosing the right expert** for your health questions
🗣️ **Using voice input** to make chatting easier  
📱 **Navigating app features** like Knowledge Base and Wishes Vault
🔒 **Understanding privacy** and how your data is protected
🚀 **Getting started** with your health journey

What specific area would you like help with? Just ask me anything about using SHAKTI-AI!`;
  };

  // Handle quick response buttons
  const handleQuickResponse = (response: string) => {
    addUserMessage(response);
  };

  // Add user message and trigger bot response
  const addUserMessage = (text: string) => {
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    // Simulate typing delay
    setTimeout(() => {
      const botResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: getResponse(text),
        isUser: false,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 800 + Math.random() * 400); // 0.8-1.2 second delay
  };

  // Initialize chat when opened
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const contextHelp = getContextualHelp();
      const welcomeMessage: ChatMessage = {
        id: 'welcome',
        text: contextHelp.welcome,
        isUser: false,
        timestamp: new Date()
      };
      setMessages([welcomeMessage]);
    }
  }, [isOpen, pathname, messages.length]);

  // Handle input submission
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const message = formData.get('message') as string;
    
    if (message.trim()) {
      addUserMessage(message.trim());
      e.currentTarget.reset();
    }
  };

  const contextHelp = getContextualHelp();

  return (
    <>
      {/* Floating Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className={`w-14 h-14 rounded-full shadow-lg transition-all duration-300 flex items-center justify-center text-white font-bold text-lg relative ${
            isOpen 
              ? 'bg-gray-500 hover:bg-gray-600' 
              : 'bg-gradient-to-br from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600'
          }`}
          aria-label="Open Saheli Helper Chatbot"
        >
          {isOpen ? '✕' : '💬'}
          {!isOpen && (
            <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full"></div>
          )}
        </button>
      </div>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 w-80 h-96 bg-white rounded-lg shadow-2xl border border-gray-200 z-50 flex flex-col overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white p-4 flex items-center">
            <div className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center mr-3">
              🌟
            </div>
            <div>
              <h3 className="font-semibold">Saheli</h3>
              <p className="text-sm opacity-90">Your SHAKTI-AI Guide</p>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs p-3 rounded-lg text-sm ${
                    message.isUser
                      ? 'bg-purple-500 text-white'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  <pre className="whitespace-pre-wrap font-sans">{message.text}</pre>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-gray-800 p-3 rounded-lg text-sm">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Quick Actions */}
          {messages.length === 1 && (
            <div className="px-4 pb-2">
              <div className="grid grid-cols-2 gap-2">
                {contextHelp.suggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={suggestion.action}
                    className="text-xs bg-purple-50 text-purple-700 px-2 py-1 rounded-full hover:bg-purple-100 transition-colors"
                  >
                    {suggestion.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input */}
          <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200">
            <div className="flex space-x-2">
              <input
                type="text"
                name="message"
                placeholder="Ask Saheli anything..."
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                disabled={isTyping}
              />
              <button
                type="submit"
                disabled={isTyping}
                className="px-4 py-2 bg-purple-500 text-white rounded-lg text-sm hover:bg-purple-600 transition-colors disabled:opacity-50"
              >
                💬
              </button>
            </div>
          </form>
        </div>
      )}
    </>
  );
};

export default SaheliChatbot;
