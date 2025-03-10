import logging
from flask import current_app
from abc import ABC, abstractmethod
from openai import OpenAI

class IChatGPTService(ABC):
    @abstractmethod
    def get_response(self, prompt: str) -> str:
        pass


class ChatGPTService(IChatGPTService):
    def __init__(self):
        self.client = OpenAI(api_key=current_app.config["OPENAI_API_KEY"])

    def get_response(self, prompt: str) -> str:
        response = self.client.ChatCompletion.create(
            model=current_app.config["OPENAI_MODEL"],
            messages=[
                {"role": "system", "content":  current_app.config["AI_CONTENT_TYPE"] },
                {"role": "user", "content": prompt}
            ]
        )

        content = response['choices'][0]['message']['content']

        if content is None or content == "":
            logging.info("ChatGPT did not return a response: " + content)
            return

        return content