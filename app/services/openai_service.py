from abc import ABC, abstractmethod
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class IChatGPTService(ABC):
    @abstractmethod
    def get_response(self, prompt: str) -> str:
        pass


class ChatGPTService(IChatGPTService):
    def __init__(self):
        self.api_key = os.getenv("OPEN_AI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL")
        self.ai_content_type = os.getenv("AI_CONTENT_TYPE")
        self.client = OpenAI(api_key=self.api_key)

    def get_response(self, prompt: str) -> str:
        response = self.client.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content":  self.ai_content_type },
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
