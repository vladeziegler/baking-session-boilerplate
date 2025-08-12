import { create } from "zustand"
import { v4 as uuidv4 } from "uuid"
import { persist, createJSONStorage } from "zustand/middleware"

const API_URL = "http://localhost:8000"

interface Message {
  id: string
  text: string
  sender: "user" | "bot"
  timestamp: Date
}

interface AgentState {
  messages: Message[]
  sessionId: string
  isSending: boolean
  error: string | null
  addMessage: (message: Message) => void
  sendMessage: (text: string) => Promise<void>
  setError: (error: string | null) => void
}

export const useAgentStore = create<AgentState>()(
  persist(
    (set, get) => ({
      messages: [
        {
          id: uuidv4(),
          text: "How can I help you with your banking needs today?",
          sender: "bot",
          timestamp: new Date(),
        },
      ],
      sessionId: uuidv4(),
      isSending: false,
      error: null,

      addMessage: (message) =>
        set((state) => ({ messages: [...state.messages, message] })),

      sendMessage: async (text) => {
        const { sessionId, addMessage } = get()
        set({ isSending: true, error: null })

        const userMessage: Message = {
          id: uuidv4(),
          text,
          sender: "user",
          timestamp: new Date(),
        }
        addMessage(userMessage)

        try {
          const response = await fetch(`${API_URL}/chat/stream`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              session_id: sessionId,
              user_input: text,
            }),
          })

          if (!response.body) {
            throw new Error("Response body is null")
          }

          const reader = response.body.getReader()
          const decoder = new TextDecoder()
          let botMessage: Message | null = null

          while (true) {
            const { done, value } = await reader.read()
            if (done) break

            const chunk = decoder.decode(value, { stream: true })
            const lines = chunk.split("\n").filter((line) => line.trim())

            for (const line of lines) {
              try {
                const event = JSON.parse(line)

                if (event.event_type === "FINAL_RESPONSE" && event.data.text) {
                  const botText = event.data.text

                  if (botMessage) {
                    botMessage.text += botText;
                    set((state) => ({
                      messages: state.messages.map((m) =>
                        m.id === botMessage!.id ? botMessage! : m
                      ),
                    }));
                  } else {
                    botMessage = {
                      id: uuidv4(),
                      text: botText,
                      sender: "bot",
                      timestamp: new Date(),
                    };
                    addMessage(botMessage);
                  }
                } else if (event.event_type === "ERROR") {
                  throw new Error(event.data.message);
                }
              } catch (e) {
                console.error("Error processing stream event:", e)
              }
            }
          }
        } catch (error) {
          const errorMessage =
            error instanceof Error ? error.message : "An unknown error occurred"
          set({ error: errorMessage })
          addMessage({
            id: uuidv4(),
            text: `Error: ${errorMessage}`,
            sender: "bot",
            timestamp: new Date(),
          })
        } finally {
          set({ isSending: false })
        }
      },

      setError: (error) => set({ error }),
    }),
    {
      name: "agent-storage",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ sessionId: state.sessionId }),
    }
  )
)
