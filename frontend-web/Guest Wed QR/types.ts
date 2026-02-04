export interface MenuItem {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  image: string;
  spicyLevel?: number; // 0-3
  isPopular?: boolean;
}

export interface CartItem extends MenuItem {
  quantity: number;
  notes?: string;
}

export type OrderStatus = 'pending' | 'preparing' | 'ready' | 'served' | 'paid';

export interface Order {
  id: string;
  tableId: string;
  items: CartItem[];
  status: OrderStatus;
  totalAmount: number;
  createdAt: string;
}

export interface SessionContext {
  tenantId: string;
  branchId: string;
  tableId: string;
  token: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'model';
  text: string;
  isThinking?: boolean;
}
