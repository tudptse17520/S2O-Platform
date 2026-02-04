
import { Tenant, TenantStatus, User, Payment, AIConfig, AuditLog } from './types';

export const MOCK_TENANTS: Tenant[] = [
  { 
    tenantId: 101, 
    name: "Golden Dragon Seafood", 
    status: TenantStatus.ACTIVE, 
    createdAt: "2023-10-15",
    subscription: { startDate: "2023-10-15", endDate: "2024-10-15", plan: "Premium" }
  },
  { 
    tenantId: 102, 
    name: "Pizza Heaven", 
    status: TenantStatus.PENDING, 
    createdAt: "2023-12-01",
    subscription: { startDate: "2023-12-01", endDate: "2024-12-01", plan: "Basic" }
  },
  { 
    tenantId: 103, 
    name: "Sushi Master", 
    status: TenantStatus.ACTIVE, 
    createdAt: "2023-08-20",
    subscription: { startDate: "2023-08-20", endDate: "2024-08-20", plan: "Enterprise" }
  },
  { 
    tenantId: 104, 
    name: "Burger Kingly", 
    status: TenantStatus.INACTIVE, 
    createdAt: "2023-05-10",
    subscription: { startDate: "2023-05-10", endDate: "2023-11-10", plan: "Basic" }
  },
];

export const MOCK_USERS: User[] = [
  { userId: 1, email: "admin@restopro.com", role: "ADMIN", status: "ACTIVE", lastLogin: "2024-05-20" },
  { userId: 2, email: "owner@goldendragon.com", role: "RESTAURANT_OWNER", status: "ACTIVE", lastLogin: "2024-05-19" },
  { userId: 3, email: "customer1@gmail.com", role: "CUSTOMER", status: "LOCKED", lastLogin: "2024-04-12" },
  { userId: 4, email: "customer2@yahoo.com", role: "CUSTOMER", status: "ACTIVE", lastLogin: "2024-05-21" },
];

export const MOCK_PAYMENTS: Payment[] = [
  { paymentId: 5001, tenantId: 101, amount: 299.99, method: "Stripe", paidAt: "2024-05-01" },
  { paymentId: 5002, tenantId: 103, amount: 599.99, method: "PayPal", paidAt: "2024-05-05" },
  { paymentId: 5003, tenantId: 101, amount: 299.99, method: "Stripe", paidAt: "2024-04-01" },
  { paymentId: 5004, tenantId: 102, amount: 99.00, method: "Bank Transfer", paidAt: "2024-05-10" },
];

export const MOCK_AI_CONFIG: AIConfig = {
  configId: 1,
  isEnabled: true,
  chatbot: {
    model: "gemini-3-flash-preview",
    temperature: 0.7,
    ragEnabled: true,
    topK: 5,
    chunkSize: 512
  },
  recommendation: {
    vectorWeight: 0.6,
    ruleWeight: 0.4,
    embeddingModel: "text-embedding-004",
    minRatingThreshold: 4.0,
    orderHistoryWeight: 0.35,
    userPreferenceWeight: 0.45,
    contextWeight: 0.20
  },
  updatedAt: "2024-05-15 14:30:00"
};

export const MOCK_AUDIT_LOGS: AuditLog[] = [
  { logId: 1, action: "APPROVE_TENANT", timestamp: "2024-05-20 10:00:00", adminId: 1 },
  { logId: 2, action: "LOCK_USER", timestamp: "2024-05-20 11:30:00", adminId: 1 },
];
