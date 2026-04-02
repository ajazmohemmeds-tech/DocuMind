import React, { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';

interface InputBarProps {
  onSendMessage: (text: string) => void;
  isQuerying: boolean;
  hasMessages: boolean;
  sourceCount: number;
}

const InputBar: React.FC<InputBarProps> = ({ onSendMessage, isQuerying, hasMessages, sourceCount }) => {
  const [input, setInput] = useState("");

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (input.trim() && !isQuerying) {
      onSendMessage(input);
      setInput("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative mt-auto w-full max-w-4xl mx-auto">
      <div className="bg-white rounded-[28px] p-2 pl-6 border border-saas-border shadow-saas-soft flex items-center pr-2 hover:border-saas-secondary focus-within:border-blue-300 transition-all min-h-[64px]">
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isQuerying}
          placeholder={!hasMessages ? "Upload a source to get started" : "Ask about your sources..."} 
          className="flex-1 bg-transparent border-none focus:outline-none text-saas-primary placeholder:text-saas-secondary text-base py-2 disabled:opacity-50"
        />
        <div className="flex items-center gap-3 ml-2">
          <span className="text-saas-secondary text-xs font-medium whitespace-nowrap px-2">
            {sourceCount} {sourceCount === 1 ? 'source' : 'sources'}
          </span>
          <button 
            type="submit"
            disabled={isQuerying || !input.trim()}
            className="bg-saas-primary hover:bg-black text-white w-10 h-10 rounded-full flex items-center justify-center transition-all disabled:bg-saas-bg disabled:text-saas-secondary group"
          >
            {isQuerying ? <Loader2 className="animate-spin" size={18} /> : <Send size={18} className="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />}
          </button>
        </div>
      </div>
    </form>
  );
};

export default InputBar;
