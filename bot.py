import os
import requests
from pyrogram import Client, filters, idle

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
SOURCE_CHANNEL_ID = os.environ.get("SOURCE_CHANNEL_ID")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# این بخش رو تغییر دادم تا یوزرنیم‌ها (اگر با @ شروع بشن) هم درست شناسایی بشن
if SOURCE_CHANNEL_ID.startswith('@'):
    # یوزرنیم رو همونطور که هست نگه دار (پایروگرام خودش با @ هم میشناسه)
    channel_target = SOURCE_CHANNEL_ID 
else:
    # اگر عدد بود (مثل -100...) تبدیل به int بشه
    channel_target = int(SOURCE_CHANNEL_ID)

app = Client("n8n_forwarder", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# حالا فیلتر رو روی متغیر جدید تنظیم می‌کنیم
@app.on_message(filters.chat(channel_target))
async def forward_to_n8n(client, message):
    text = message.text or message.caption or ""
    
    data = {
        "message_id": message.id,
        "channel_title": message.chat.title if message.chat else "",
        "text": text,
        "date": str(message.date),
        "message_link": message.link if message.link else ""
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        print(f"✅ Message {message.id} sent to n8n! Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending to n8n: {e}")

async def main():
    print("🚀 Starting Userbot...")
    await app.start()
    
    print("🔄 Caching chats...")
    try:
        async for dialog in app.get_dialogs():
            pass
        print("✅ Cache populated successfully!")
    except Exception as e:
        print(f"⚠️ Cache warning: {e}")

    print("🎧 Listening to new messages...")
    await idle()
    await app.stop()

app.run(main())
