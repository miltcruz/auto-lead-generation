import os
import requests
import json
import time
import gspread
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from flask import Flask, request
from google.cloud import storage
from abc import ABC, abstractmethod

class ICalendlyService(ABC):
    @abstractmethod
    def schedule_call(self, email: str, name: str):
        pass
 

class CalendlyService(ICalendlyService):
    def __init__(self):
        self.calendly_api_key = os.getenv("CALENDLY_API_KEY")
        self.calendly_base_url = os.getenv("CALENDLY_BASE_URL")
        self.calendly_event_type = os.getenv("CALENDLY_EVENT_TYPE")
        

    def schedule_call(self, email, name) -> dict:
        url = self.calendly_base_url
        payload = {"email": email, "name": name, "event_type": self.calendly_event_type}
        headers = {"Authorization": f"Bearer {self.calendly_api_key}"}
        response = requests.post(url, json=payload, headers=headers)
        return response.json()