import React, { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { dark } from 'react-syntax-highlighter/dist/esm/styles/prism'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState('connected')
  const [chatHistory, setChatHistory] = useState([
    { id: 1, title: 'Python 助手', time: '2 小时前' },
    { id: 2, title: '浏览器自动化', time: '昨天' },
    { id: 3, title: 'MCP 服务器配置', time: '3 天前' }
  ])
  const [activeChat, setActiveChat] = useState(null)
  const messagesEndRef = useRef(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    // Check API connection
    checkConnection()
  }, [])

  const checkConnection = async () => {
    try {
      const res = await fetch(`${API_URL}/api/health`)
      if (res.ok) {
        setConnectionStatus('connected')
      } else {
        setConnectionStatus('error')
      }
    } catch {
      setConnectionStatus('error')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          history: messages.slice(-10)
        })
      })

      if (!response.ok) throw new Error('API request failed')

      const data = await response.json()

      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString(),
        tools: data.tools || []
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'assistant',
        content: '抱歉，发生了错误。请检查 API 服务是否正常运行。',
        timestamp: new Date().toISOString(),
        isError: true
      }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const newChat = () => {
    setMessages([])
    setActiveChat(null)
  }

  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <div className="logo">🤖</div>
          <div>
            <div className="header-title">MiniMax Agent</div>
            <div className="header-subtitle">AI Agent Platform v1.0</div>
          </div>
        </div>
        <div className="header-right">
          <div className="status-badge">
            <span className={`status-dot ${connectionStatus !== 'connected' ? 'error' : ''}`}></span>
            <span>{connectionStatus === 'connected' ? '服务正常' : '连接断开'}</span>
          </div>
          <button className="btn btn-secondary" onClick={checkConnection}>检查连接</button>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {/* Sidebar */}
        <aside className="sidebar">
          <button className="new-chat-btn" onClick={newChat}>
            <span>➕</span>
            新建对话
          </button>

          <div className="chat-history">
            <div className="chat-history-title">历史对话</div>
            {chatHistory.map(chat => (
              <div
                key={chat.id}
                className={`chat-item ${activeChat === chat.id ? 'active' : ''}`}
                onClick={() => setActiveChat(chat.id)}
              >
                <div className="chat-item-title">{chat.title}</div>
                <div className="chat-item-time">{chat.time}</div>
              </div>
            ))}
          </div>
        </aside>

        {/* Chat Area */}
        <section className="chat-area">
          {messages.length === 0 ? (
            /* Welcome Screen */
            <div className="welcome-screen">
              <div className="welcome-logo">🤖</div>
              <h1 className="welcome-title">欢迎使用 MiniMax Agent</h1>
              <p className="welcome-subtitle">
                一个强大的 AI Agent 平台，基于 Claude Code 构建，支持浏览器自动化、文件操作、Shell 执行等功能
              </p>

              <div className="capabilities">
                <div className="capability-card" onClick={() => setInput('帮我写一个 Python 函数来计算斐波那契数列')}>
                  <div className="capability-icon">🐍</div>
                  <div className="capability-title">代码助手</div>
                  <div className="capability-desc">编写、调试和优化代码</div>
                </div>

                <div className="capability-card" onClick={() => setInput('帮我访问 github.com 并截图')}>
                  <div className="capability-icon">🌐</div>
                  <div className="capability-title">浏览器自动化</div>
                  <div className="capability-desc">网页浏览和数据提取</div>
                </div>

                <div className="capability-card" onClick={() => setInput('帮我分析当前目录的文件结构')}>
                  <div className="capability-icon">📁</div>
                  <div className="capability-title">文件操作</div>
                  <div className="capability-desc">读写和管理文件</div>
                </div>

                <div className="capability-card" onClick={() => setInput('帮我执行 git status 命令')}>
                  <div className="capability-icon">💻</div>
                  <div className="capability-title">Shell 执行</div>
                  <div className="capability-desc">运行命令和脚本</div>
                </div>

                <div className="capability-card" onClick={() => setInput('帮我创建一个 MCP 服务器')}>
                  <div className="capability-icon">🔌</div>
                  <div className="capability-title">MCP 工具</div>
                  <div className="capability-desc">扩展 Agent 能力</div>
                </div>

                <div className="capability-card" onClick={() => setInput('帮我搜索最新的 AI 技术动态')}>
                  <div className="capability-icon">🔍</div>
                  <div className="capability-title">网络搜索</div>
                  <div className="capability-desc">获取最新信息</div>
                </div>
              </div>
            </div>
          ) : (
            <>
              <div className="chat-messages">
                {messages.map(msg => (
                  <div key={msg.id} className="message">
                    <div className={`message-avatar ${msg.role}`}>
                      {msg.role === 'user' ? '👤' : '🤖'}
                    </div>
                    <div className="message-content">
                      <div className="message-header">
                        <span className="message-name">
                          {msg.role === 'user' ? '你' : 'Agent'}
                        </span>
                        <span className="message-time">{formatTime(msg.timestamp)}</span>
                      </div>

                      {msg.tools && msg.tools.length > 0 && msg.tools.map((tool, idx) => (
                        <div key={idx} className="tool-call">
                          <div className="tool-call-header">
                            <span className="tool-call-icon">⚡</span>
                            <span className="tool-call-name">{tool.name}</span>
                            <span>{tool.status || '执行中'}</span>
                          </div>
                          {tool.input && (
                            <code style={{ fontSize: '12px', color: '#94A3B8' }}>
                              {JSON.stringify(tool.input, null, 2)}
                            </code>
                          )}
                        </div>
                      ))}

                      <div className="message-text" style={{ color: msg.isError ? '#EF4444' : undefined }}>
                        <ReactMarkdown
                          components={{
                            code({node, inline, className, children, ...props}) {
                              const match = /language-(\w+)/.exec(className || '')
                              return !inline && match ? (
                                <SyntaxHighlighter
                                  style={dark}
                                  language={match[1]}
                                  PreTag="div"
                                  {...props}
                                >
                                  {String(children).replace(/\n$/, '')}
                                </SyntaxHighlighter>
                              ) : (
                                <code className={className} {...props}>
                                  {children}
                                </code>
                              )
                            }
                          }}
                        >
                          {msg.content}
                        </ReactMarkdown>
                      </div>
                    </div>
                  </div>
                ))}

                {isLoading && (
                  <div className="message">
                    <div className="message-avatar assistant">🤖</div>
                    <div className="message-content">
                      <div className="message-header">
                        <span className="message-name">Agent</span>
                      </div>
                      <div className="typing-indicator">
                        <div className="typing-dot"></div>
                        <div className="typing-dot"></div>
                        <div className="typing-dot"></div>
                      </div>
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>

              <div className="input-area">
                <div className="input-tools">
                  <button className="tool-btn" title="文件上传">
                    📎 文件
                  </button>
                  <button className="tool-btn" title="代码片段">
                    💻 代码
                  </button>
                  <button className="tool-btn" title="图片上传">
                    🖼️ 图片
                  </button>
                </div>

                <form className="input-container" onSubmit={handleSubmit}>
                  <div className="input-wrapper">
                    <textarea
                      ref={textareaRef}
                      className="chat-input"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyDown={handleKeyDown}
                      placeholder="输入消息... (Shift+Enter 换行)"
                      rows={1}
                    />
                  </div>
                  <button
                    type="submit"
                    className="send-btn"
                    disabled={!input.trim() || isLoading}
                  >
                    {isLoading ? '⏳' : '➤'}
                  </button>
                </form>
              </div>
            </>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
