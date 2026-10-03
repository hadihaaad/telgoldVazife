import os
import requests
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# خواندن مقادیر مستقیماً از Variables در Railway
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
N8N_WEBHOOK = os.environ.get("N8N_WEBHOOK")

# آیدی کانال هدف
TARGET_CHAT = -1001479335313 

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=TARGET_CHAT))
async def handler(event):
    text = event.message.text or ""
    
    data = {
        "text": text,
        "message_id": event.message.id,
        "date": str(event.message.date)
    }

    try:
        response = requests.post(N8N_WEBHOOK, json=data, timeout=10)
        print(f"✅ پیام {event.message.id} به n8n ارسال شد! وضعیت: {response.status_code}")
    except Exception as e:
        print(f"❌ خطا در ارسال پیام به n8n: {e}")

print("🚀 ربات با Telethon روشن شد و منتظر پیام کانال است...")
client.start()
client.run_until_disconnected()
