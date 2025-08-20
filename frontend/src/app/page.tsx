'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'

interface SystemStatus {
  docs_processed: boolean
  vector_store_ready: boolean
  retriever_ready: boolean
  rag_chain_ready: boolean
  memory_ready: boolean
}

interface ProcessResponse {
  message: string
  success: boolean
  document_count?: number
}

interface AnswerResponse {
  answer: string
  success: boolean
}

interface ChatMessage {
  question: string
  answer: string
  timestamp: string
}

export default function Home() {
  const [status, setStatus] = useState<SystemStatus | null>(null)
  const [loading, setLoading] = useState(false)
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [processing, setProcessing] = useState(false)
  const [message, setMessage] = useState('')
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([])
  const [sidebarOpen, setSidebarOpen] = useState(false)

  // Check system status on component mount
  useEffect(() => {
    checkStatus()
    loadChatHistory()
  }, [])

  // Close sidebar when clicking outside on mobile
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (sidebarOpen && window.innerWidth < 1024) {
        const sidebar = document.getElementById('sidebar')
        const target = event.target as Node
        
        // Check if click is outside sidebar and not on the menu button
        if (sidebar && !sidebar.contains(target)) {
          setSidebarOpen(false)
        }
      }
    }

    const handleEscapeKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && sidebarOpen) {
        setSidebarOpen(false)
      }
    }

    // Add event listener only when sidebar is open
    if (sidebarOpen) {
      document.addEventListener('mousedown', handleClickOutside)
      document.addEventListener('keydown', handleEscapeKey)
      // Prevent body scroll on mobile
      document.body.style.overflow = 'hidden'
    } else {
      // Restore body scroll
      document.body.style.overflow = 'unset'
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
      document.removeEventListener('keydown', handleEscapeKey)
      document.body.style.overflow = 'unset'
    }
  }, [sidebarOpen])

  const loadChatHistory = async () => {
    try {
      const response = await axios.get('/api/chat-history')
      setChatHistory(response.data.chat_history || [])
    } catch (error) {
      console.error('Error loading chat history:', error)
    }
  }

  const clearChatHistory = async () => {
    try {
      await axios.delete('/api/chat-history')
      setChatHistory([])
      setMessage('✅ Chat history cleared')
    } catch (error) {
      setMessage('❌ Error clearing chat history')
    }
  }

  const checkStatus = async () => {
    try {
      const response = await axios.get('/api/status')
      setStatus(response.data)
    } catch (error) {
      console.error('Error checking status:', error)
    }
  }

  const processDocuments = async () => {
    setProcessing(true)
    setMessage('')
    try {
      const response = await axios.post<ProcessResponse>('/api/process-documents')
      if (response.data.success) {
        setMessage(`✅ ${response.data.message}`)
        await checkStatus() // Refresh status
      }
    } catch (error: any) {
      setMessage(`❌ Error: ${error.response?.data?.detail || error.message}`)
    } finally {
      setProcessing(false)
    }
  }

  const reprocessDocuments = async () => {
    setProcessing(true)
    setMessage('')
    try {
      const response = await axios.post<ProcessResponse>('/api/reprocess-documents')
      if (response.data.success) {
        setMessage(`✅ ${response.data.message}`)
        await checkStatus() // Refresh status
      }
    } catch (error: any) {
      setMessage(`❌ Error: ${error.response?.data?.detail || error.message}`)
    } finally {
      setProcessing(false)
    }
  }

  const askQuestion = async () => {
    if (!question.trim()) return
    
    setLoading(true)
    setAnswer('')
    try {
      const response = await axios.post<AnswerResponse>('/api/ask-question', {
        question: question.trim()
      })
      if (response.data.success) {
        setAnswer(response.data.answer)
        // Refresh chat history
        await loadChatHistory()
      }
    } catch (error: any) {
      setAnswer(`❌ Error: ${error.response?.data?.detail || error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <h1 className="text-3xl font-bold text-gray-900">
              🇪🇹 Ethio Startup Advisor ��
            </h1>
            
            {/* Mobile menu button */}
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="lg:hidden inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary"
            >
              <span className="sr-only">Open sidebar</span>
              {sidebarOpen ? (
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* App Description */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="text-center py-6 px-4 bg-primary text-white rounded-lg mb-8">
          <h4 className="text-xl font-semibold mb-2">
            🚀 Get instant, accurate answers about Ethiopian business registration, licensing, and investment rules
          </h4>
          <p className="text-lg">
            <strong>Directly from official government proclamations and legal codes</strong>
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div 
            id="sidebar"
            className={`lg:col-span-1 ${
              sidebarOpen 
                ? 'fixed inset-0 z-50 lg:relative lg:inset-auto' 
                : 'hidden lg:block'
            }`}
          >
            {/* Mobile overlay */}
            {sidebarOpen && (
              <div 
                className="fixed inset-0 bg-gray-600 bg-opacity-75 lg:hidden z-40"
                onClick={() => setSidebarOpen(false)}
              />
            )}
            
            {/* Sidebar content */}
            <div className={`relative h-full ${
              sidebarOpen 
                ? 'fixed inset-y-0 left-0 z-50 w-80 bg-white shadow-xl lg:relative lg:inset-auto lg:w-auto lg:shadow-none' 
                : ''
            }`}>
              <div className="bg-white rounded-lg shadow p-6 h-full overflow-y-auto">
                {/* Mobile close button */}
                <div className="flex justify-between items-center mb-4 lg:hidden">
                  <h2 className="text-xl font-semibold text-gray-900">
                    📂 Ethio Startup Advisor
                  </h2>
                  <button
                    onClick={() => setSidebarOpen(false)}
                    className="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
                  >
                    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
                
                {/* Desktop title (hidden on mobile) */}
                <h2 className="text-xl font-semibold text-gray-900 mb-4 hidden lg:block">
                  📂 Ethio Startup Advisor
                </h2>

              {/* Status */}
              {status?.docs_processed ? (
                <div className="mb-6">
                  <div className="bg-green-50 border border-green-200 rounded-md p-4 mb-4">
                    <div className="flex">
                      <div className="flex-shrink-0">
                        <div className="w-5 h-5 bg-green-400 rounded-full flex items-center justify-center">
                          <span className="text-white text-sm">✅</span>
                        </div>
                      </div>
                      <div className="ml-3">
                        <h3 className="text-sm font-medium text-green-800">
                          Legal Advisor Ready
                        </h3>
                        <p className="text-sm text-green-700 mt-1">
                          Ask questions about Ethiopian business law!
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Legal Sources */}
                  <div className="mb-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-3">
                      📚 Legal Sources:
                    </h3>
                    <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
                      <ul className="text-sm text-blue-800 space-y-1">
                        <li>• Ethiopian Commercial Code (2021)</li>
                        <li>• Investment Proclamation No. 1180/2020</li>
                        <li>• Trade Registration Proclamation No. 980/2016</li>
                        <li>• Tax Proclamations</li>
                      </ul>
                    </div>
                  </div>

                  {/* Reprocess Button */}
                  <button
                    onClick={reprocessDocuments}
                    disabled={processing}
                    className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed mb-4"
                  >
                    {processing ? '🔄 Reprocessing...' : '🔄 Reprocess Documents'}
                  </button>

                  {/* Chat History */}
                  {chatHistory.length > 0 && (
                    <div className="mb-6">
                      <div className="flex justify-between items-center mb-3">
                        <h3 className="text-lg font-medium text-gray-900">
                          💬 Recent Questions
                        </h3>
                        <button
                          onClick={clearChatHistory}
                          className="text-sm text-red-600 hover:text-red-800"
                        >
                          Clear
                        </button>
                      </div>
                      <div className="space-y-3 max-h-60 overflow-y-auto">
                        {chatHistory.slice(-5).reverse().map((chat, index) => (
                          <div key={index} className="bg-gray-50 rounded-md p-3">
                            <p className="text-sm font-medium text-gray-900 mb-1">
                              {chat.question}
                            </p>
                            <p className="text-xs text-gray-600">
                              {new Date(chat.timestamp).toLocaleTimeString()}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="mb-6">
                  <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
                    <p className="text-sm text-yellow-800">
                      No knowledge base found. Process documents to get started.
                    </p>
                  </div>
                </div>
              )}

              {/* Process Documents Button */}
              <button
                onClick={processDocuments}
                disabled={processing}
                className="w-full bg-primary text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {processing ? '📚 Processing...' : '📚 Process Documents'}
              </button>

              {/* Status Message */}
              {message && (
                <div className="mt-4 p-3 rounded-md bg-blue-50 border border-blue-200">
                  <p className="text-sm text-blue-800">{message}</p>
                </div>
              )}
            </div>
            </div>
          </div>

          {/* Main Content */}
          <div className={`lg:col-span-3 ${sidebarOpen ? 'hidden lg:block' : 'block'}`}>
            {/* Q&A Section */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                💬 Ask Your Startup Questions
              </h2>

              {status?.docs_processed ? (
                <>
                  <div className="bg-green-50 border border-green-200 rounded-md p-4 mb-6">
                    <div className="flex">
                      <div className="flex-shrink-0">
                        <div className="w-5 h-5 bg-green-400 rounded-full flex items-center justify-center">
                          <span className="text-white text-sm">🚀</span>
                        </div>
                      </div>
                      <div className="ml-3">
                        <h3 className="text-sm font-medium text-green-800">
                          Ready to Advise!
                        </h3>
                        <p className="text-sm text-green-700 mt-1">
                          Ask me anything about Ethiopian startups, business registration, or entrepreneurship.
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Common Questions */}
                  <div className="mb-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-3">
                      🔍 Common Questions You Can Ask:
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-medium text-gray-900 mb-2">🏢 Business Registration:</h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          <li>• How do I register a private limited company?</li>
                          <li>• What's the minimum capital requirement?</li>
                          <li>• What documents do I need?</li>
                        </ul>
                        <h4 className="font-medium text-gray-900 mb-2 mt-3">📋 Licensing & Permits:</h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          <li>• How do I get a trade license?</li>
                        </ul>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900 mb-2">🌍 Foreign Investment:</h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          <li>• What are the foreign investment rules?</li>
                          <li>• Can foreigners own 100% of a company?</li>
                          <li>• What sectors are open to foreigners?</li>
                        </ul>
                        <h4 className="font-medium text-gray-900 mb-2 mt-3">💰 Tax & Compliance:</h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          <li>• What are the tax obligations for startups?</li>
                          <li>• When do I need to register for VAT?</li>
                        </ul>
                      </div>
                    </div>
                  </div>

                  {/* Question Input */}
                  <div className="mb-6">
                    <label htmlFor="question" className="block text-sm font-medium text-gray-700 mb-2">
                      💭 Ask your startup question:
                    </label>
                    <input
                      type="text"
                      id="question"
                      value={question}
                      onChange={(e) => setQuestion(e.target.value)}
                      placeholder="e.g., What's the minimum capital for a private limited company?"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                      onKeyPress={(e) => e.key === 'Enter' && askQuestion()}
                    />
                  </div>

                  {/* Ask Button */}
                  <button
                    onClick={askQuestion}
                    disabled={loading || !question.trim()}
                    className="bg-primary text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed mb-6"
                  >
                    {loading ? '🤔 Searching...' : 'Ask Question'}
                  </button>

                  {/* Answer Display */}
                  {answer && (
                    <div className="border-t pt-6">
                      <h3 className="text-lg font-medium text-gray-900 mb-3">
                        📋 Answer:
                      </h3>
                      <div className="bg-gray-50 rounded-md p-4">
                        <div className="prose max-w-none markdown-content">
                          <ReactMarkdown>{answer}</ReactMarkdown>
                        </div>
                      </div>
                      <div className="mt-4 p-3 rounded-md bg-blue-50 border border-blue-200">
                        <p className="text-sm text-blue-800">
                          💡 <strong>Tip:</strong> Ask follow-up questions about your startup journey in Ethiopia!
                        </p>
                      </div>
                    </div>
                  )}
                </>
              ) : (
                <div className="text-center py-12">
                  <div className="bg-yellow-50 border border-yellow-200 rounded-md p-6">
                    <h3 className="text-lg font-medium text-yellow-800 mb-2">
                      ⚠️ Legal Advisor Not Ready
                    </h3>
                    <p className="text-yellow-700">
                      Please load your Ethiopian legal documents first using the sidebar. Once loaded, I'll be ready to advise you on business registration and compliance.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
