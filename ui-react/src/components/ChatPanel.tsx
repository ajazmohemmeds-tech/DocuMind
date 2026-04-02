import React, { useRef, useEffect } from 'react';
import Header from './Header';
import EmptyState from './EmptyState';
import InputBar from './InputBar';
import { Loader2 } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatPanelProps {
  messages: Message[];
  onSendMessage: (text: string) => void;
  onUploadClick: () => void;
  isQuerying: boolean;
  sourceCount: number;
}

const ChatPanel: React.FC<ChatPanelProps> = ({ messages, onSendMessage, onUploadClick, isQuerying, sourceCount }) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <main className="flex-1 h-[calc(100vh-32px)] bg-white rounded-saas p-6 flex flex-col m-4 ml-0 border border-saas-border shadow-saas-soft relative overflow-hidden">
      {/* 1. Header */}
      <Header />

      {/* 2. Messages / Empty State */}
      <div className="flex-1 flex flex-col overflow-y-auto mb-6 scrollbar-hide px-2">
        {messages.length === 0 ? (
          <EmptyState onUploadClick={onUploadClick} />
        ) : (
          <div className="space-y-6 max-w-4xl mx-auto w-full">
            {messages.map((m, idx) => (
              <div 
                key={idx} 
                className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-[85%] p-4 rounded-2xl ${
                  m.role === 'user' 
                    ? 'bg-saas-primary text-white ml-12 shadow-sm' 
                    : 'bg-saas-sidebar text-saas-primary mr-12 border border-saas-border shadow-sm'
                } text-sm leading-relaxed whitespace-pre-wrap font-inter`}>
                  {m.content}
                </div>
              </div>
            ))}
            {isQuerying && (
              <div className="flex justify-start">
                <div className="bg-saas-sidebar p-4 rounded-2xl border border-saas-border flex items-center gap-2 shadow-sm">
                  <Loader2 size={16} className="animate-spin text-blue-500" />
                  <span className="text-xs text-saas-secondary font-semibold">Synthesizing insight...</span>
                </div>
              </div>
            )}
            <div ref={scrollRef} />
          </div>
        )}
      </div>

      {/* 3. Input Bar */}
      <InputBar 
        onSendMessage={onSendMessage} 
        isQuerying={isQuerying} 
        hasMessages={messages.length > 0} 
        sourceCount={sourceCount}
      />
    </main>
  );
};

export default ChatPanel;
