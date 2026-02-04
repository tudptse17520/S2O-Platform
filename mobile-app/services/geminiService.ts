import { GoogleGenAI } from "@google/genai";
import { Restaurant } from "../types";

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

export const generateRestaurantResponse = async (
  message: string,
  restaurant: Restaurant
): Promise<string> => {
  try {
    const systemPrompt = `
      Bạn là một trợ lý AI hữu ích và thân thiện cho nhà hàng tên là "${restaurant.name}".
      
      Thông tin nhà hàng:
      - Địa chỉ: ${restaurant.address}
      - Loại hình: ${restaurant.category}
      - Mô tả: ${restaurant.description}
      - Món ăn tiêu biểu: ${restaurant.menu.map(m => m.name + ` (${m.price}đ)`).join(', ')}
      
      Nhiệm vụ của bạn:
      1. Trả lời các câu hỏi của khách hàng về thực đơn, giờ mở cửa, vị trí, và đề xuất món ăn.
      2. Luôn giữ thái độ lịch sự, chuyên nghiệp nhưng gần gũi.
      3. Nếu khách hàng hỏi về việc đặt bàn, hãy hướng dẫn họ nhấn nút "Đặt Bàn" trên ứng dụng.
      4. Trả lời ngắn gọn (dưới 100 từ) vì đây là giao diện chat trên mobile.
      
      Khách hàng hỏi: "${message}"
    `;

    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: systemPrompt,
    });

    return response.text || "Xin lỗi, tôi không thể trả lời ngay lúc này.";
  } catch (error) {
    console.error("Gemini API Error:", error);
    return "Hệ thống đang bận, vui lòng thử lại sau.";
  }
};