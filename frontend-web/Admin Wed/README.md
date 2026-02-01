# 🍽️ GuestDine | RestoAdmin Pro

### Hệ Thống Quản Trị Nhà Hàng Thông Minh Tích Hợp AI

[cite_start]**GuestDine** (RestoAdmin Pro) là một nền tảng Dashboard quản trị hiện đại dành cho hệ thống đặt món qua QR Code. Dự án tập trung vào việc tối ưu hóa vận hành nhà hàng bằng các thuật toán AI tiên tiến, giúp cá nhân hóa trải nghiệm khách hàng và quản lý đa chi nhánh (Multi-tenancy) một cách hiệu quả.

---

## ✨ Tính Năng Nổi Bật

- **🤖 Trung Tâm Điều Khiển AI:** Tùy chỉnh tham số cho Chatbot (Gemini 3 Flash/Pro) và tinh chỉnh các trọng số cho thuật toán gợi ý món ăn.
- **📚 RAG (Retrieval-Augmented Generation):** Nạp dữ liệu thực đơn (PDF, CSV, TXT) để AI hỗ trợ khách hàng dựa trên thông tin thực tế của từng nhà hàng.
- [cite_start]**📊 Phân Tích Doanh Thu:** Theo dõi tăng trưởng, phân bổ gói dịch vụ và quản lý giao dịch theo thời gian thực với Recharts.
- [cite_start]**🏢 Quản Lý Nhà Hàng (Tenants):** Quy trình phê duyệt đối tác, quản lý gói đăng ký (Basic, Premium, Enterprise) và trạng thái hoạt động.
- [cite_start]**🔐 Quản Trị Người Dùng:** Phân quyền chi tiết giữa Quản trị viên, Chủ nhà hàng và Khách hàng kèm tính năng khóa/mở tài khoản bảo mật.

## 🛠️ Công Nghệ Sử Dụng

- **Core:** React 19 (StrictMode), TypeScript 5.8.
- **Build Tool:** Vite 6 (Hỗ trợ nạp biến môi trường linh hoạt).
- **UI/UX:** Tailwind CSS, Lucide React (Icons).
- [cite_start]**Data Visualization:** Recharts (Area & Bar Charts).
- **AI Integration:** Google Gemini API (Flash & Pro models).

## 🚀 Cài Đặt và Chạy Local

### 1. Yêu cầu hệ thống

- **Node.js:** Phiên bản 18.0.0 trở lên.

### 2. Các bước cài đặt

```bash
# Cài đặt các thư viện cần thiết
npm install
```

# Chế độ phát triển

npm run dev

Ứng dụng sẽ khả dụng tại: http://localhost:3000.
📂 Cấu Trúc Thư Mục Chính
/views: Chứa các trang chức năng chính (Dashboard, AIConfig, Tenants, Users, Revenue).

**App.tsx:** Luồng điều hướng chính và hệ thống thông báo toàn cục.

**types.ts:** Định nghĩa Interface chặt chẽ cho toàn hệ thống.

**mockData.ts:** Dữ liệu mẫu phục vụ quá trình phát triển.
