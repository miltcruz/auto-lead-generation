# Automated AI Lead Generation Service

## Overview

This Python-based AI service automates lead generation, customer interaction, and marketing for a your business. It integrates with ChatGPT API, WhatsApp, Facebook, Google Sheets, Calendly, and Google Cloud Storage to manage customer inquiries and schedule consultations.

## Features

- AI Chatbot: Responds to customer inquiries via WhatsApp and Facebook Messenger.

- Lead Tracking: Stores leads in Google Sheets and Google Cloud Storage.

- Marketing Automation: Generates and posts daily content to Facebook.

- Appointment Scheduling: Uses Calendly API to book customer consultations.

- Google Cloud Deployment: Runs on Google Cloud Run with scalable architecture.

## Requirements

- Python 3.8+

- Google Cloud Project with Cloud Run & Cloud Storage enabled

- API Keys for:

  - OpenAI (ChatGPT API)
  - Facebook Page Access Token
  - TikTok API (optional for future expansion)
  - WhatsApp Business API
  - Google Sheets API
  - Calendly API

Setup Instructions

1. Clone Repository

        git clone https://github.com/your-repo/lead-gen-bot.git
        cd lead-gen-bot

2. Install Dependencies

        pip install -r requirements.txt

3. Set Up Environment Variables

Create a .env file and add:

        CHATGPT_API_KEY=your_openai_api_key
        FACEBOOK_PAGE_ACCESS_TOKEN=your_facebook_access_token
        TIKTOK_ACCESS_TOKEN=your_tiktok_access_token
        CALENDLY_API_KEY=your_calendly_api_key
        WHATSAPP_API_KEY=your_whatsapp_api_key
        GOOGLE_SHEET_CREDENTIALS=your_google_sheet_credentials.json
        GCP_BUCKET_NAME=your_gcp_bucket_name

4. Deploy on Google Cloud Run

Authenticate with Google Cloud

        gcloud auth login
        gcloud config set project your-gcp-project-id

Build & Deploy Container

        gcloud builds submit --tag gcr.io/your-gcp-project-id/lead-gen-bot
        gcloud run deploy lead-gen-bot --image gcr.io/your-gcp-project-id/lead-gen-bot --platform managed --allow-unauthenticated --region us-central1

## Usage

- WhatsApp Bot: Users send a message; AI chatbot responds and captures lead.

- Facebook Auto-Posting: AI generates marketing posts and publishes daily.

- Google Sheets Storage: All leads are logged for future follow-ups.

- Calendly Scheduling: Qualified leads can book an installation consultation.


## Future Enhancements

- TikTok Video Marketing Automation

- Integration with Additional CRM Tools

- Multi-Language AI Support
