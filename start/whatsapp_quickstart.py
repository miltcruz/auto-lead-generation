import openai
import requests
import json
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request
from google.cloud import storage

# Load environment variables (API Keys)
CHATGPT_API_KEY = "your_openai_api_key"
FACEBOOK_PAGE_ACCESS_TOKEN = "your_facebook_access_token"
TIKTOK_ACCESS_TOKEN = "your_tiktok_access_token"
CALENDLY_API_KEY = "your_calendly_api_key"
WHATSAPP_API_KEY = "your_whatsapp_api_key"
GOOGLE_SHEET_CREDENTIALS = "your_google_sheet_credentials.json"
GOOGLE_SHEET_NAME = "LeadTracking"
GCP_BUCKET_NAME = "your_gcp_bucket_name"

# Google Cloud Storage setup
storage_client = storage.Client()
bucket = storage_client.bucket(GCP_BUCKET_NAME)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEET_CREDENTIALS, scope)
client = gspread.authorize(creds)
sheet = client.open(GOOGLE_SHEET_NAME).sheet1

# Flask app for WhatsApp bot
app = Flask(__name__)

# ChatGPT function for AI responses
def get_chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI assistant for a microgrid business."},
                  {"role": "user", "content": prompt}],
        api_key=CHATGPT_API_KEY
    )
    return response['choices'][0]['message']['content']

# Function to auto-post on Facebook
def post_to_facebook(message):
    url = f"https://graph.facebook.com/v17.0/me/feed?access_token={FACEBOOK_PAGE_ACCESS_TOKEN}"
    payload = {"message": message}
    response = requests.post(url, data=payload)
    return response.json()

# Function to store leads in Google Sheets
def store_lead(name, phone, message):
    sheet.append_row([name, phone, message, time.strftime("%Y-%m-%d %H:%M:%S")])
    print("Lead stored successfully")

# Function to store data in Google Cloud Storage
def store_data_gcp(data, filename):
    blob = bucket.blob(filename)
    blob.upload_from_string(json.dumps(data))
    print(f"Stored {filename} in Google Cloud Storage")

# WhatsApp bot webhook
def respond_to_whatsapp(sender, message):
    response_text = get_chatgpt_response(message)
    lead_data = {"sender": sender, "message": message, "response": response_text}
    store_lead(sender, sender, message)
    store_data_gcp(lead_data, f"leads/{sender}_{int(time.time())}.json")
    url = "https://api.whatsapp.com/send"
    payload = {"recipient": sender, "message": response_text}
    headers = {"Authorization": f"Bearer {WHATSAPP_API_KEY}"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    data = request.json
    sender = data["from"]
    message = data["body"]
    return respond_to_whatsapp(sender, message)

# Function to schedule calls with Calendly
def schedule_call(email, name):
    url = "https://api.calendly.com/scheduled_events"
    payload = {"email": email, "name": name, "event_type": "battery-storage-consultation"}
    headers = {"Authorization": f"Bearer {CALENDLY_API_KEY}"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Function to generate daily marketing posts
def generate_marketing_content():
    prompt = "Generate a short marketing post about home battery storage and VPP programs."
    return get_chatgpt_response(prompt)

# Auto-post marketing content daily
def daily_marketing():
    content = generate_marketing_content()
    post_to_facebook(content)
    print("Posted to Facebook: ", content)

# Run daily marketing task
daily_marketing()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
