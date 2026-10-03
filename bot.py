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
    print(f"👀 پیام جدید در: {chat_title} | آیدی: {chat_id}")

async def main():
    print("🚀 Starting Debug Mode...")
    await app.start()
    
    # این بخش اضافه شد تا مشکل Peer ID که در عکس فرستادی کاملاً حل شود
    print("🔄 Caching chats to fix Peer ID error...")
    try:
        async for dialog in app.get_dialogs():
            pass
        print("✅ Cache ready!")
    except Exception as e:
        print(f"⚠️ Cache error: {e}")

    print("🎧 Listening to ALL incoming messages...")
    await idle()
    await app.stop()

app.run(main())
