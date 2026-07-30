import { useState, useRef, useEffect } from 'react';
import { Send, Database, Loader2, Code2, LayoutList, Cpu, ChevronDown, ChevronUp, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

type StreamStage = 'understanding' | 'rag_retrieval' | 'schema' | 'planning' | 'generating' | 'validating' | 'executing' | 'formatting' | 'complete' | 'error';

interface RagContext {
  schema_matches?: Array<{ table: string; column?: string; similarity_score: number; description?: string }>;
  golden_sql_matches?: Array<{ question: string; similarity_score: number; sql: string }>;
  resolved_entities?: Array<{ input: string; resolved_value: string; similarity_score: number; field?: string }>;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  stage?: StreamStage;
  stageMessage?: string;
  sql?: string;
  data?: any[];
  rag_context?: RagContext;
}

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [showRagInsights, setShowRagInsights] = useState<Record<string, boolean>>({});
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const toggleRagPanel = (msgId: string) => {
    setShowRagInsights(prev => ({ ...prev, [msgId]: !prev[msgId] }));
  };

  const handleSend = async () => {
    if (!input.trim() || isStreaming) return;
    
    const userMessage: Message = { id: Date.now().toString(), role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsStreaming(true);

    const assistantMsgId = (Date.now() + 1).toString();
    setMessages(prev => [...prev, { id: assistantMsgId, role: 'assistant', content: '', stage: 'understanding', stageMessage: 'Initializing pipeline...' }]);

    try {
      // Check for irrelevant queries
      const irrelevantKeywords = ["joke", "python", "tesla", "match", "capital", "translate", "image"];
      const isIrrelevant = irrelevantKeywords.some(kw => input.toLowerCase().includes(kw));

      if (isIrrelevant) {
        await new Promise(r => setTimeout(r, 600));
        setMessages(prev => prev.map(m => 
          m.id === assistantMsgId ? { 
            ...m, 
            content: "I'm designed specifically to answer questions using your company's connected database. Your current question cannot be answered from the available database because it is not related to the stored business data.\n\nPlease ask a question about your organization's data, such as employees, customers, products, orders, inventory, finance, or sales.",
            stage: 'complete' 
          } : m
        ));
        setIsStreaming(false);
        return;
      }

      // Simulated RAG + Text-to-SQL Pipeline Stages
      const stages = [
        { stage: 'understanding', message: 'Analyzing question intent...' },
        { stage: 'rag_retrieval', message: 'Retrieving semantic schema, golden SQL examples, and entity matches...' },
        { stage: 'schema', message: 'Finding relevant tables and columns...' },
        { stage: 'planning', message: 'Creating query execution plan...' },
        { stage: 'generating', message: 'Generating optimized SQL using Golden Examples...' },
        { stage: 'validating', message: 'Validating SQL against AST security policies...' },
        { stage: 'executing', message: 'Running secure read-only query on database...' },
        { stage: 'formatting', message: 'Formatting results and analyzing...' }
      ];

      for (const step of stages) {
        setMessages(prev => prev.map(m => 
          m.id === assistantMsgId ? { ...m, stage: step.stage as StreamStage, stageMessage: step.message } : m
        ));
        await new Promise(r => setTimeout(r, 450));
      }

      // Simulated RAG Augmented Response
      const finalResponse = {
        answer: `Here is the retrieved data for your query: '${input}'`,
        sql: "SELECT \n  c.name AS customer_name,\n  SUM(o.amount) as total_revenue\nFROM customers c\nJOIN orders o ON c.id = o.customer_id\nGROUP BY c.name\nORDER BY total_revenue DESC\nLIMIT 10;",
        data: [
          { customer_name: "Acme Corp", total_revenue: "$45,200.00" },
          { customer_name: "Global Tech", total_revenue: "$38,150.00" },
          { customer_name: "Apex Innovations", total_revenue: "$29,400.00" }
        ],
        rag_context: {
          schema_matches: [
            { table: "orders", column: "amount", similarity_score: 0.91, description: "Order sales revenue value" },
            { table: "customers", column: "name", similarity_score: 0.87, description: "Customer name" }
          ],
          golden_sql_matches: [
            { question: "Show top revenue customers", similarity_score: 0.93, sql: "SELECT c.name, SUM(o.amount)..." }
          ],
          resolved_entities: [
            { input: "Hyd", resolved_value: "Hyderabad", similarity_score: 0.95, field: "customers.city" }
          ]
        }
      };
      
      setMessages(prev => prev.map(m => 
        m.id === assistantMsgId ? { 
          ...m, 
          content: finalResponse.answer, 
          sql: finalResponse.sql, 
          data: finalResponse.data, 
          rag_context: finalResponse.rag_context,
          stage: 'complete' 
        } : m
      ));
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
          <p className="text-sm text-gray-400">Hybrid RAG + Text-to-SQL Enterprise Retrieval Engine</p>
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
                  <p className="text-[#FAFAFA] leading-relaxed whitespace-pre-line">{msg.content}</p>
                  
                  {/* Collapsible RAG Context Insights Panel */}
                  {msg.rag_context && (
                    <div className="bg-[#050505] border border-[#2A2A2A] rounded-lg overflow-hidden">
                      <button 
                        onClick={() => toggleRagPanel(msg.id)}
                        className="w-full flex items-center justify-between bg-[#111] px-4 py-2 text-xs font-mono text-[#D4AF37] hover:bg-[#161616] transition-colors"
                      >
                        <span className="flex items-center gap-2">
                          <Sparkles size={14} /> RAG CONTEXT INSIGHTS (Vector Similarity Matches)
                        </span>
                        {showRagInsights[msg.id] ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                      </button>

                      {showRagInsights[msg.id] && (
                        <div className="p-4 space-y-4 text-xs font-mono text-gray-300 bg-[#0A0A0A] border-t border-[#2A2A2A]">
                          {/* Schema Matches */}
                          {msg.rag_context.schema_matches && msg.rag_context.schema_matches.length > 0 && (
                            <div>
                              <div className="text-gray-400 font-semibold mb-1 uppercase tracking-wider flex items-center gap-1">
                                <Cpu size={12} className="text-[#D4AF37]" /> Schema Vector Matches:
                              </div>
                              <ul className="space-y-1 pl-4">
                                {msg.rag_context.schema_matches.map((sm, i) => (
                                  <li key={i} className="flex justify-between">
                                    <span>• {sm.table}{sm.column ? `.${sm.column}` : ''} {sm.description ? `(${sm.description})` : ''}</span>
                                    <span className="text-[#D4AF37] font-bold">score: {sm.similarity_score}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {/* Golden SQL Examples */}
                          {msg.rag_context.golden_sql_matches && msg.rag_context.golden_sql_matches.length > 0 && (
                            <div>
                              <div className="text-gray-400 font-semibold mb-1 uppercase tracking-wider flex items-center gap-1">
                                <Code2 size={12} className="text-[#D4AF37]" /> Golden SQL Few-Shot Matches:
                              </div>
                              <ul className="space-y-1 pl-4">
                                {msg.rag_context.golden_sql_matches.map((gm, i) => (
                                  <li key={i} className="flex justify-between">
                                    <span>• "{gm.question}"</span>
                                    <span className="text-[#D4AF37] font-bold">score: {gm.similarity_score}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {/* Entity Matches */}
                          {msg.rag_context.resolved_entities && msg.rag_context.resolved_entities.length > 0 && (
                            <div>
                              <div className="text-gray-400 font-semibold mb-1 uppercase tracking-wider flex items-center gap-1">
                                <Database size={12} className="text-[#D4AF37]" /> Resolved Entity Matches:
                              </div>
                              <ul className="space-y-1 pl-4">
                                {msg.rag_context.resolved_entities.map((em, i) => (
                                  <li key={i} className="flex justify-between">
                                    <span>• '{em.input}' → '{em.resolved_value}' {em.field ? `(${em.field})` : ''}</span>
                                    <span className="text-[#D4AF37] font-bold">score: {em.similarity_score}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  )}

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
            placeholder="Ask a question about your data... (e.g. 'Show top revenue customers')"
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
