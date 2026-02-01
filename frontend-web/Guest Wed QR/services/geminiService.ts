import { GoogleGenAI } from "@google/genai";
import { MenuItem } from "../types";

// ✅ Vite frontend: dùng import.meta.env và bắt buộc có tiền tố VITE_
const apiKey = import.meta.env.VITE_GEMINI_API_KEY;

if (!apiKey) {
  throw new Error("Missing VITE_GEMINI_API_KEY. Please check .env.local");
}

// Khởi tạo Gemini client
const ai = new GoogleGenAI({ apiKey });

export const getDishRecommendation = async (
  userQuery: string,
  currentMenu: MenuItem[],
): Promise<string> => {
  // Tối ưu context để tiết kiệm token
  const menuContext = currentMenu
    .map(
      (item) =>
        `${item.name} (${item.category}) - ${item.price}đ: ${item.description}`,
    )
    .join("\n");

  const systemInstruction = `
Bạn là một nhân viên phục vụ bàn thông minh, thân thiện tại một nhà hàng Việt Nam.
Nhiệm vụ của bạn là tư vấn món ăn cho khách dựa trên Menu được cung cấp bên dưới.

Quy tắc:
1. Chỉ gợi ý các món có trong Menu.
2. Trả lời ngắn gọn, hấp dẫn, giọng điệu vui vẻ.
3. Nếu khách hỏi món không có, hãy khéo léo gợi ý món tương tự trong Menu.
4. Trả lời bằng tiếng Việt.

Menu Hiện Tại:
${menuContext}
`;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: userQuery,
      config: {
        systemInstruction,
        temperature: 0.7,
        maxOutputTokens: 300,
      },
    });

    return (
      response.text || "Xin lỗi, tôi chưa nghĩ ra câu trả lời ngay lúc này."
    );
  } catch (error) {
    console.error("Gemini API Error:", error);
    return "Hệ thống tư vấn đang bận, bạn vui lòng tự chọn món nhé!";
  }
};
