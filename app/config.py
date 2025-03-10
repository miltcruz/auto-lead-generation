import sys
import os
from dotenv import load_dotenv
import logging


def load_configurations(app):
    load_dotenv()
    app.config["ACCESS_TOKEN"] = os.getenv("ACCESS_TOKEN")
    app.config["YOUR_PHONE_NUMBER"] = os.getenv("YOUR_PHONE_NUMBER")
    app.config["APP_ID"] = os.getenv("APP_ID")
    app.config["APP_SECRET"] = os.getenv("APP_SECRET")
    app.config["RECIPIENT_WAID"] = os.getenv("RECIPIENT_WAID")
    app.config["VERSION"] = os.getenv("VERSION")
    app.config["PHONE_NUMBER_ID"] = os.getenv("PHONE_NUMBER_ID")
    app.config["VERIFY_TOKEN"] = os.getenv("VERIFY_TOKEN")
    
    app.config["GOOGLE_SHEET_CREDENTIALS"]  = os.getenv("GOOGLE_SHEET_CREDENTIALS")
    app.config["GOOGLE_SHEET_NAME"] = os.getenv("GOOGLE_SHEET_NAME")
    app.config["GCP_BUCKET_NAME"]  = os.getenv("GCP_BUCKET_NAME")
    app.config["GOOGLE_SCOPE"] = os.getenv("GOOGLE_SCOPE")

    app.config["DEEPSEEK_API_KEY"] = os.getenv("DEEPSEEK_API_KEY")
    app.config["DEEPSEEK_BASE_URL"] = os.getenv("DEEPSEEK_BASE_URL")
    app.config["DEEPSEEK_MODEL"] = os.getenv("DEEPSEEK_MODEL")

    app.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    app.config["OPENAI_MODEL"] = os.getenv("OPENAI_MODEL")

    app.config["FACEBOOK_PAGE_ACCESS_TOKEN"] = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
    app.config["FACEBOOK_GRAPH_URL"] = os.getenv("FACEBOOK_GRAPH_URL")
    app.config["WHATSAPP_API_KEY"] = os.getenv("WHATSAPP_API_KEY")
    app.config["WHATSAPP_API_URL"] = os.getenv("WHATSAPP_API_URL")

    app.config["CALENDLY_API_KEY"]  = os.getenv("CALENDLY_API_KEY")
    app.config["CALENDLY_BASE_URL"]  = os.getenv("CALENDLY_BASE_URL")
    app.config["CALENDLY_EVENT_TYPE"]  = os.getenv("CALENDLY_EVENT_TYPE")

    app.config["AI_CONTENT_TYPE"] = os.getenv("AI_CONTENT_TYPE")


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
