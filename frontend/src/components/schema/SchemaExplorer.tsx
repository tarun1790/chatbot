import { useState } from 'react';
import { Database, Search, Key, Type, ChevronRight } from 'lucide-react';
import { motion } from 'framer-motion';

const MOCK_SCHEMA = [
  {
    name: 'customers',
    description: 'Core customer data and demographics',
    columns: [
      { name: 'id', type: 'INT', isPrimary: true },
      { name: 'name', type: 'VARCHAR(255)', isPrimary: false },
      { name: 'email', type: 'VARCHAR(255)', isPrimary: false },
      { name: 'city', type: 'VARCHAR(100)', isPrimary: false },
      { name: 'created_at', type: 'TIMESTAMP', isPrimary: false },
    ]
  },
  {
    name: 'orders',
    description: 'Customer order history and totals',
    columns: [
      { name: 'id', type: 'INT', isPrimary: true },
      { name: 'customer_id', type: 'INT', isPrimary: false, isForeign: true },
      { name: 'amount', type: 'DECIMAL(10,2)', isPrimary: false },
      { name: 'status', type: 'VARCHAR(50)', isPrimary: false },
      { name: 'order_date', type: 'TIMESTAMP', isPrimary: false },
    ]
  },
  {
    name: 'employees',
    description: 'Internal staff records',
    columns: [
      { name: 'id', type: 'INT', isPrimary: true },
      { name: 'name', type: 'VARCHAR(255)', isPrimary: false },
      { name: 'department', type: 'VARCHAR(100)', isPrimary: false },
      { name: 'hire_date', type: 'DATE', isPrimary: false },
    ]
  }
];

export default function SchemaExplorer() {
  const [search, setSearch] = useState('');

  const filteredSchema = MOCK_SCHEMA.filter(table => 
    table.name.toLowerCase().includes(search.toLowerCase()) ||
    table.columns.some(col => col.name.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div className="p-8 h-full flex flex-col overflow-hidden">
      <div className="flex justify-between items-end mb-8">
        <div>
          <h2 className="text-3xl font-heading font-bold text-[#FAFAFA]">Schema Explorer</h2>
          <p className="text-gray-400 mt-2">Discover and search database tables available to the AI</p>
        </div>
        <div className="relative">
          <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input 
            type="text" 
            placeholder="Search tables or columns..." 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="glass-panel bg-[#111] border border-[#2A2A2A] rounded-full py-2 pl-10 pr-4 text-sm text-[#FAFAFA] focus:outline-none focus:border-[#D4AF37] w-64 transition-colors"
          />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto pb-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredSchema.map((table, i) => (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              key={table.name} 
              className="glass-panel border border-[#2A2A2A] rounded-xl overflow-hidden"
            >
              <div className="bg-[#111] p-4 border-b border-[#2A2A2A] flex justify-between items-center">
                <div className="flex items-center gap-3">
                  <Database size={18} className="text-[#D4AF37]" />
                  <h3 className="font-heading font-semibold text-[#FAFAFA] text-lg">{table.name}</h3>
                </div>
                <span className="text-xs text-gray-500 bg-[#050505] px-2 py-1 rounded-full border border-[#2A2A2A]">
                  {table.columns.length} columns
                </span>
              </div>
              <div className="p-4 bg-[#0A0A0A]">
                <p className="text-sm text-gray-400 mb-4">{table.description}</p>
                
                <table className="w-full text-sm text-left">
                  <tbody>
                    {table.columns.map((col) => (
                      <tr key={col.name} className="border-b border-[#2A2A2A]/30 hover:bg-[#111] transition-colors group">
                        <td className="py-2 px-3 font-medium text-gray-200 flex items-center gap-2">
                          {col.isPrimary && <Key size={12} className="text-[#D4AF37]" />}
                          {col.isForeign && <ChevronRight size={12} className="text-blue-400" />}
                          {col.name}
                        </td>
                        <td className="py-2 px-3 text-right">
                          <span className="text-xs font-mono text-gray-500 bg-[#171717] px-2 py-0.5 rounded flex items-center gap-1 w-max ml-auto">
                            <Type size={10} /> {col.type}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </motion.div>
          ))}
        </div>
        {filteredSchema.length === 0 && (
          <div className="text-center text-gray-500 mt-12">
            No tables or columns match your search.
          </div>
        )}
      </div>
    </div>
  );
}
