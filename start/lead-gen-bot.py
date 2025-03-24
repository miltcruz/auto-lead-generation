from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from flask import Flask, request
from app.services.meta_service import FacebookService, WhatsAppService
from app.services.openai_service import ChatGPTService

# Flask app for WhatsApp bot
app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    data = request.json
    sender = data["from"]
    message = data["body"]
    return WhatsAppService.respond_to_whatsapp(sender, message)

# Auto-post marketing content daily
def daily_marketing(prompt: str):
    content = ChatGPTService.get_response(prompt)
    print("Posted to content: ", content)
    assitant_content = ChatGPTService.get_assitant_response(prompt)
    print("Posted to assitant_content: ", assitant_content)
    #FacebookService.post_to_facebook(content)
    #print("Posted to Facebook: ", content)

# Run daily marketing task
daily_marketing("Generate a message promoting programs offered by utility companies and government incentives in WA. Make sure to include specific utility programs and incentives available in the state.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
