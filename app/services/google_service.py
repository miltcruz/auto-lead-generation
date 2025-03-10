import json
import time
import gspread
import logging
from flask import current_app
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google.cloud import storage
from abc import ABC, abstractmethod

class IGoogleCloudService(ABC):
    @abstractmethod
    def store_lead(self, name: str, phone: str, message: str):
        pass
    
    @abstractmethod
    def store_data_gcp(self, data: dict, filename: str):
        pass

class GoogleCloudService(IGoogleCloudService):
    def __init__(self):

        # Google Cloud Storage setup
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(current_app.config["GCP_BUCKET_NAME"])

        creds = ServiceAccountCredentials.from_json_keyfile_name(current_app.config["GOOGLE_SHEET_CREDENTIALS"], current_app.config["GOOGLE_SCOPE"])
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(current_app.config["GOOGLE_SHEET_NAME"]).sheet1
    
    def store_lead(self, name: str, phone: str, message: str):
        """Store a lead in Google Sheets."""
        self.sheet.append_row([name, phone, message, time.strftime("%Y-%m-%d %H:%M:%S")])
        logging.info("Lead stored successfully")
    
    def store_data_gcp(self, data: dict, filename: str):
        """Store data in Google Cloud Storage."""
        blob = self.bucket.blob(filename)
        blob.upload_from_string(json.dumps(data))
        logging.info(f"Stored {filename} in Google Cloud Storage")