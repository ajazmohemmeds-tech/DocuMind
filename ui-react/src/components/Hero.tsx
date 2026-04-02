import React from 'react';
import { Sparkles, Brain, ShieldCheck, Zap } from 'lucide-react';

interface HeroProps {
  onLaunch: () => void;
}

const Hero: React.FC<HeroProps> = ({ onLaunch }) => {
  return (
    <div className="w-full bg-[#EAE0D2] font-outfit text-[#2D2D2D] overflow-y-auto">
      
      {/* ─── SECTION 1: HERO ─── */}
      <div className="min-h-screen w-full flex flex-col items-center justify-center relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full p-10 flex justify-between items-center z-20">
          <div className="text-2xl font-extrabold tracking-tighter">DocuMind</div>
          <div className="hidden md:flex gap-8 text-sm font-semibold opacity-70">
            <span className="cursor-pointer hover:opacity-100 hover:text-[#A68763] transition-colors">Insight Hub</span>
            <span className="cursor-pointer hover:opacity-100 hover:text-[#A68763] transition-colors">Capabilities</span>
            <span className="cursor-pointer hover:opacity-100 hover:text-[#A68763] transition-colors">Enterprise</span>
            <span className="cursor-pointer hover:opacity-100 hover:text-[#A68763] transition-colors">Community</span>
          </div>
          <div className="bg-[#2D2D2D] text-white px-6 py-2.5 rounded-full text-xs font-bold uppercase tracking-widest cursor-pointer hover:bg-[#A68763] transition-colors">BETA</div>
        </div>
        <div className="relative z-10 text-center px-6 max-w-5xl">
          <div className="flex justify-center mb-8"><div className="text-[#A68763] animate-pulse"><Sparkles size={48} /></div></div>
          <h1 className="text-[72px] md:text-[110px] font-extrabold leading-[0.9] tracking-[-0.04em] mb-10">Stop Searching<br /><span className="text-[#A68763]">Start Asking</span></h1>
          <p className="text-lg md:text-2xl opacity-80 max-w-2xl mx-auto mb-14 leading-relaxed font-inter">Your research and thinking partner, grounded in the information you trust, built with premium DocuMind synthesis.</p>
          <button onClick={onLaunch} className="bg-[#A68763] hover:bg-[#2D2D2D] text-white px-16 py-6 rounded-full text-2xl font-extrabold transition-all transform hover:scale-105 shadow-2xl hover:shadow-[#A68763]/40 cursor-pointer">Try DocuMind</button>
        </div>
        <div className="absolute bottom-16 w-full flex justify-center items-center gap-10 opacity-20 font-bold tracking-[0.3em] text-[10px] uppercase pointer-events-none">
          <span>Google Gemini</span><div className="w-1 h-1 bg-[#2D2D2D] rounded-full" /><span>FAISS</span><div className="w-1 h-1 bg-[#2D2D2D] rounded-full" /><span>LangChain</span><div className="w-1 h-1 bg-[#2D2D2D] rounded-full" /><span>PyMuPDF</span><div className="w-1 h-1 bg-[#2D2D2D] rounded-full" /><span>RAGAS</span>
        </div>
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-[#A68763] opacity-10 blur-[120px] rounded-full" />
        <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-[#A68763] opacity-10 blur-[120px] rounded-full" />
      </div>

      {/* ─── SECTION 2: WHAT IS DOCUMIND? ─── */}
      <div className="py-32 px-8 md:px-20 bg-[#EAE0D2]">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-start gap-8 mb-20">
            <h2 className="text-4xl md:text-[56px] font-bold leading-tight">What is DocuMind?</h2>
            <p className="text-lg md:text-xl opacity-70 max-w-md leading-relaxed">DocuMind is an insight-bearing research hub that helps your synthesis grow while staying grounded in verified sources.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-[#D7C9AE] rounded-[32px] p-12 relative overflow-hidden group hover:shadow-2xl transition-shadow">
              <div className="mb-6 text-[#A68763]"><Brain size={40} /></div>
              <h3 className="text-2xl font-bold mb-4">Insights that grow</h3>
              <p className="text-base opacity-70 max-w-[240px]">Transform passive data into high-performing research protocols.</p>
              <div className="absolute -right-10 -bottom-10 w-48 h-48 bg-[#A68763] opacity-10 rounded-full blur-[60px] group-hover:opacity-20 transition-opacity" />
            </div>
            <div className="bg-[#2D2D2D] text-[#EAE0D2] rounded-[32px] p-12 group hover:shadow-2xl transition-shadow">
              <div className="mb-6 text-[#A68763]"><ShieldCheck size={40} /></div>
              <h3 className="text-2xl font-bold mb-4">Always grounded,<br/>Always verified</h3>
              <p className="text-base opacity-70">Stay fully source-pegged with instant access to your citations — no hallucinations.</p>
            </div>
            <div className="bg-[#2D2D2D] text-[#EAE0D2] rounded-[32px] p-12 group hover:shadow-2xl transition-shadow">
              <div className="mb-6 text-[#A68763]"><Zap size={40} /></div>
              <h3 className="text-2xl font-bold mb-4">100%<br/>Hands-free</h3>
              <p className="text-base opacity-70">No need to manage chunks manually. DocuMind works in the background for you.</p>
            </div>
          </div>
          <div className="flex justify-center gap-16 mt-20 opacity-30 font-bold tracking-[0.2em] text-xs uppercase">
            <span>GOOGLE GEMINI</span><span>FAISS</span><span>LANGCHAIN</span><span>PYMUPDF</span><span>RAGAS</span>
          </div>
        </div>
      </div>

      {/* ─── SECTION 3: USE CASES ─── */}
      <div className="py-28 px-8 md:px-20 bg-[#D7C9AE]">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row gap-16 items-center">
          <div className="flex-1">
            <p className="text-sm font-semibold text-[#A68763] mb-4 tracking-widest uppercase">DocuMind in Action</p>
            <h2 className="text-4xl md:text-[56px] font-bold mb-8 leading-tight">Use cases</h2>
            <p className="text-lg opacity-80 leading-relaxed max-w-md">DocuMind offers a variety of use cases for researchers, students, and businesses seeking secure and accurate knowledge synthesis.</p>
          </div>
          <div className="flex-[1.5] bg-[#EAE0D2] border border-[#A68763] rounded-[40px] p-14">
            <h3 className="text-3xl md:text-4xl font-bold mb-6">Scholarly Hub</h3>
            <p className="text-lg opacity-80 mb-10 leading-relaxed">Boost your engagement by offering a secure, source-backed synthesis with high fidelity, allowing you to learn effortlessly.</p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex items-start gap-4"><div className="w-10 h-10 rounded-full bg-[#A68763] flex items-center justify-center text-white shrink-0">✓</div><div><h4 className="font-bold text-lg">PDF & URL Ingestion</h4><p className="opacity-60 text-sm">Upload research papers or paste web articles</p></div></div>
              <div className="flex items-start gap-4"><div className="w-10 h-10 rounded-full bg-[#A68763] flex items-center justify-center text-white shrink-0">✓</div><div><h4 className="font-bold text-lg">Hybrid Search</h4><p className="opacity-60 text-sm">Dense + BM25 for high-precision retrieval</p></div></div>
              <div className="flex items-start gap-4"><div className="w-10 h-10 rounded-full bg-[#A68763] flex items-center justify-center text-white shrink-0">✓</div><div><h4 className="font-bold text-lg">Streaming Synthesis</h4><p className="opacity-60 text-sm">Real-time AI-powered research insights</p></div></div>
              <div className="flex items-start gap-4"><div className="w-10 h-10 rounded-full bg-[#A68763] flex items-center justify-center text-white shrink-0">✓</div><div><h4 className="font-bold text-lg">RAGAS Evaluation</h4><p className="opacity-60 text-sm">Automated quality & faithfulness scoring</p></div></div>
            </div>
          </div>
        </div>
      </div>

      {/* ─── FOOTER CTA ─── */}
      <div className="py-20 bg-[#2D2D2D] text-center">
        <h2 className="text-3xl md:text-5xl font-bold text-[#EAE0D2] mb-6">Ready to transform your research?</h2>
        <p className="text-lg text-[#D7C9AE] opacity-70 mb-10 max-w-lg mx-auto">Start asking questions grounded in the documents you trust.</p>
        <button onClick={onLaunch} className="bg-[#A68763] hover:bg-[#EAE0D2] hover:text-[#2D2D2D] text-white px-14 py-5 rounded-full text-xl font-bold transition-all transform hover:scale-105 shadow-2xl cursor-pointer">Launch DocuMind</button>
      </div>
    </div>
  );
};

export default Hero;
