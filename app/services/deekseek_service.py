from abc import ABC, abstractmethod
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class IDeepSeekCkhat(ABC):
    @abstractmethod
    def chat(self, message: str) -> str:
        pass


class DeepSeekChat(IDeepSeekCkhat):
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = os.getenv("DEEPSEEK_BASE_URL")
        self.model = os.getenv("DEEPSEEK_MODEL")
        self.ai_content_type = os.getenv("AI_CONTENT_TYPE")

        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def chat(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.ai_content_type},
                {"role": "user", "content": message},
            ],
            stream=False
        )
        return response.choices[0].message.content
