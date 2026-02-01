import React, { useEffect, useState } from 'react';
import { ChefHat, UtensilsCrossed } from 'lucide-react';

interface SplashScreenProps {
  onFinish: () => void;
}

export const SplashScreen: React.FC<SplashScreenProps> = ({ onFinish }) => {
  const [isExiting, setIsExiting] = useState(false);

  useEffect(() => {
    // Start exit animation after 2.2 seconds
    const timer = setTimeout(() => {
      setIsExiting(true);
    }, 2200);

    // Unmount callback after animation completes
    const cleanup = setTimeout(() => {
      onFinish();
    }, 2800);

    return () => {
      clearTimeout(timer);
      clearTimeout(cleanup);
    };
  }, [onFinish]);

  return (
    <div 
      className={`fixed inset-0 z-[100] bg-slate-950 flex flex-col items-center justify-center transition-opacity duration-700 ease-out ${
        isExiting ? 'opacity-0 pointer-events-none' : 'opacity-100'
      }`}
    >
      <style>
        {`
          @keyframes blur-in {
            0% { opacity: 0; filter: blur(10px); transform: scale(0.9); }
            100% { opacity: 1; filter: blur(0); transform: scale(1); }
          }
          @keyframes slide-up-fade {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
          }
          @keyframes draw-line {
            0% { width: 0; opacity: 0; }
            50% { opacity: 1; }
            100% { width: 6rem; opacity: 1; }
          }
          @keyframes shimmer {
            0% { background-position: -200% center; }
            100% { background-position: 200% center; }
          }
        `}
      </style>

      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-orange-600/20 rounded-full blur-[100px] animate-pulse"></div>

      <div className="relative z-10 flex flex-col items-center">
        {/* Icon Animation */}
        <div 
          className="mb-6 relative"
          style={{ animation: 'blur-in 1s cubic-bezier(0.22, 1, 0.36, 1) forwards' }}
        >
          <div className="relative z-10 bg-gradient-to-br from-orange-500 to-red-600 p-4 rounded-2xl shadow-[0_0_30px_rgba(234,88,12,0.4)]">
            <ChefHat size={48} className="text-white" />
          </div>
          <div className="absolute -inset-2 border border-orange-500/30 rounded-3xl animate-spin-slow"></div>
        </div>

        {/* Main Title "ANH HAI" */}
        <h1 
          className="text-5xl sm:text-6xl font-bold tracking-tighter mb-2"
          style={{ 
            animation: 'blur-in 1.2s cubic-bezier(0.22, 1, 0.36, 1) 0.3s forwards',
            opacity: 0
          }}
        >
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-orange-200 via-orange-500 to-orange-200 bg-[length:200%_auto] animate-[shimmer_3s_linear_infinite]">
            ANH HAI
          </span>
        </h1>

        {/* Subtitle "RESTAURANT" */}
        <div 
          className="flex flex-col items-center gap-3"
          style={{ 
            animation: 'slide-up-fade 0.8s ease-out 0.8s forwards',
            opacity: 0
          }}
        >
          <div className="flex items-center gap-3">
             <div className="h-[1px] bg-slate-700 w-8"></div>
             <span className="text-slate-400 text-sm tracking-[0.4em] uppercase font-medium">Restaurant</span>
             <div className="h-[1px] bg-slate-700 w-8"></div>
          </div>
        </div>

        {/* Loading Indicator */}
        <div 
          className="absolute -bottom-24 flex flex-col items-center gap-2"
           style={{ 
            animation: 'slide-up-fade 0.5s ease-out 1.2s forwards',
            opacity: 0
          }}
        >
          <div className="flex gap-1">
            <div className="w-1.5 h-1.5 bg-orange-500 rounded-full animate-bounce"></div>
            <div className="w-1.5 h-1.5 bg-orange-500 rounded-full animate-bounce delay-100"></div>
            <div className="w-1.5 h-1.5 bg-orange-500 rounded-full animate-bounce delay-200"></div>
          </div>
          <span className="text-[10px] text-slate-600 uppercase tracking-widest">Loading Experience</span>
        </div>
      </div>
    </div>
  );
};