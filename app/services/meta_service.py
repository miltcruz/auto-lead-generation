from abc import ABC, abstractmethod
import requests
import time
import os
from dotenv import load_dotenv
from google_service import IGoogleCloudService
from openai_service import IChatGPTService

# Load environment variables
load_dotenv()


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
        self.facebook_access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
        self.facebook_graph_url = os.getenv("FACEBOOK_GRAPH_URL")

    def post_to_facebook(self, message: str) -> dict:
        """Posts a message to Facebook."""
        url = f"{self.facebook_graph_url}?access_token={self.facebook_access_token}"
        payload = {"message": message}
        response = requests.post(url, data=payload)
        return response.json()


class WhatsAppService(IWhatsAppService):
    def __init__(self, google_service: IGoogleCloudService, chat_service: IChatGPTService):
        self.whatsapp_api_key = os.getenv("WHATSAPP_API_KEY")
        self.whatsapp_api_url = os.getenv("WHATSAPP_API_URL")

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
        url = self.whatsapp_api_url
        payload = {"recipient": sender, "message": response_text}
        headers = {"Authorization": f"Bearer {self.whatsapp_api_key}"}
        response = requests.post(url, json=payload, headers=headers)

        return response.json()
