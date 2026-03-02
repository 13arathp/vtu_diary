from google import genai
from config import settings


class GeminiService:
    def __init__(self):
        self.GEMINI_MODEL_NAME = settings.GEMINI_MODEL_NAME
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
    def get_response(self, prompt: str):
        try:
            response = self.client.models.generate_content(
                model=self.GEMINI_MODEL_NAME,
                contents=prompt,
                config={
                    "temperature": 0.0,
                    "top_p": 1.0,
                    "top_k": 1
                }
            )
            return response.text
        except Exception as e:
            return f"Error connecting to Gemini: {e}"
        