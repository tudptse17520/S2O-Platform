import React, { useState, useRef, useEffect } from 'react';
import { X, Send, Sparkles, ChefHat, MessageSquare } from 'lucide-react';
import { getDishRecommendation } from '../services/geminiService';
import { MenuItem, ChatMessage } from '../types';

interface AIChatProps {
  isOpen: boolean;
  onClose: () => void;
  menu: MenuItem[];
}

const SUGGESTED_PROMPTS = [
  "Món nào bán chạy nhất?",
  "Tôi thích ăn cay",
  "Món nào rẻ nhất?",
  "Tư vấn thực đơn cho 2 người",
  "Có món nào không cay không?"
];

export const AIChat: React.FC<AIChatProps> = ({ isOpen, onClose, menu }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      role: 'model',
      text: 'Xin chào! Tôi là trợ lý ảo AI. Bạn đang thèm món gì hôm nay?'
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen]);

  const handleSend = async (text: string = inputText) => {
    if (!text.trim() || isLoading) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      text: text
    };

    setMessages(prev => [...prev, userMsg]);
    setInputText('');
    setIsLoading(true);

    const responseText = await getDishRecommendation(text, menu);

    const aiMsg: ChatMessage = {
      id: (Date.now() + 1).toString(),
      role: 'model',
      text: responseText
    };

    setMessages(prev => [...prev, aiMsg]);
    setIsLoading(false);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center pointer-events-none">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm pointer-events-auto transition-opacity" onClick={onClose} />
      
      <div className="bg-slate-900 w-full sm:w-[400px] h-[90vh] sm:h-[650px] rounded-t-3xl sm:rounded-3xl shadow-2xl flex flex-col pointer-events-auto transform transition-transform duration-300 ease-out animate-in slide-in-from-bottom border-t-2 border-t-orange-200/60 border-b-2 border-b-white/10 border-x border-x-slate-800 overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex justify-between items-center bg-slate-900">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-tr from-indigo-600 to-purple-700 p-2.5 rounded-xl shadow-lg shadow-indigo-900/50">
              <Sparkles size={20} className="text-white" />
            </div>
            <div>
              <h3 className="font-bold text-white">Trợ Lý Ẩm Thực</h3>
              <p className="text-xs text-indigo-400 font-medium">Powered by Gemini</p>
            </div>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-slate-800 rounded-full text-slate-400 hover:text-white transition-colors">
            <X size={20} />
          </button>
        </div>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-950/50">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex w-full ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex flex-col max-w-[85%] ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                {msg.role === 'model' && (
                  <span className="text-[10px] text-slate-500 mb-1 ml-1 flex items-center gap-1">
                    <ChefHat size={10} /> Chef AI
                  </span>
                )}
                <div
                  className={`p-3.5 rounded-2xl text-sm leading-relaxed shadow-sm whitespace-pre-wrap ${
                    msg.role === 'user'
                      ? 'bg-indigo-600 text-white rounded-br-sm'
                      : 'bg-slate-800 text-slate-200 border border-slate-700 rounded-bl-sm'
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start w-full">
               <div className="bg-slate-800 border border-slate-700 px-4 py-3 rounded-2xl rounded-bl-sm shadow-sm flex items-center gap-1.5">
                 <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce" />
                 <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce delay-75" />
                 <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-bounce delay-150" />
               </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Suggested Prompts (Horizontal Scroll) */}
        {!isLoading && (
          <div className="px-4 py-2 bg-slate-900 border-t border-slate-800 overflow-x-auto no-scrollbar flex gap-2">
            {SUGGESTED_PROMPTS.map((prompt, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(prompt)}
                className="whitespace-nowrap px-3 py-1.5 bg-slate-800 border border-slate-700 text-indigo-400 text-xs rounded-full hover:bg-slate-700 transition-colors shadow-sm"
              >
                {prompt}
              </button>
            ))}
          </div>
        )}

        {/* Input Area */}
        <div className="p-4 bg-slate-900 border-t border-slate-800">
          <div className="flex gap-2 items-center bg-slate-950 rounded-full px-2 py-1.5 border border-slate-800 focus-within:border-indigo-500 focus-within:ring-1 focus-within:ring-indigo-500/50 transition-all">
            <div className="p-2 text-slate-500">
              <MessageSquare size={20} />
            </div>
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Nhập câu hỏi..."
              className="flex-1 bg-transparent focus:outline-none text-sm text-white placeholder:text-slate-600"
            />
            <button
              onClick={() => handleSend()}
              disabled={isLoading || !inputText.trim()}
              className="bg-indigo-600 text-white p-2 rounded-full hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-transform active:scale-95 shadow-md"
            >
              <Send size={18} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};