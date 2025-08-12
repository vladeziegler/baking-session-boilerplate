"use client"

import type React from "react"
import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { MessageCircle, X, Paperclip, Send, AlertTriangle } from "lucide-react"
import { useAgentStore } from "@/stores/useAgentStore"

export function ChatBot() {
  const [isOpen, setIsOpen] = useState(false)
  const [inputValue, setInputValue] = useState("")
  const fileInputRef = useRef<HTMLInputElement>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const { messages, sendMessage, isSending, error, setError } = useAgentStore()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = () => {
    if (!inputValue.trim()) return
    sendMessage(inputValue)
    setInputValue("")
  }

  const handleFileUpload = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      // This is a placeholder. File upload logic should be implemented.
      console.log("Uploaded file:", file.name)
    }
  }

  return (
    <>
      {/* Chat Toggle Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <Button
          onClick={() => setIsOpen(!isOpen)}
          className="w-14 h-14 rounded-full bg-[#2563eb] hover:bg-[#0ea5e9] text-white shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-110"
        >
          {isOpen ? <X size={24} /> : <MessageCircle size={24} />}
        </Button>
      </div>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 z-40 w-80 h-96">
          <Card className="w-full h-full flex flex-col shadow-2xl border-0 bg-white">
            {/* Header */}
            <div className="bg-[#2563eb] text-white p-4 rounded-t-lg">
              <h3 className="font-semibold">SecureBank Assistant</h3>
              <p className="text-sm opacity-90">We're here to help</p>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {messages.map((message) => (
                <div key={message.id} className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`max-w-[80%] p-3 rounded-lg text-sm ${
                      message.sender === "user" ? "bg-[#2563eb] text-white" : "bg-gray-100 text-[#334155]"
                    }`}
                  >
                    {message.text}
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Error Display */}
            {error && (
              <div className="p-2 text-sm text-red-500 flex items-center gap-2">
                <AlertTriangle size={16} />
                <span>{error}</span>
                <Button variant="ghost" size="sm" onClick={() => setError(null)}>
                  <X size={14} />
                </Button>
              </div>
            )}

            {/* Input Area */}
            <div className="p-4 border-t">
              <div className="flex gap-2">
                <Button variant="outline" size="sm" onClick={handleFileUpload} className="px-3 bg-transparent" disabled={isSending}>
                  <Paperclip size={16} />
                </Button>
                <Input
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Type your message..."
                  onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                  className="flex-1"
                  disabled={isSending}
                />
                <Button
                  onClick={handleSendMessage}
                  size="sm"
                  className="bg-[#2563eb] hover:bg-[#0ea5e9] text-white px-3"
                  disabled={isSending}
                >
                  <Send size={16} />
                </Button>
              </div>
              <input ref={fileInputRef} type="file" onChange={handleFileChange} className="hidden" accept="*/*" disabled={isSending} />
            </div>
          </Card>
        </div>
      )}
    </>
  )
}
