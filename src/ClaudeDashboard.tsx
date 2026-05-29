import React, { useState } from 'react';
import { 
  Plus, Bot, Folder, 
  Search, ChevronDown, User, Monitor,
  FileSpreadsheet, FileCode2, Sun, ArrowRight, Menu, X, Layout
} from 'lucide-react';
import OmegaLegacy from './App';

export default function ClaudeDashboard() {
  const [model, setModel] = useState('Gemini 3.1 Pro (High)');
  const [showLegacy, setShowLegacy] = useState(false);
  const [chatInput, setChatInput] = useState('');
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  if (showLegacy) {
    return (
      <div className="relative w-full h-screen overflow-hidden">
        <button 
          onClick={() => setShowLegacy(false)}
          className="absolute top-4 right-4 md:left-4 md:right-auto z-50 bg-black text-white px-4 py-2 rounded shadow-lg text-sm font-medium hover:bg-gray-800 transition-colors"
        >
          &larr; Return to Dashboard
        </button>
        <OmegaLegacy />
      </div>
    );
  }

  const models = [
    'Gemini 3.1 Pro (High)',
    'Gemini 3.1 Flash',
    'OMEGA Scientific Engine',
    'Manifold Projection Kernel'
  ];

  const SidebarContent = () => (
    <>
      <div className="p-4 flex items-center justify-between text-xl font-serif font-semibold text-[#1A1914]">
        <div className="flex items-center space-x-2">
          <span className="text-[#D97757]">✺</span>
          <span>OMEGA</span>
        </div>
        {/* Mobile close button */}
        <button className="md:hidden" onClick={() => setIsMobileSidebarOpen(false)}>
          <X className="w-6 h-6 text-gray-500" />
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto px-3 py-2 space-y-4">
        <div className="space-y-1">
          <button className="w-full flex items-center space-x-3 px-3 py-2 text-sm font-medium hover:bg-[#EAE4DA] rounded-lg transition-colors">
            <Plus className="w-4 h-4" />
            <span>New Chat</span>
          </button>
          <button className="w-full flex items-center space-x-3 px-3 py-2 text-sm font-medium hover:bg-[#EAE4DA] rounded-lg transition-colors">
            <Bot className="w-4 h-4" />
            <span>Agents</span>
          </button>
          <button className="w-full flex items-center space-x-3 px-3 py-2 text-sm font-medium hover:bg-[#EAE4DA] rounded-lg transition-colors">
            <Folder className="w-4 h-4" />
            <span>Context</span>
          </button>
        </div>

        <div>
          <div className="flex items-center justify-between px-3 py-2">
            <span className="text-xs font-semibold text-[#8C8673] uppercase tracking-wider">Projects</span>
            <Plus className="w-4 h-4 text-[#8C8673] cursor-pointer hover:text-[#3D3929]" />
          </div>
          <button className="w-full flex items-center space-x-3 px-3 py-2 text-sm font-medium hover:bg-[#EAE4DA] rounded-lg transition-colors">
            <Search className="w-4 h-4 text-purple-600" />
            <span>Research</span>
          </button>
        </div>
      </div>

      <div className="p-4 border-t border-[#E5DECD]">
        <button 
          onClick={() => setShowLegacy(true)}
          className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-[#1A1914] text-white rounded-lg hover:bg-[#2A2924] transition-colors text-sm font-medium shadow-sm"
        >
          <Monitor className="w-4 h-4" />
          <span>Open Legacy Console</span>
        </button>
      </div>
    </>
  );

  return (
    <div className="flex h-screen overflow-hidden bg-[#FFFAF3] text-[#3D3929] font-sans">
      
      {/* Mobile Sidebar Overlay */}
      {isMobileSidebarOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden" onClick={() => setIsMobileSidebarOpen(false)} />
      )}

      {/* Sidebar - Desktop & Mobile */}
      <div className={`fixed inset-y-0 left-0 z-50 w-[260px] bg-[#F5EFE6] border-r border-[#E5DECD] flex flex-col transition-transform duration-300 ease-in-out md:relative md:translate-x-0 ${isMobileSidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <SidebarContent />
      </div>
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col h-full bg-[#FFFAF3] relative overflow-y-auto">
        
        {/* Header */}
        <div className="flex items-center justify-between p-4 md:absolute md:top-0 md:right-0 md:w-auto w-full z-10 bg-[#FFFAF3] md:bg-transparent border-b md:border-b-0 border-[#E5DECD]">
          {/* Mobile Hamburger */}
          <button className="md:hidden p-2 hover:bg-[#F0EBE1] rounded-md transition-colors" onClick={() => setIsMobileSidebarOpen(true)}>
            <Menu className="w-6 h-6 text-gray-700" />
          </button>
          
          <div className="flex-1 md:hidden text-center text-xl font-serif font-semibold text-[#1A1914]">
            <span className="text-[#D97757] mr-1">✺</span>OMEGA
          </div>

          <div className="flex items-center space-x-2 md:space-x-4">
            <div className="relative">
              <button 
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                className="flex items-center space-x-1 md:space-x-2 text-xs md:text-sm font-medium hover:bg-[#F0EBE1] px-2 py-1.5 md:px-3 rounded-md transition-colors"
              >
                <span className="hidden sm:inline">{model}</span>
                <span className="sm:hidden">{model.split(' ')[0]}</span>
                <ChevronDown className="w-4 h-4 text-gray-500" />
              </button>
              {isDropdownOpen && (
                <div className="absolute top-full mt-1 right-0 w-48 md:w-56 bg-white border border-[#E5DECD] rounded-lg shadow-xl py-1 z-50">
                  {models.map(m => (
                    <button 
                      key={m}
                      onClick={() => { setModel(m); setIsDropdownOpen(false); }}
                      className={`w-full text-left px-4 py-2 text-xs md:text-sm hover:bg-[#F5EFE6] ${model === m ? 'font-semibold' : ''}`}
                    >
                      {m}
                    </button>
                  ))}
                </div>
              )}
            </div>
            <button className="hidden sm:flex p-2 hover:bg-[#F0EBE1] rounded-full transition-colors">
              <User className="w-5 h-5 text-gray-600" />
            </button>
          </div>
        </div>

        {/* Centered Content */}
        <div className="flex-1 flex flex-col items-center justify-center max-w-3xl mx-auto w-full px-4 sm:px-6 py-12 md:py-0">
          <h1 className="text-4xl md:text-5xl font-serif text-[#1A1914] mb-2 text-center leading-tight">
            Think fast, build faster
          </h1>
          <p className="text-[#8C8673] mb-8 md:mb-12 text-center text-base md:text-lg">
            Brainstorm in chat, build in OMEGA Core
          </p>

          {/* Action Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 md:gap-3 mb-6 md:mb-8 w-full">
            <button className="flex flex-col items-center justify-center p-3 md:p-4 bg-white border border-[#E5DECD] rounded-xl hover:border-[#D97757] hover:shadow-md transition-all group min-h-[100px]">
              <FileSpreadsheet className="w-5 h-5 md:w-6 md:h-6 text-gray-400 group-hover:text-[#D97757] mb-2" />
              <span className="text-xs md:text-sm font-medium text-center leading-tight">Create a file</span>
            </button>
            <button className="flex flex-col items-center justify-center p-3 md:p-4 bg-white border border-[#E5DECD] rounded-xl hover:border-[#D97757] hover:shadow-md transition-all group min-h-[100px]">
              <Layout className="w-5 h-5 md:w-6 md:h-6 text-gray-400 group-hover:text-[#D97757] mb-2" />
              <span className="text-xs md:text-sm font-medium text-center leading-tight">Crunch data</span>
            </button>
            <button className="flex flex-col items-center justify-center p-3 md:p-4 bg-white border border-[#E5DECD] rounded-xl hover:border-[#D97757] hover:shadow-md transition-all group min-h-[100px]">
              <FileCode2 className="w-5 h-5 md:w-6 md:h-6 text-gray-400 group-hover:text-[#D97757] mb-2" />
              <span className="text-xs md:text-sm font-medium text-center leading-tight">Make a prototype</span>
            </button>
            <button className="flex flex-col items-center justify-center p-3 md:p-4 bg-white border border-[#E5DECD] rounded-xl hover:border-[#D97757] hover:shadow-md transition-all group min-h-[100px]">
              <Sun className="w-5 h-5 md:w-6 md:h-6 text-gray-400 group-hover:text-[#D97757] mb-2" />
              <span className="text-xs md:text-sm font-medium text-center leading-tight">Prep for the day</span>
            </button>
          </div>

          {/* Chat Input */}
          <div className="w-full bg-white border border-[#E5DECD] rounded-2xl shadow-sm focus-within:shadow-md focus-within:border-[#D97757] transition-all p-2 flex flex-col">
            <div className="px-3 pt-2 text-[#8C8673] text-xs md:text-sm truncate">
              Summarize this research into a presentation
            </div>
            <textarea 
              className="w-full resize-none bg-transparent outline-none p-3 text-[#1A1914] placeholder-[#8C8673] min-h-[80px] text-sm md:text-base"
              placeholder="How can OMEGA help you today?"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
            />
            <div className="flex items-center justify-between p-1 md:p-2">
              <button className="flex items-center space-x-1 text-[#8C8673] hover:text-[#3D3929] px-2 py-1 rounded-md text-xs md:text-sm transition-colors font-medium border border-transparent hover:border-[#E5DECD]">
                <Folder className="w-3 h-3 md:w-4 md:h-4" />
                <span className="hidden sm:inline">Work in a folder</span>
                <span className="sm:hidden">Folder</span>
                <Plus className="w-3 h-3 md:w-4 md:h-4 ml-1" />
              </button>
              <button className="bg-[#D97757] text-white px-3 md:px-4 py-1.5 md:py-2 rounded-lg flex items-center space-x-1 md:space-x-2 hover:bg-[#C26547] transition-colors font-medium text-xs md:text-sm">
                <span>Let's go</span>
                <ArrowRight className="w-3 h-3 md:w-4 md:h-4" />
              </button>
            </div>
          </div>
          
          <div className="mt-4 md:mt-6 text-[10px] md:text-xs text-[#8C8673] text-center max-w-lg px-2">
            By interacting with OMEGA, you are engaging with the autonomous scientific cognition layer. No external API keys are active. Data is localized to the secure sandbox.
          </div>
        </div>
      </div>
    </div>
  );
}
