import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import ChatWindow from './components/chat/ChatWindow';
import Overview from './components/dashboard/Overview';
import SchemaExplorer from './components/schema/SchemaExplorer';
import DatabaseHealth from './components/health/DatabaseHealth';

function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-[#0D0D0D] text-[#FAFAFA] font-sans">
      {/* Sidebar */}
      <aside className="w-64 glass-panel border-r border-[#2A2A2A] p-4 flex flex-col gap-4">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-8 h-8 rounded-full bg-[#D4AF37] shadow-[0_0_15px_rgba(212,175,55,0.4)] flex items-center justify-center">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="black" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
          </div>
          <h1 className="text-xl font-heading font-bold text-[#FAFAFA]">Chat Bot</h1>
        </div>
        
        <nav className="flex flex-col gap-2">
          <Link to="/" className="p-3 rounded-lg hover:bg-[#171717] transition-colors border border-transparent hover:border-[#2A2A2A]">Dashboard</Link>
          <Link to="/chat" className="p-3 rounded-lg bg-[#171717] text-[#D4AF37] border border-[#2A2A2A] gold-glow">AI Chat</Link>
          <Link to="/schema" className="p-3 rounded-lg hover:bg-[#171717] transition-colors border border-transparent hover:border-[#2A2A2A]">Schema Explorer</Link>
          <Link to="/health" className="p-3 rounded-lg hover:bg-[#171717] transition-colors border border-transparent hover:border-[#2A2A2A]">Database Health</Link>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col relative overflow-hidden">
        {children}
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppShell>
        <Routes>
          <Route path="/" element={<Overview />} />
          <Route path="/chat" element={<ChatWindow />} />
          <Route path="/schema" element={<SchemaExplorer />} />
          <Route path="/health" element={<DatabaseHealth />} />
        </Routes>
      </AppShell>
    </BrowserRouter>
  );
}

export default App;
