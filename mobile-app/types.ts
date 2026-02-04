export enum MembershipTier {
  SILVER = 'Bạc',
  GOLD = 'Vàng',
  DIAMOND = 'Kim Cương'
}

export interface Review {
  id: string;
  userId: string;
  userName: string;
  rating: number;
  comment: string;
  date: string;
  restaurantId: string;
}

export interface MenuItem {
  id: string;
  name: string;
  price: number;
  image: string;
  description: string;
}

export interface Restaurant {
  id: string;
  name: string;
  address: string;
  rating: number;
  image: string;
  category: string;
  priceRange: string; // e.g., $$, $$$
  description: string;
  menu: MenuItem[];
  lat: number;
  lng: number;
  reviews: Review[];
}

export interface HistoryItem {
  id: string;
  restaurantName: string;
  date: string;
  total: number;
  items: string[]; // List of dish names
}

export interface User {
  id: string;
  name: string;
  email: string; // Added email
  avatar: string;
  tier: MembershipTier;
  points: number;
  totalSpent: number;
  history: HistoryItem[];
  token?: string; // JWT token from Python backend
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'model';
  text: string;
  timestamp: Date;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
}