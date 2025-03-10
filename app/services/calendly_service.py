import logging
import requests
from flask import current_app
from abc import ABC, abstractmethod

class ICalendlyService(ABC):
    @abstractmethod
    def schedule_call(self, email: str, name: str):
        pass
 

class CalendlyService(ICalendlyService):
    def __init__(self):
        pass

    
    def schedule_call(self, email, name) -> dict:
        url = current_app.config["CALENDLY_BASE_URL"]
        payload = {"email": email, "name": name, "event_type": current_app.config["CALENDLY_EVENT_TYPE"] }
        headers = {"Authorization": f"Bearer {current_app.config["CALENDLY_API_KEY"]}"}
        response = requests.post(url, json=payload, headers=headers)

        if response is None:
            logging.info("Calendly API did not return a response: " + response.json())
            return
        
        return response.json()