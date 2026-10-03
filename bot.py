import os
import requests
from pyrogram import Client, filters

# ۱. دریافت اطلاعات از متغیرهای تنظیمات Railway
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
SOURCE_CHANNEL_ID = os.environ.get("SOURCE_CHANNEL_ID")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# تبدیل آیدی کانال به عدد (اگر عدد منفی بود) یا نگه داشتن به شکل @username
if SOURCE_CHANNEL_ID.lstrip('-').isdigit():
    SOURCE_CHANNEL_ID = int(SOURCE_CHANNEL_ID)

# ۲. روشن کردن یوزربات
app = Client("n8n_forwarder", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# ۳. وقتی پیام جدیدی تو کانالِ مبدا اومد، این تابع اجرا میشه
@app.on_message(filters.chat(SOURCE_CHANNEL_ID))
def forward_to_n8n(client, message):
    # گرفتن متن پیام (اگر عکس/ویدیو باشه، متن زیرش یا همون کپشن رو میگیره)
    text = message.text or message.caption or ""
    
    # ساختن بسته اطلاعاتی
    data = {
        "message_id": message.id,
        "channel_title": message.chat.title if message.chat else "",
        "text": text,
        "date": str(message.date),
        "message_link": message.link if message.link else ""
    }
    
    # فرستادن اطلاعات به n8n
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        print(f"✅ Message {message.id} sent to n8n! Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending to n8n: {e}")

print("🚀 Userbot is running and listening to the channel...")
app.run()