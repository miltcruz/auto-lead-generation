import logging
from flask import current_app
from abc import ABC, abstractmethod
from openai import OpenAI

class IDeepSeekCkhat(ABC):
    @abstractmethod
    def chat(self, message: str) -> str:
        pass


class DeepSeekChat(IDeepSeekCkhat):
    def __init__(self):
        self.client = OpenAI(api_key=current_app.config["DEEPSEEK_API_KEY"], base_url=current_app.config["DEEPSEEK_BASE_URL"])

    def chat(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model=current_app.config["DEEPSEEK_MODEL"],
            messages=[
                {"role": "system", "content": current_app.config["AI_CONTENT_TYPE"]},
                {"role": "user", "content": message},
            ],
            stream=False
        )

        content = response.choices[0].message.content

        if content is None or content == "":
            logging.info("Deep Seek Chat did not return a response: " + content)
            return

        return content
