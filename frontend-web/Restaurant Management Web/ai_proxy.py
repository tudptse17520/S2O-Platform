# backend/ai_proxy.py
import os
import requests
from typing import Any, Dict, Optional

# Đọc key từ biến môi trường (backend/.env phải có GEMINI_API_KEY)
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
DEFAULT_MODEL = os.environ.get("GEMINI_DEFAULT_MODEL", "gemini-2.5-flash")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

if not GEMINI_KEY:
    # Trả về lỗi rõ ràng nếu key chưa set
    raise RuntimeError("GEMINI_API_KEY is not set in environment (check backend/.env)")

def list_models() -> Dict[str, Any]:
    """
    List models that the key has access to.
    Trả về JSON từ API (hoặc dict error).
    """
    url = f"{BASE_URL}/models?key={GEMINI_KEY}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        # trả về dict có key 'error' để app.py xử lý
        try:
            return {"error": str(e), "detail": r.json() if 'r' in locals() and hasattr(r, "json") else None}
        except Exception:
            return {"error": str(e)}

def generate_content(request_body: Dict[str, Any], model: Optional[str] = None, timeout: int = 20) -> Dict[str, Any]:
    """
    Gọi endpoint generateContent.
    request_body phải theo định dạng bạn gửi từ frontend.
    Trả về JSON từ API hoặc dict lỗi { "error": ... }.
    """
    model = model or DEFAULT_MODEL
    url = f"{BASE_URL}/models/{model}:generateContent?key={GEMINI_KEY}"
    headers = {"Content-Type": "application/json"}
    try:
        r = requests.post(url, headers=headers, json=request_body, timeout=timeout)
    except requests.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

    # parse json nếu có
    try:
        data = r.json()
    except ValueError:
        return {"error": "Invalid JSON response from model", "status_code": r.status_code, "text": r.text}

    if r.status_code >= 400:
        return {"error": "Model returned error", "status_code": r.status_code, "detail": data}

    return data
