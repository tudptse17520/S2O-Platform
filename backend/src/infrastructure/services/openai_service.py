class OpenAIService:

    def generate_answer(self, query, context_docs):
        return f"(AI answer) You asked: {query}. Found {len(context_docs)} related documents."