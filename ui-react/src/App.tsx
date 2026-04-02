import { useState, useRef } from 'react';
import axios from 'axios';
import Sidebar from './components/Sidebar';
import ChatPanel from './components/ChatPanel';

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface Source {
  id: string;
  name: string;
  type: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sources, setSources] = useState<Source[]>([]);
  const [isIngesting, setIsIngesting] = useState(false);
  const [isQuerying, setIsQuerying] = useState(false);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsIngesting(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE}/upload/pdf`, formData);
      setSources(prev => [...prev, { id: response.data.id, name: file.name, type: 'pdf' }]);
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Failed to ingest source. Ensure backend is running at :8000");
    } finally {
      setIsIngesting(false);
    }
  };

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMsg: Message = { role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setIsQuerying(true);

    try {
      const response = await fetch(`${API_BASE}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: text }),
      });

      if (!response.body) return;

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantContent = "";
      
      setMessages(prev => [...prev, { role: 'assistant', content: "" }]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        assistantContent += chunk;
        
        setMessages(prev => {
          const newMessages = [...prev];
          newMessages[newMessages.length - 1].content = assistantContent;
          return newMessages;
        });
      }
    } catch (err) {
      console.error("Query failed:", err);
    } finally {
      setIsQuerying(false);
    }
  };

  return (
    <div className="flex h-screen bg-saas-bg p-4 overflow-hidden font-inter text-saas-primary">
      <input 
        type="file" 
        ref={fileInputRef} 
        onChange={handleFileChange} 
        className="hidden" 
        accept=".pdf"
      />
      
      {/* Sidebar (Sources Panel) */}
      <Sidebar sources={sources} isIngesting={isIngesting} onAddClick={handleUploadClick} />

      {/* Main Content Area (Chat Panel) */}
      <ChatPanel 
        messages={messages} 
        onSendMessage={handleSendMessage} 
        onUploadClick={handleUploadClick}
        isQuerying={isQuerying}
        sourceCount={sources.length}
      />
    </div>
  );
}

export default App;
