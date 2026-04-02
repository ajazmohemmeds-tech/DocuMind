import React from 'react';
import { Sparkles } from 'lucide-react';

interface HeroProps {
  onLaunch: () => void;
}

const Hero: React.FC<HeroProps> = ({ onLaunch }) => {
  return (
    <div className="min-h-screen w-full bg-[#EAE0D2] flex flex-col items-center justify-center relative overflow-hidden font-outfit">
      {/* Background Image Layer */}
      <div 
        className="absolute inset-0 opacity-40 mix-blend-multiply pointer-events-none bg-center bg-no-repeat bg-cover"
        style={{ backgroundImage: 'url("/hero-bg.png")' }}
      />
      
      {/* Navigation (Ghost Header) */}
      <div className="absolute top-0 left-0 w-full p-10 flex justify-between items-center z-20">
        <div className="text-2xl font-extrabold text-[#2D2D2D] tracking-tighter">DocuMind</div>
        <div className="hidden md:flex gap-8 text-sm font-semibold text-[#2D2D2D] opacity-70">
          <span className="cursor-pointer hover:opacity-100">Insight Hub</span>
          <span className="cursor-pointer hover:opacity-100">Capabilities</span>
          <span className="cursor-pointer hover:opacity-100">Enterprise</span>
          <span className="cursor-pointer hover:opacity-100">Community</span>
        </div>
        <div className="bg-[#2D2D2D] text-white px-6 py-2.5 rounded-full text-xs font-bold uppercase tracking-widest cursor-pointer hover:bg-[#A68763] transition-colors">
          BETA
        </div>
      </div>
      
      {/* Main Hero Content */}
      <div className="relative z-10 text-center px-6 max-w-5xl">
        <div className="flex justify-center mb-8">
          <div className="text-[#A68763] animate-pulse">
            <Sparkles size={48} />
          </div>
        </div>
        
        <h1 className="text-[72px] md:text-[110px] font-extrabold text-[#2D2D2D] leading-[0.9] tracking-[-0.04em] mb-10">
          Stop Searching<br />
          <span className="text-[#A68763]">Start Asking</span>
        </h1>
        
        <p className="text-lg md:text-2xl text-[#2D2D2D] opacity-80 max-w-2xl mx-auto mb-14 leading-relaxed font-inter">
          Your research and thinking partner, grounded in the information you trust, 
          built with premium DocuMind synthesis.
        </p>
        
        <button 
          onClick={onLaunch}
          className="bg-[#A68763] hover:bg-[#2D2D2D] text-white px-16 py-6 rounded-full text-2xl font-extrabold transition-all transform hover:scale-105 shadow-2xl hover:shadow-[#A68763]/40 cursor-pointer"
        >
          Try DocuMind
        </button>
      </div>

      {/* Capabilities Section Preview */}
      <div className="absolute bottom-16 w-full flex justify-center items-center gap-10 text-[#2D2D2D] opacity-20 font-bold tracking-[0.3em] text-[10px] uppercase pointer-events-none">
        <span>OpenAI</span>
        <div className="w-1 h-1 bg-[#2D2D2D] rounded-full" />
        <span>FAISS</span>
        <div className="w-1 h-1 bg-[#2D2D2D] rounded-full" />
        <span>LangChain</span>
        <div className="w-1 h-1 bg-[#2D2D2D] rounded-full" />
        <span>PyMuPDF</span>
        <div className="w-1 h-1 bg-[#2D2D2D] rounded-full" />
        <span>RAGAS</span>
      </div>

      {/* Subtle corner gradients */}
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-[#A68763] opacity-10 blur-[120px] rounded-full" />
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-[#A68763] opacity-10 blur-[120px] rounded-full" />
    </div>
  );
};

export default Hero;
