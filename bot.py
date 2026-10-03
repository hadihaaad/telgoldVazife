import os
from pyrogram import Client, filters, idle

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

app = Client("n8n_forwarder", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.all)
async def debug_messages(client, message):
    chat_title = message.chat.title if message.chat else "Private/Unknown"
    chat_id = message.chat.id if message.chat else "No ID"
    print(f"👀 پیام جدید دیده شد! چت: {chat_title} | آیدی: {chat_id}")

async def main():
    print("🚀 Starting Debug Mode...")
    await app.start()
    print("🎧 Listening to ALL incoming messages without any filters...")
    await idle()
    await app.stop()

app.run(main())
