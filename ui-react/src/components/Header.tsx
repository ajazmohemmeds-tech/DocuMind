import React from 'react';
import { Settings, MoreVertical } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="flex justify-between items-center py-4 px-2 mb-4 bg-transparent">
      <h2 className="text-saas-primary font-bold text-xl tracking-tight">Chat</h2>
      <div className="flex gap-4 text-saas-secondary">
        <button className="hover:text-saas-primary transition-colors p-1 rounded-md hover:bg-gray-100">
          <Settings size={20} />
        </button>
        <button className="hover:text-saas-primary transition-colors p-1 rounded-md hover:bg-gray-100">
          <MoreVertical size={20} />
        </button>
      </div>
    </header>
  );
};

export default Header;
