import logging
import requests
import time
from flask import current_app
from abc import ABC, abstractmethod
from google_service import IGoogleCloudService
from openai_service import IChatGPTService


class IFacebookService(ABC):
    @abstractmethod
    def post_to_facebook(self, message: str) -> dict:
        pass

class IWhatsAppService(ABC):
    @abstractmethod
    def respond_to_whatsapp(self, sender: str, message: str) -> dict:
        pass




class FacebookService(IFacebookService):
    def __init__(self):
        pass

    def post_to_facebook(self, message: str) -> dict:
        """Posts a message to Facebook."""
        url = f"{current_app.config["FACEBOOK_GRAPH_URL"]}?access_token={current_app.config["FACEBOOK_PAGE_ACCESS_TOKEN"]}"
        payload = {"message": message}
        response = requests.post(url, data=payload)

        if response is None:
            logging.info("Facebook API did not return a response: " + response.json())
            return
        
        return response.json()


class WhatsAppService(IWhatsAppService):
    def __init__(self, google_service: IGoogleCloudService, chat_service: IChatGPTService):

        # Inject dependencies
        self.google_service = google_service
        self.chat_service = chat_service

    def respond_to_whatsapp(self, sender: str, message: str) -> dict:
        """Handles WhatsApp message, generates response using ChatGPT, and stores lead in Google Cloud."""
        response_text = self.chat_service.get_response(message)

        # Store lead data in Google Sheets and Google Cloud Storage
        lead_data = {"sender": sender, "message": message, "response": response_text}
        self.google_service.store_lead(sender, sender, message)
        self.google_service.store_data_gcp(lead_data, f"leads/{sender}_{int(time.time())}.json")

        # Send response via WhatsApp API
        url = current_app.config["WHATSAPP_API_URL"]
        payload = {"recipient": sender, "message": response_text}
        headers = {"Authorization": f"Bearer {current_app.config["WHATSAPP_API_KEY"]}"}
        response = requests.post(url, json=payload, headers=headers)

        if response is None:
            logging.info("WhatsApp API did not return a response: " + response.json())
            return

        return response.json()
