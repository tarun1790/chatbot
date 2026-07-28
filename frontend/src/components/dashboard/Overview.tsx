import { Activity, Users, Database, Zap, Clock } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Overview() {
  const stats = [
    { title: 'Total Queries (24h)', value: '1,248', change: '+12%', icon: <Activity size={20} className="text-[#D4AF37]" /> },
    { title: 'Avg Latency', value: '240ms', change: '-5%', icon: <Zap size={20} className="text-[#D4AF37]" /> },
    { title: 'Active Users', value: '42', change: '+3', icon: <Users size={20} className="text-[#D4AF37]" /> },
    { title: 'Data Processed', value: '18.4 GB', change: '+2.1 GB', icon: <Database size={20} className="text-[#D4AF37]" /> },
  ];

  const recentQueries = [
    { id: 1, user: 'Sarah J.', query: 'Show sales for the last quarter', time: '2 min ago', status: 'success' },
    { id: 2, user: 'Mike T.', query: 'Top 10 customers by revenue', time: '15 min ago', status: 'success' },
    { id: 3, user: 'Alex W.', query: 'Which employees joined in 2025?', time: '1 hour ago', status: 'success' },
    { id: 4, user: 'Emma R.', query: 'DROP TABLE orders', time: '2 hours ago', status: 'blocked' },
  ];

  return (
    <div className="p-8 h-full overflow-y-auto">
      <div className="flex justify-between items-end mb-8">
        <div>
          <h2 className="text-3xl font-heading font-bold text-[#FAFAFA]">Dashboard Overview</h2>
          <p className="text-gray-400 mt-2">Real-time telemetry and query analytics</p>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-400">
          <Clock size={16} /> Last updated: Just now
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, i) => (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            key={i} 
            className="glass-panel p-6 rounded-xl border border-[#2A2A2A] hover:border-[#D4AF37]/50 transition-colors"
          >
            <div className="flex justify-between items-start mb-4">
              <div className="p-2 bg-[#111] rounded-lg border border-[#2A2A2A]">{stat.icon}</div>
              <span className={`text-sm font-medium ${stat.change.startsWith('+') && stat.title !== 'Avg Latency' ? 'text-green-400' : 'text-green-400'}`}>
                {stat.change}
              </span>
            </div>
            <h3 className="text-gray-400 text-sm mb-1">{stat.title}</h3>
            <p className="text-3xl font-bold text-[#FAFAFA]">{stat.value}</p>
          </motion.div>
        ))}
      </div>

      {/* Recent Activity Table */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="glass-panel rounded-xl border border-[#2A2A2A] overflow-hidden"
      >
        <div className="p-6 border-b border-[#2A2A2A]">
          <h3 className="text-lg font-heading font-semibold text-[#FAFAFA]">Recent Query Activity</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs uppercase text-gray-400 bg-[#0A0A0A] border-b border-[#2A2A2A]">
              <tr>
                <th className="px-6 py-4">User</th>
                <th className="px-6 py-4">Natural Language Query</th>
                <th className="px-6 py-4">Time</th>
                <th className="px-6 py-4">Status</th>
              </tr>
            </thead>
            <tbody>
              {recentQueries.map((q) => (
                <tr key={q.id} className="border-b border-[#2A2A2A]/50 hover:bg-[#111] transition-colors">
                  <td className="px-6 py-4 font-medium text-[#FAFAFA]">{q.user}</td>
                  <td className="px-6 py-4 text-gray-300 font-mono text-xs">{q.query}</td>
                  <td className="px-6 py-4 text-gray-500">{q.time}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2.5 py-1 rounded-full text-xs font-medium border ${
                      q.status === 'success' 
                        ? 'bg-green-900/20 text-green-400 border-green-900/50' 
                        : 'bg-red-900/20 text-red-400 border-red-900/50'
                    }`}>
                      {q.status === 'success' ? 'EXECUTED' : 'BLOCKED BY SECURITY'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  );
}
