import { GoogleGenAI } from "@google/genai";
import { Restaurant } from "../types";

// 1. Dùng import.meta.env cho Vite và thêm fallback để tránh lỗi crash nếu quên set key
const apiKey = import.meta.env.VITE_GEMINI_API_KEY || "";
const ai = new GoogleGenAI({ apiKey: apiKey });

export const generateRestaurantResponse = async (
  message: string,
  restaurant: Restaurant,
): Promise<string> => {
  // Kiểm tra nếu chưa có key thì báo lỗi ngay, đỡ gọi API
  if (!apiKey) {
    console.error("Thiếu API Key trong file .env.local");
    return "Lỗi cấu hình hệ thống: Thiếu API Key.";
  }

  try {
    const systemPrompt = `
      Bạn là một trợ lý AI hữu ích và thân thiện cho nhà hàng tên là "${restaurant.name}".
      
      Thông tin nhà hàng:
      - Địa chỉ: ${restaurant.address}
      - Loại hình: ${restaurant.category}
      - Mô tả: ${restaurant.description}
      - Món ăn tiêu biểu: ${restaurant.menu.map((m) => m.name + ` (${m.price}đ)`).join(", ")}
      
      Nhiệm vụ của bạn:
      1. Trả lời các câu hỏi của khách hàng về thực đơn, giờ mở cửa, vị trí, và đề xuất món ăn.
      2. Luôn giữ thái độ lịch sự, chuyên nghiệp nhưng gần gũi.
      3. Nếu khách hàng hỏi về việc đặt bàn, hãy hướng dẫn họ nhấn nút "Đặt Bàn" trên ứng dụng.
      4. Trả lời ngắn gọn (dưới 100 từ) vì đây là giao diện chat trên mobile.
      
      Khách hàng hỏi: "${message}"
    `;

    const response = await ai.models.generateContent({
      model: "gemini-1.5-flash", // 2. Sửa lại tên model chính xác
      contents: [
        {
          parts: [{ text: systemPrompt }],
        },
      ],
    });

    // 3. Truy xuất text đúng cách từ response object của SDK mới
    return (
      response.response?.text() ||
      "Xin lỗi, tôi không thể trả lời ngay lúc này."
    );
  } catch (error) {
    console.error("Gemini API Error:", error);
    return "Hệ thống đang bận, vui lòng thử lại sau.";
  }
};