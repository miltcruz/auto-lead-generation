import os
import json
import time
import logging
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google.cloud import storage
import gspread
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
        # Load environment variables
        load_dotenv()
        self.google_sheet_credentials = os.getenv("GOOGLE_SHEET_CREDENTIALS")
        self.google_sheet_name = os.getenv("GOOGLE_SHEET_NAME")
        self.gcp_bucket_name = os.getenv("GCP_BUCKET_NAME")
        self.gcp_scope = os.getenv("GOOGLE_SCOPE")
        
        # Google Cloud Storage setup
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(self.gcp_bucket_name)
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.google_sheet_credentials, self.gcp_scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(self.google_sheet_name).sheet1
    
    def store_lead(self, name: str, phone: str, message: str):
        """Store a lead in Google Sheets."""
        self.sheet.append_row([name, phone, message, time.strftime("%Y-%m-%d %H:%M:%S")])
        logging.info("Lead stored successfully")
    
    def store_data_gcp(self, data: dict, filename: str):
        """Store data in Google Cloud Storage."""
        blob = self.bucket.blob(filename)
        blob.upload_from_string(json.dumps(data))
        logging.info(f"Stored {filename} in Google Cloud Storage")