import os
from typing import List, Dict, Any, Optional

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class OpenAIService:
    """
    Service for interacting with OpenAI API
    Handles chat completions and answer generation for RAG
    """
    
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self._client = None
        
    @property
    def client(self):
        """Lazy initialization of OpenAI client"""
        if self._client is None and OPENAI_AVAILABLE and self.api_key:
            self._client = OpenAI(api_key=self.api_key)
        return self._client

    def generate_answer(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        """
        Generate an answer using RAG - Retrieval Augmented Generation
        Uses context documents to inform the response
        """
        if not self.client:
            # Fallback for when OpenAI is not configured
            return self._generate_fallback_answer(query, context_docs)
        
        # Build context from retrieved documents
        context_text = self._build_context(context_docs)
        
        # Create the prompt
        system_prompt = """You are a helpful restaurant assistant AI. 
Answer questions about the restaurant, menu, and services based on the provided context.
If the context doesn't contain relevant information, politely say you don't have that information.
Be concise and helpful."""

        user_prompt = f"""Context information:
{context_text}

User question: {query}

Please provide a helpful answer based on the context above."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request. Error: {str(e)}"

    def generate_menu_description(self, dish_name: str, ingredients: List[str] = None) -> str:
        """Generate an appealing menu description for a dish"""
        if not self.client:
            return f"Delicious {dish_name} made with care."
        
        prompt = f"Write a short, appetizing menu description (2-3 sentences) for a dish called '{dish_name}'"
        if ingredients:
            prompt += f" made with {', '.join(ingredients)}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception:
            return f"Delicious {dish_name} made with care."

    def generate_recommendation_text(self, customer_history: str) -> str:
        """Generate personalized recommendation text"""
        if not self.client:
            return "Based on your preferences, we recommend trying our popular dishes!"
        
        prompt = f"""Based on this customer's order history: {customer_history}
Suggest 2-3 dishes they might enjoy. Be brief and friendly."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception:
            return "Based on your preferences, we recommend trying our popular dishes!"

    def _build_context(self, context_docs: List[Dict[str, Any]]) -> str:
        """Build context string from retrieved documents"""
        if not context_docs:
            return "No specific context available."
        
        context_parts = []
        for i, doc in enumerate(context_docs[:5], 1):  # Limit to 5 docs
            text = doc.get("text", "")
            if text:
                context_parts.append(f"{i}. {text}")
        
        return "\n".join(context_parts) if context_parts else "No specific context available."

    def _generate_fallback_answer(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        """Generate a fallback answer when OpenAI is not available"""
        if context_docs:
            # Return first relevant context
            first_doc = context_docs[0]
            text = first_doc.get("text", "")
            if text:
                return f"Based on our information: {text[:200]}..."
        
        return (
            f"Thank you for your question about '{query}'. "
            "Our AI assistant is currently unavailable. "
            "Please contact our staff for assistance."
        )