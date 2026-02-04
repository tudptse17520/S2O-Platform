import { User, LoginRequest, RegisterRequest, Restaurant, Review } from '../types';
import { MOCK_USER, RESTAURANTS } from '../constants';

// Cấu hình URL Backend Python (Ví dụ: FastAPI hoặc Flask chạy ở port 8000)
const API_URL = 'http://localhost:8000/api';

/**
 * Helper để gọi API. Nếu lỗi kết nối, sẽ trả về null để fallback sang Mock Data
 * giúp app không bị crash khi chưa bật Backend.
 */
async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T | null> {
  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        // Thêm token nếu có trong localStorage
        ...(localStorage.getItem('token') ? { 'Authorization': `Bearer ${localStorage.getItem('token')}` } : {})
      },
      ...options,
    });
    if (!response.ok) throw new Error('API Error');
    return await response.json();
  } catch (error) {
    console.warn(`Backend connection failed for ${endpoint}. Using Mock Data.`);
    return null;
  }
}

export const api = {
  // --- AUTH ---
  login: async (data: LoginRequest): Promise<User> => {
    const result = await fetchAPI<User>('/login', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    
    // Mock logic nếu backend chưa chạy
    if (!result) {
      if (data.email === 'admin@gmail.com' && data.password === '123456') {
        return { ...MOCK_USER, email: data.email, token: 'mock-jwt-token' };
      }
      throw new Error('Email hoặc mật khẩu không đúng (Mock: dùng admin@gmail.com / 123456)');
    }
    return result;
  },

  register: async (data: RegisterRequest): Promise<User> => {
    const result = await fetchAPI<User>('/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });

    if (!result) {
      return { 
        ...MOCK_USER, 
        id: 'new-user',
        name: data.name, 
        email: data.email, 
        token: 'mock-jwt-token-new' 
      };
    }
    return result;
  },

  // --- DATA ---
  getRestaurants: async (): Promise<Restaurant[]> => {
    const result = await fetchAPI<Restaurant[]>('/restaurants');
    return result || RESTAURANTS;
  },

  getUserProfile: async (): Promise<User> => {
    const result = await fetchAPI<User>('/me');
    return result || MOCK_USER;
  },

  // --- ACTIONS ---
  submitReview: async (restaurantId: string, review: Omit<Review, 'id' | 'userName'>): Promise<Review> => {
    const result = await fetchAPI<Review>(`/restaurants/${restaurantId}/reviews`, {
      method: 'POST',
      body: JSON.stringify(review),
    });
    
    if (!result) {
      return {
        id: Date.now().toString(),
        userId: review.userId,
        userName: 'Bạn', // Tạm thời
        rating: review.rating,
        comment: review.comment,
        date: review.date,
        restaurantId
      };
    }
    return result;
  },
  
  deleteReview: async (restaurantId: string, reviewId: string): Promise<boolean> => {
      const result = await fetchAPI<{success: boolean}>(`/restaurants/${restaurantId}/reviews/${reviewId}`, {
          method: 'DELETE'
      });
      return result ? result.success : true; 
  }
};