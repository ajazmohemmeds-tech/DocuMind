import React from 'react';
import { Upload } from 'lucide-react';

interface EmptyStateProps {
  onUploadClick: () => void;
}

const EmptyState: React.FC<EmptyStateProps> = ({ onUploadClick }) => {
  return (
    <div className="flex-1 flex flex-col items-center justify-center text-center">
      <div className="p-5 bg-saas-accent rounded-full text-blue-600 mb-8 flex items-center justify-center shadow-sm">
        <Upload size={36} />
      </div>
      <h1 className="text-saas-primary text-3xl font-bold tracking-tight mb-8">Add a source to get started</h1>
      <button 
        onClick={onUploadClick}
        className="bg-white border border-saas-border text-saas-primary px-8 py-3 rounded-full hover:bg-saas-bg transition-all font-semibold shadow-sm hover:border-saas-secondary"
      >
        Upload a source
      </button>
    </div>
  );
};

export default EmptyState;
