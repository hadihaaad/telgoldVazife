import os
import requests
from pyrogram import Client, filters, idle

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
# آیدی حتما باید به عدد (int) تبدیل شود تا پایروگرام آن را بشناسد
SOURCE_CHANNEL_ID = int(os.environ.get("SOURCE_CHANNEL_ID"))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Client("n8n_forwarder", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# فیلتر کردن پیام‌ها فقط برای همین کانال
@app.on_message(filters.chat(SOURCE_CHANNEL_ID))
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
    
    # کش کردن چت‌ها برای اینکه ربات آیدی عددی بالا را بشناسد و ارور Peer ID ندهد
    print("🔄 Caching chats to prevent Peer ID errors...")
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
