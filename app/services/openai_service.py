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
    
    def get_assitant_response(prompt):
        # Create a new thread
        thread = current_app.client.beta.threads.create()

        # Send a message to the thread
        current_app.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )

        # Run the assistant
        run = current_app.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=current_app.config["OPENAI_ASSISTANT_ID"]
        )

        # Wait for completion
        while run.status in ["queued", "in_progress"]:
            run = current_app.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        # Retrieve messages from the thread
        response = current_app.client.beta.threads.messages.list(thread_id=thread.id)

        # Get the last assistant response
        for msg in reversed(response.data):
            if msg.role == "assistant":
                return msg.content[0].text.value

        return "No response received from the assistant."