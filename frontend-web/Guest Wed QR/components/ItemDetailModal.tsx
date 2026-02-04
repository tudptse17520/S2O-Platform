import React, { useState, useEffect } from 'react';
import { X, Minus, Plus, ShoppingBag, Flame } from 'lucide-react';
import { MenuItem } from '../types';

interface ItemDetailModalProps {
  item: MenuItem | null;
  isOpen: boolean;
  onClose: () => void;
  onAddToCart: (item: MenuItem, quantity: number, notes: string) => void;
}

export const ItemDetailModal: React.FC<ItemDetailModalProps> = ({ item, isOpen, onClose, onAddToCart }) => {
  const [quantity, setQuantity] = useState(1);
  const [notes, setNotes] = useState('');

  // Reset state when modal opens/item changes
  useEffect(() => {
    if (isOpen) {
      setQuantity(1);
      setNotes('');
    }
  }, [isOpen, item]);

  if (!isOpen || !item) return null;

  const handleAddToCart = () => {
    onAddToCart(item, quantity, notes);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center pointer-events-none">
      <div 
        className="absolute inset-0 bg-black/80 backdrop-blur-sm pointer-events-auto transition-opacity duration-300" 
        onClick={onClose} 
      />
      
      <div className="bg-slate-900 w-full sm:w-[480px] h-[85vh] sm:h-auto sm:max-h-[90vh] rounded-t-3xl sm:rounded-3xl shadow-2xl flex flex-col pointer-events-auto transform transition-transform duration-300 animate-in slide-in-from-bottom overflow-hidden border-t-2 border-t-orange-200/60 border-b-2 border-b-white/10 border-x border-x-slate-800">
        
        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto no-scrollbar pb-24">
          <div className="relative h-64 sm:h-72 w-full">
            <img 
              src={item.image} 
              alt={item.name} 
              className="w-full h-full object-cover"
            />
            <button 
              onClick={onClose}
              className="absolute top-4 right-4 bg-black/40 backdrop-blur-md p-2 rounded-full text-white hover:bg-black/60 transition-colors"
            >
              <X size={24} />
            </button>
            <div className="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-slate-900 to-transparent"></div>
          </div>

          <div className="p-6 -mt-6 relative">
            <div className="flex justify-between items-start mb-2">
              <h2 className="text-2xl font-bold text-white">{item.name}</h2>
              <div className="text-2xl font-bold text-orange-500">
                {new Intl.NumberFormat('vi-VN').format(item.price)}đ
              </div>
            </div>

            <p className="text-slate-400 leading-relaxed mb-6">
              {item.description}
            </p>

            <div className="space-y-6">
              {/* Properties */}
              <div className="flex gap-4">
                <div className="bg-slate-800 border border-slate-700 px-3 py-1.5 rounded-lg text-orange-400 text-sm font-medium">
                  {item.category}
                </div>
                {item.spicyLevel ? (
                  <div className="bg-red-900/20 border border-red-900/40 px-3 py-1.5 rounded-lg text-red-500 text-sm font-medium flex items-center gap-1">
                    {Array.from({ length: item.spicyLevel }).map((_, i) => (
                      <Flame key={i} size={14} fill="currentColor" />
                    ))}
                    <span className="ml-1">Cay</span>
                  </div>
                ) : null}
              </div>

              {/* Notes */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Ghi chú cho bếp (Tùy chọn)
                </label>
                <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Ví dụ: Không hành, ít cay..."
                  className="w-full border border-slate-700 rounded-xl p-3 text-sm focus:ring-2 focus:ring-orange-600 focus:border-transparent outline-none bg-slate-950 text-white resize-none h-24 placeholder:text-slate-600"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Sticky Bottom Action */}
        <div className="absolute bottom-0 left-0 right-0 bg-slate-900 border-t border-slate-800 p-4 sm:p-6 pb-8 sm:pb-6 z-10">
          <div className="flex items-center justify-between gap-6">
            {/* Quantity Controls */}
            <div className="flex items-center gap-3 bg-slate-950 border border-slate-800 rounded-full p-1.5">
              <button 
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                className={`w-10 h-10 flex items-center justify-center rounded-full bg-slate-800 shadow-sm transition-all ${quantity === 1 ? 'text-slate-600 cursor-not-allowed' : 'text-slate-300 hover:text-white hover:bg-slate-700 active:scale-95'}`}
                disabled={quantity === 1}
              >
                <Minus size={18} />
              </button>
              <span className="font-bold text-lg w-6 text-center text-white">{quantity}</span>
              <button 
                onClick={() => setQuantity(quantity + 1)}
                className="w-10 h-10 flex items-center justify-center rounded-full bg-slate-800 shadow-sm text-slate-300 hover:text-white hover:bg-slate-700 active:scale-95 transition-all"
              >
                <Plus size={18} />
              </button>
            </div>

            {/* Add Button */}
            <button 
              onClick={handleAddToCart}
              className="flex-1 bg-gradient-to-r from-orange-600 to-red-600 text-white py-3.5 rounded-full font-bold text-lg shadow-lg shadow-orange-900/50 active:scale-95 transition-transform flex items-center justify-center gap-2 border border-orange-500/20"
            >
              <ShoppingBag size={20} />
              <span>Thêm • {new Intl.NumberFormat('vi-VN').format(item.price * quantity)}đ</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};