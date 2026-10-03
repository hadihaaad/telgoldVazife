import os
from pyrogram import Client, filters, idle
from pyrogram.errors import PeerIdInvalid

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# آیدی کانال هدف را اینجا قرار دادم
TARGET_CHANNEL_ID = -1002385788148

app = Client("n8n_forwarder", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.all)
async def debug_messages(client, message):
    chat_title = message.chat.title if message.chat else "Private/Unknown"
    chat_id = message.chat.id if message.chat else "No ID"
    print(f"👀 پیام جدید در: {chat_title} | آیدی: {chat_id}")
    
    # اگر پیام از کانال هدف بود، یک نشانه خاص چاپ کن
    if chat_id == TARGET_CHANNEL_ID:
        print("🎯🎯🎯 پیام از کانال عباس نژاد با موفقیت دریافت شد! 🎯🎯🎯")

async def main():
    print("🚀 Starting...")
    await app.start()
    
    print("🔄 در حال کش کردن اختصاصی کانال عباس نژاد...")
    try:
        # با این دستور، ربات را مجبور می‌کنیم اطلاعات این کانال را مستقیم از سرور بگیرد
        chat = await app.get_chat(TARGET_CHANNEL_ID)
        print(f"✅ کانال هدف با موفقیت شناسایی و کش شد: {chat.title}")
    except PeerIdInvalid:
        print("❌ ارور PeerIdInvalid: ربات هنوز این کانال را نمی‌شناسد! در حال تلاش با کش عمومی...")
        try:
            # اگر مستقیم نتوانست، از روش عمومی استفاده می‌کنیم ولی با لیمیت بیشتر
            async for _ in app.get_dialogs(limit=500): 
                pass
            print("✅ کش عمومی کامل شد.")
        except Exception as e:
            print(f"⚠️ خطای کش عمومی: {e}")
    except Exception as e:
        print(f"❌ خطای ناشناخته در کش اختصاصی: {e}")

    print("🎧 Listening to ALL incoming messages...")
    await idle()
    await app.stop()

app.run(main())
