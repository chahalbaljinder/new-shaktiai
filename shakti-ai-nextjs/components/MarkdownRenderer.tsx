'use client'

import React, { ReactNode } from 'react'

interface MarkdownRendererProps {
  content: string
  className?: string
}

export default function MarkdownRenderer({ content, className = '' }: MarkdownRendererProps) {
  // Simple markdown renderer for basic formatting
  const renderMarkdown = (text: string) => {
    // Split text by lines to handle formatting
    const lines = text.split('\n')
    const elements: ReactNode[] = []
    
    for (let i = 0; i < lines.length; i++) {
      let line = lines[i]
      
      // Handle headers
      if (line.startsWith('# ')) {
        elements.push(
          <h1 key={i} className="text-2xl font-bold mb-4 text-gray-900">
            {line.slice(2)}
          </h1>
        )
        continue
      }
      
      if (line.startsWith('## ')) {
        elements.push(
          <h2 key={i} className="text-xl font-bold mb-3 text-gray-900">
            {line.slice(3)}
          </h2>
        )
        continue
      }
      
      if (line.startsWith('### ')) {
        elements.push(
          <h3 key={i} className="text-lg font-bold mb-2 text-gray-900">
            {line.slice(4)}
          </h3>
        )
        continue
      }
      
      // Handle bullet points
      if (line.startsWith('- ') || line.startsWith('* ')) {
        const content = line.slice(2)
        elements.push(
          <div key={i} className="flex items-start mb-1">
            <span className="text-blue-500 mr-2">•</span>
            <span className="flex-1">{renderInlineFormatting(content)}</span>
          </div>
        )
        continue
      }
      
      // Handle numbered lists
      const numberedMatch = line.match(/^(\d+)\.\s(.+)/)
      if (numberedMatch) {
        const [, number, content] = numberedMatch
        elements.push(
          <div key={i} className="flex items-start mb-1">
            <span className="text-blue-500 mr-2">{number}.</span>
            <span className="flex-1">{renderInlineFormatting(content)}</span>
          </div>
        )
        continue
      }
      
      // Handle empty lines
      if (line.trim() === '') {
        elements.push(<br key={i} />)
        continue
      }
      
      // Handle regular paragraphs
      elements.push(
        <p key={i} className="mb-2 leading-relaxed">
          {renderInlineFormatting(line)}
        </p>
      )
    }
    
    return elements
  }
  
  // Handle inline formatting like **bold** and *italic*
  const renderInlineFormatting = (text: string) => {
    const parts: ReactNode[] = []
    let currentIndex = 0
    
    // Handle **bold** formatting
    const boldRegex = /\*\*(.*?)\*\*/g
    let boldMatch
    
    while ((boldMatch = boldRegex.exec(text)) !== null) {
      // Add text before the bold part
      if (boldMatch.index > currentIndex) {
        const beforeText = text.slice(currentIndex, boldMatch.index)
        parts.push(renderItalicFormatting(beforeText, parts.length))
      }
      
      // Add the bold part
      parts.push(
        <strong key={parts.length} className="font-bold text-gray-900">
          {boldMatch[1]}
        </strong>
      )
      
      currentIndex = boldMatch.index + boldMatch[0].length
    }
    
    // Add remaining text
    if (currentIndex < text.length) {
      const remainingText = text.slice(currentIndex)
      parts.push(renderItalicFormatting(remainingText, parts.length))
    }
    
    return parts.length > 0 ? parts : text
  }
  
  // Handle *italic* formatting
  const renderItalicFormatting = (text: string, baseKey: number = 0) => {
    const parts: ReactNode[] = []
    let currentIndex = 0
    
    // Handle *italic* formatting (but not **bold**)
    const italicRegex = /(?<!\*)\*([^*]+)\*(?!\*)/g
    let italicMatch
    
    while ((italicMatch = italicRegex.exec(text)) !== null) {
      // Add text before the italic part
      if (italicMatch.index > currentIndex) {
        parts.push(text.slice(currentIndex, italicMatch.index))
      }
      
      // Add the italic part
      parts.push(
        <em key={`${baseKey}-${parts.length}`} className="italic text-gray-800">
          {italicMatch[1]}
        </em>
      )
      
      currentIndex = italicMatch.index + italicMatch[0].length
    }
    
    // Add remaining text
    if (currentIndex < text.length) {
      parts.push(text.slice(currentIndex))
    }
    
    return parts.length > 0 ? parts : text
  }
  
  return (
    <div className={`prose prose-sm max-w-none ${className}`}>
      {renderMarkdown(content)}
    </div>
  )
}
