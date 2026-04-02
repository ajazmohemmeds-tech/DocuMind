import React from 'react';
import { Plus, Search, Globe, Sparkles, FileText, PanelLeftClose, Loader2 } from 'lucide-react';

interface Source {
  id: string;
  name: string;
  type: string;
}

interface SidebarProps {
  sources: Source[];
  isIngesting: boolean;
  onAddClick: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ sources, isIngesting, onAddClick }) => {
  return (
    <aside className="w-[300px] h-[calc(100vh-32px)] bg-saas-sidebar rounded-saas p-4 flex flex-col border border-saas-border m-4 shadow-sm overflow-hidden">
      {/* Header */}
      <div className="flex justify-between items-center mb-6 px-1">
        <h2 className="text-saas-primary font-semibold text-lg tracking-tight">Sources</h2>
        <button className="text-saas-secondary hover:text-saas-primary transition-colors p-1 rounded-md hover:bg-gray-200">
          <PanelLeftClose size={18} />
        </button>
      </div>

      {/* Add Sources Button */}
      <button 
        onClick={onAddClick}
        disabled={isIngesting}
        className="w-full bg-saas-accent hover:bg-blue-100 text-[#2563EB] py-3 px-4 rounded-full flex items-center justify-center gap-2 transition-all font-semibold text-sm mb-6 border border-transparent disabled:opacity-50"
      >
        {isIngesting ? <Loader2 className="animate-spin" size={18} /> : <Plus size={18} />}
        Add sources
      </button>

      {/* Search Section */}
      <div className="bg-white rounded-[20px] p-1.5 border border-saas-border mb-6 shadow-sm">
        <div className="flex items-center gap-2 px-2 py-1.5">
          <Search size={16} className="text-saas-secondary" />
          <input 
            type="text" 
            placeholder="Search the web for new sources" 
            className="bg-transparent border-none focus:outline-none text-xs w-full placeholder:text-saas-secondary font-medium"
          />
        </div>
        <div className="flex items-center justify-between px-1.5 pb-1 mt-1">
          <div className="flex gap-2">
            <div className="flex items-center gap-1.5 bg-saas-sidebar px-2.5 py-1.5 rounded-lg text-[11px] font-semibold text-saas-primary border border-saas-border cursor-pointer hover:bg-white transition-all">
              <Globe size={12} />
              Web
            </div>
            <div className="flex items-center gap-1.5 bg-saas-sidebar px-2.5 py-1.5 rounded-lg text-[11px] font-semibold text-saas-primary border border-saas-border cursor-pointer hover:bg-white transition-all">
              <Sparkles size={12} className="text-blue-500" />
              Fast Research
            </div>
          </div>
          <button className="w-8 h-8 bg-saas-sidebar rounded-full flex items-center justify-center border border-saas-border hover:bg-white transition-all">
            <span className="text-saas-primary text-sm font-bold opacity-40">→</span>
          </button>
        </div>
      </div>

      {/* Source List / Empty State */}
      <div className="flex-1 overflow-y-auto space-y-2 mb-4 scrollbar-hide">
        {sources.length > 0 ? (
          sources.map((src) => (
            <div key={src.id} className="flex items-center gap-3 p-3 bg-white rounded-xl border border-saas-border hover:border-blue-300 transition-all cursor-pointer shadow-sm group">
              <div className="p-2 bg-saas-bg rounded-lg text-saas-secondary group-hover:text-blue-500 transition-colors">
                <FileText size={16} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-saas-primary truncate">{src.name}</p>
                <p className="text-[10px] text-saas-secondary uppercase font-bold tracking-wider">{src.type}</p>
              </div>
            </div>
          ))
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-center px-4 pb-8 space-y-4">
            <div className="bg-white p-4 rounded-2xl border border-saas-border text-saas-secondary shadow-sm">
              <FileText size={32} strokeWidth={1.5} />
            </div>
            <div className="space-y-2">
              <h4 className="text-saas-primary font-bold text-sm">Saved sources will appear here</h4>
              <p className="text-saas-secondary text-[12px] leading-relaxed max-w-[200px] mx-auto">
                Click Add source above to add PDFs, websites, text, videos, or audio files. Or import a file directly from Google Drive.
              </p>
            </div>
          </div>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
