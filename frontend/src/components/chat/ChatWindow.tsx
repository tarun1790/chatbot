import React, { useState, useRef, useEffect } from 'react';
import { Send, Database, Loader2, Play, Code2, LayoutList } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

type StreamStage = 'understanding' | 'schema' | 'planning' | 'generating' | 'validating' | 'executing' | 'formatting' | 'complete' | 'error';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  stage?: StreamStage;
  stageMessage?: string;
  sql?: string;
  data?: any[];
}

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isStreaming) return;
    
    const userMessage: Message = { id: Date.now().toString(), role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsStreaming(true);

    const assistantMsgId = (Date.now() + 1).toString();
    setMessages(prev => [...prev, { id: assistantMsgId, role: 'assistant', content: '', stage: 'understanding', stageMessage: 'Initializing pipeline...' }]);

    try {
      // Initiate SSE Stream to backend
      const response = await fetch('http://localhost:8000/api/v1/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input, session_id: "demo-session" })
      });

      if (!response.body) throw new Error("No response body");
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter(line => line.trim() !== '');
        
        for (const line of lines) {
          if (line.startsWith('event: ')) {
            // handle event type
          } else if (line.startsWith('data: ')) {
            const dataStr = line.substring(6);
            try {
              const data = JSON.parse(dataStr);
              if (data.stage === 'complete') {
                 setMessages(prev => prev.map(m => 
                  m.id === assistantMsgId ? { ...m, content: data.answer, sql: data.sql, data: data.data, stage: 'complete' } : m
                ));
              } else {
                 setMessages(prev => prev.map(m => 
                  m.id === assistantMsgId ? { ...m, stage: data.stage, stageMessage: data.message } : m
                ));
              }
            } catch (e) {
              console.error("Error parsing SSE data", e);
            }
          }
        }
      }
    } catch (error) {
      setMessages(prev => prev.map(m => 
        m.id === assistantMsgId ? { ...m, stage: 'error', stageMessage: 'Pipeline failed to execute.' } : m
      ));
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-[#0D0D0D]">
      {/* Header */}
      <header className="px-6 py-4 border-b border-[#2A2A2A] glass-panel z-10 flex justify-between items-center">
        <div>
          <h2 className="text-xl font-heading font-semibold text-[#FAFAFA]">AI Data Analyst</h2>
          <p className="text-sm text-gray-400">Query your enterprise database in natural language</p>
        </div>
        <div className="flex items-center gap-2 text-sm text-[#D4AF37] bg-[#171717] px-3 py-1.5 rounded-full border border-[#2A2A2A]">
          <Database size={14} /> MySQL Connected
        </div>
      </header>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg) => (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            key={msg.id} 
            className={`flex flex-col max-w-4xl ${msg.role === 'user' ? 'ml-auto items-end' : 'mr-auto items-start'}`}
          >
            <div className={`p-4 rounded-2xl ${msg.role === 'user' ? 'bg-[#D4AF37] text-black font-medium rounded-tr-none' : 'glass-panel rounded-tl-none w-full'}`}>
              {msg.role === 'assistant' && msg.stage !== 'complete' && msg.stage !== 'error' && (
                <div className="flex items-center gap-3 text-[#D4AF37] mb-2 font-mono text-sm">
                  <Loader2 className="animate-spin" size={16} />
                  <span className="uppercase tracking-wider">{msg.stageMessage}</span>
                </div>
              )}
              
              {msg.role === 'assistant' && msg.stage === 'complete' && (
                <div className="flex flex-col gap-4 w-full">
                  <p className="text-[#FAFAFA] leading-relaxed">{msg.content}</p>
                  
                  {msg.sql && (
                    <div className="bg-[#050505] border border-[#2A2A2A] rounded-lg overflow-hidden">
                      <div className="flex items-center justify-between bg-[#111] px-4 py-2 border-b border-[#2A2A2A]">
                        <span className="text-xs text-gray-400 font-mono flex items-center gap-2"><Code2 size={14} /> GENERATED SQL</span>
                      </div>
                      <pre className="p-4 text-sm font-mono text-[#D4AF37] overflow-x-auto">
                        {msg.sql}
                      </pre>
                    </div>
                  )}

                  {msg.data && msg.data.length > 0 && (
                     <div className="bg-[#050505] border border-[#2A2A2A] rounded-lg overflow-hidden">
                       <div className="flex items-center justify-between bg-[#111] px-4 py-2 border-b border-[#2A2A2A]">
                        <span className="text-xs text-gray-400 font-mono flex items-center gap-2"><LayoutList size={14} /> RESULTS ({msg.data.length} rows)</span>
                      </div>
                      <div className="p-4 overflow-x-auto">
                        <table className="w-full text-sm text-left">
                          <thead className="text-xs uppercase text-gray-400 border-b border-[#2A2A2A]">
                            <tr>
                              {Object.keys(msg.data[0]).map(k => <th key={k} className="px-4 py-2">{k}</th>)}
                            </tr>
                          </thead>
                          <tbody>
                            {msg.data.map((row, i) => (
                              <tr key={i} className="border-b border-[#2A2A2A]/50 hover:bg-[#111]">
                                {Object.values(row).map((val: any, j) => <td key={j} className="px-4 py-2">{String(val)}</td>)}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                     </div>
                  )}
                </div>
              )}
              
              {msg.role === 'user' && <span>{msg.content}</span>}
            </div>
          </motion.div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-6 bg-[#0D0D0D] border-t border-[#2A2A2A]">
        <div className="max-w-4xl mx-auto relative flex items-center">
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask a question about your data... (e.g. 'Show total sales for Q3')"
            className="w-full glass-panel bg-[#111] text-[#FAFAFA] rounded-full py-4 pl-6 pr-16 focus:outline-none focus:border-[#D4AF37] focus:ring-1 focus:ring-[#D4AF37] transition-all placeholder-gray-500"
            disabled={isStreaming}
          />
          <button 
            onClick={handleSend}
            disabled={isStreaming || !input.trim()}
            className="absolute right-2 p-3 bg-[#D4AF37] text-black rounded-full hover:bg-yellow-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
