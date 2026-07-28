import { Activity, Server, Database as DbIcon, ShieldCheck, HardDrive, Cpu, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';

export default function DatabaseHealth() {
  const nodes = [
    { name: 'Primary MySQL (Write)', status: 'healthy', cpu: '45%', memory: '12.4 GB', latency: '4ms', uptime: '99.99%' },
    { name: 'Replica 01 (Read)', status: 'healthy', cpu: '22%', memory: '8.1 GB', latency: '6ms', uptime: '99.99%' },
    { name: 'Replica 02 (Read)', status: 'warning', cpu: '88%', memory: '15.9 GB', latency: '42ms', uptime: '99.95%' },
    { name: 'Redis Cache Layer', status: 'healthy', cpu: '12%', memory: '4.2 GB', latency: '1ms', uptime: '100%' },
  ];

  return (
    <div className="p-8 h-full flex flex-col">
      <div className="flex justify-between items-end mb-8">
        <div>
          <h2 className="text-3xl font-heading font-bold text-[#FAFAFA]">Database Health</h2>
          <p className="text-gray-400 mt-2">Live monitoring of infrastructure and connections</p>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-900/20 text-green-400 border border-green-900/50 text-sm font-medium">
          <ShieldCheck size={16} /> All Systems Operational
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {/* Connection Pool */}
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass-panel p-6 rounded-xl border border-[#2A2A2A]"
        >
          <div className="flex items-center gap-3 mb-6">
            <Activity className="text-[#D4AF37]" size={24} />
            <h3 className="text-xl font-heading font-semibold text-[#FAFAFA]">Connection Pool</h3>
          </div>
          
          <div className="space-y-6">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-400">Active Connections</span>
                <span className="text-[#FAFAFA] font-medium">42 / 100</span>
              </div>
              <div className="w-full bg-[#111] rounded-full h-2 border border-[#2A2A2A]">
                <div className="bg-[#D4AF37] h-1.5 rounded-full" style={{ width: '42%' }}></div>
              </div>
            </div>
            
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-400">Thread Cache Hit Rate</span>
                <span className="text-[#FAFAFA] font-medium">98.5%</span>
              </div>
              <div className="w-full bg-[#111] rounded-full h-2 border border-[#2A2A2A]">
                <div className="bg-green-500 h-1.5 rounded-full" style={{ width: '98.5%' }}></div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Global Status */}
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass-panel p-6 rounded-xl border border-[#2A2A2A]"
        >
          <div className="flex items-center gap-3 mb-6">
            <Server className="text-[#D4AF37]" size={24} />
            <h3 className="text-xl font-heading font-semibold text-[#FAFAFA]">Security Gateway</h3>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-[#111] p-4 rounded-lg border border-[#2A2A2A]">
              <div className="text-gray-400 text-xs uppercase mb-1">Blocked Queries (24h)</div>
              <div className="text-2xl font-bold text-red-400">14</div>
            </div>
            <div className="bg-[#111] p-4 rounded-lg border border-[#2A2A2A]">
              <div className="text-gray-400 text-xs uppercase mb-1">AST Validation Fails</div>
              <div className="text-2xl font-bold text-yellow-400">3</div>
            </div>
            <div className="bg-[#111] p-4 rounded-lg border border-[#2A2A2A]">
              <div className="text-gray-400 text-xs uppercase mb-1">Avg AI Generation Time</div>
              <div className="text-2xl font-bold text-[#FAFAFA]">1.2s</div>
            </div>
            <div className="bg-[#111] p-4 rounded-lg border border-[#2A2A2A]">
              <div className="text-gray-400 text-xs uppercase mb-1">Schema Cache Sync</div>
              <div className="text-2xl font-bold text-green-400">Synced</div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Cluster Nodes Table */}
      <h3 className="text-xl font-heading font-semibold text-[#FAFAFA] mb-4">Infrastructure Cluster</h3>
      <div className="glass-panel border border-[#2A2A2A] rounded-xl overflow-hidden">
        <table className="w-full text-sm text-left">
          <thead className="text-xs uppercase text-gray-400 bg-[#0A0A0A] border-b border-[#2A2A2A]">
            <tr>
              <th className="px-6 py-4">Node Identity</th>
              <th className="px-6 py-4">Status</th>
              <th className="px-6 py-4"><Cpu size={14} className="inline mr-1"/> CPU</th>
              <th className="px-6 py-4"><HardDrive size={14} className="inline mr-1"/> Memory</th>
              <th className="px-6 py-4">Latency</th>
              <th className="px-6 py-4">Uptime</th>
            </tr>
          </thead>
          <tbody>
            {nodes.map((node, i) => (
              <tr key={i} className="border-b border-[#2A2A2A]/50 hover:bg-[#111] transition-colors">
                <td className="px-6 py-4 font-medium text-[#FAFAFA] flex items-center gap-2">
                  <DbIcon size={16} className="text-[#D4AF37]" /> {node.name}
                </td>
                <td className="px-6 py-4">
                  {node.status === 'healthy' ? (
                    <span className="flex items-center gap-1 text-green-400"><div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div> Healthy</span>
                  ) : (
                    <span className="flex items-center gap-1 text-yellow-400"><AlertTriangle size={14} /> Warning</span>
                  )}
                </td>
                <td className="px-6 py-4 text-gray-300">{node.cpu}</td>
                <td className="px-6 py-4 text-gray-300">{node.memory}</td>
                <td className="px-6 py-4 font-mono text-gray-400">{node.latency}</td>
                <td className="px-6 py-4 text-gray-300">{node.uptime}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
