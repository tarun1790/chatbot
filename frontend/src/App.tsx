import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import ChatWindow from './components/chat/ChatWindow';

function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-[#0D0D0D] text-[#FAFAFA] font-sans">
      {/* Sidebar */}
      <aside className="w-64 glass-panel border-r border-[#2A2A2A] p-4 flex flex-col gap-4">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-8 h-8 rounded-full bg-[#D4AF37] shadow-[0_0_15px_rgba(212,175,55,0.4)]"></div>
          <h1 className="text-xl font-heading font-bold text-[#FAFAFA]">Enterprise SQL</h1>
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
          <Route path="/" element={<div className="p-8"><h2 className="text-3xl font-heading font-bold mb-4">Dashboard Overview</h2><div className="grid grid-cols-3 gap-6"><div className="glass-panel p-6 rounded-xl"><h3>Total Queries</h3><p className="text-3xl text-[#D4AF37] mt-2">1,248</p></div></div></div>} />
          <Route path="/chat" element={<ChatWindow />} />
          <Route path="/schema" element={<div className="p-8">Schema Explorer Content</div>} />
          <Route path="/health" element={<div className="p-8">Database Health Content</div>} />
        </Routes>
      </AppShell>
    </BrowserRouter>
  );
}

export default App;
