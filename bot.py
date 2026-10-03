import os
from pyrogram import Client, filters, idle

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# استفاده مستقیم از یوزرنیم بدون @
TARGET_USERNAME = "abshode_abasnezhad"

app = Client("n8n_forwarder", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# فیلتر مستقیم روی یوزرنیم
@app.on_message(filters.chat(TARGET_USERNAME))
async def target_messages(client, message):
    print(f"🎯🎯🎯 پیام جدید از کانال عباس نژاد دریافت شد! | آیدی پیام: {message.id} 🎯🎯🎯")

async def main():
    print("🚀 Starting...")
    await app.start()
    
    print(f"🔄 در حال اتصال مستقیم و زوری به کانال @{TARGET_USERNAME}...")
    try:
        # ربات را مجبور می‌کنیم اطلاعات کانال را با یوزرنیم بگیرد و در صورت نیاز عضو شود
        chat = await app.join_chat(TARGET_USERNAME)
        print(f"✅ ربات با موفقیت به کانال متصل شد! آیدی دقیق سرور: {chat.id}")
    except Exception as e:
        print(f"⚠️ اخطار در عضویت خودکار (احتمالاً از قبل عضو است): {e}")
        try:
            # اگر از قبل عضو بود و ارور داد، فقط اطلاعاتش را می‌گیریم که تو کش ذخیره بشه
            chat = await app.get_chat(TARGET_USERNAME)
            print(f"✅ اطلاعات کانال با موفقیت دریافت شد. آیدی: {chat.id}")
        except Exception as ex:
            print(f"❌ خطای کامل در ارتباط با کانال: {ex}")

    print(f"🎧 Listening ONLY to @{TARGET_USERNAME}...")
    await idle()
    await app.stop()

app.run(main())
