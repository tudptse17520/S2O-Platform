import React from 'react';
import { Plus, Flame, Star } from 'lucide-react';
import { MenuItem } from '../types';

interface MenuCardProps {
  item: MenuItem;
  onPress: (item: MenuItem) => void;
  onQuickAdd: (item: MenuItem, e: React.MouseEvent) => void;
}

export const MenuCard: React.FC<MenuCardProps> = ({ item, onPress, onQuickAdd }) => {
  return (
    <div 
      onClick={() => onPress(item)}
      className="group relative bg-slate-900 rounded-3xl shadow-lg shadow-black/40 border-t-2 border-t-orange-200/60 border-b-2 border-b-white/10 border-x border-x-slate-800 overflow-hidden flex flex-row sm:flex-col h-28 sm:h-full cursor-pointer hover:border-t-orange-400 hover:border-b-white/30 transition-all active:scale-[0.98] transform-gpu"
    >
      {/* Image Section */}
      <div className="relative w-28 sm:w-full h-full sm:h-48 flex-shrink-0 bg-slate-800 overflow-hidden">
        <img 
          src={item.image} 
          alt={item.name} 
          className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500 opacity-90 group-hover:opacity-100 will-change-transform"
        />
        {item.isPopular && (
          <div className="absolute top-2 left-2 bg-yellow-500/90 backdrop-blur-sm text-yellow-950 text-[10px] font-bold px-2 py-0.5 rounded-full shadow-sm flex items-center gap-1">
            <Star size={10} fill="currentColor" />
            <span>BEST SELLER</span>
          </div>
        )}
      </div>
      
      {/* Content Section */}
      <div className="p-3 sm:p-4 flex flex-col flex-grow justify-between min-w-0">
        <div>
          <div className="flex justify-between items-start">
            <h3 className="font-semibold text-slate-100 text-sm sm:text-lg leading-tight line-clamp-2 mb-1 group-hover:text-orange-400 transition-colors">
              {item.name}
            </h3>
          </div>
          {/* Show description more prominently on larger screens */}
          <p className="text-slate-500 text-xs sm:text-sm line-clamp-2 mb-2 hidden sm:block">
            {item.description}
          </p>
        </div>
        
        <div className="flex items-end justify-between mt-1">
          <div className="flex flex-col">
            <div className="flex items-center gap-1 mb-1">
               {item.spicyLevel ? (
                <div className="flex bg-red-900/30 border border-red-900/50 px-1.5 py-0.5 rounded-md">
                   {Array.from({ length: item.spicyLevel }).map((_, i) => (
                     <Flame key={i} size={10} className="text-red-500" fill="currentColor" />
                   ))}
                </div>
              ) : null}
            </div>
            <span className="font-bold text-orange-500 text-base sm:text-lg">
              {new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(item.price)}
            </span>
          </div>
          
          <button 
            onClick={(e) => onQuickAdd(item, e)}
            className="bg-slate-800 hover:bg-orange-600 hover:text-white text-orange-500 border border-slate-700 hover:border-orange-500 p-2 rounded-2xl transition-colors shadow-sm"
            aria-label="Thêm nhanh"
          >
            <Plus size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};