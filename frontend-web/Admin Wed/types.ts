
export enum TenantStatus {
  ACTIVE = 'ACTIVE',
  PENDING = 'PENDING',
  INACTIVE = 'INACTIVE'
}

export interface TenantSubscription {
  startDate: string;
  endDate: string;
  plan: 'Basic' | 'Premium' | 'Enterprise';
}

export interface Tenant {
  tenantId: number;
  name: string;
  status: TenantStatus;
  createdAt: string;
  subscription?: TenantSubscription;
}

export interface User {
  userId: number;
  email: string;
  role: 'ADMIN' | 'RESTAURANT_OWNER' | 'CUSTOMER';
  status: 'ACTIVE' | 'LOCKED';
  lastLogin: string;
}

export interface Payment {
  paymentId: number;
  tenantId: number;
  amount: number;
  method: string;
  paidAt: string;
}

export interface ChatbotConfig {
  model: string;
  temperature: number;
  ragEnabled: boolean;
  topK: number;
  chunkSize: number;
}

export interface RecommendationConfig {
  vectorWeight: number; // Weight for Semantic Matching (0-1)
  ruleWeight: number;   // Weight for Rule-based (0-1)
  embeddingModel: string;
  minRatingThreshold: number;
  // Specific Algorithm Inputs as per user request
  orderHistoryWeight: number;
  userPreferenceWeight: number;
  contextWeight: number; // Time & Location
}

export interface AIConfig {
  configId: number;
  isEnabled: boolean;
  chatbot: ChatbotConfig;
  recommendation: RecommendationConfig;
  updatedAt: string;
}

export interface AuditLog {
  logId: number;
  action: string;
  timestamp: string;
  adminId: number;
}
