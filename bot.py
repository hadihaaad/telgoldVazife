import requests
from pyrogram import Client, filters, idle

# ==========================================
# مقادیر خودت رو دقیقاً در ۴ خط زیر جایگزین کن:
# ==========================================
API_ID = 12345678  # آیدی خودت رو به صورت عدد اینجا بنویس (بدون کوتیشن)
API_HASH = "YOUR_API_HASH"  # ای‌پی‌آی هش خودت رو اینجا بین کوتیشن‌ها بذار
SESSION_STRING = "YOUR_SESSION_STRING"  # سشن استرینگ رو اینجا بین کوتیشن‌ها بذار
WEBHOOK_URL = "YOUR_N8N_WEBHOOK_URL"  # لینک وب‌هوک رو اینجا بین کوتیشن‌ها بذار
# ==========================================

TARGET_USERNAME = "abshode_abasnezhad"

app = Client("n8n_forwarder", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.chat(TARGET_USERNAME))
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
        response = requests.post(WEBHOOK_URL, json=data, timeout=10)
        print(f"✅ پیام {message.id} با موفقیت به n8n ارسال شد! Status: {response.status_code}")
    except Exception as e:
        print(f"❌ خطا در ارسال به n8n: {e}")

async def main():
    print("🚀 در حال روشن شدن ربات...")
    await app.start()
    
    print(f"🔄 در حال اتصال اختصاصی به کانال هدف (@{TARGET_USERNAME})...")
    try:
        await app.join_chat(TARGET_USERNAME)
    except:
        pass # اگر از قبل عضو بود خطا ندهد
    
    print("🔄 در حال کش عمومی برای جلوگیری از کرش بخاطر سایر کانال‌ها...")
    try:
        async for _ in app.get_dialogs(limit=500):
            pass
        print("✅ کش عمومی کامل شد.")
    except Exception as e:
        print(f"⚠️ خطای کش عمومی: {e}")

    print(f"🎧 ربات آماده است و فقط پیام‌های @{TARGET_USERNAME} را به n8n می‌فرستد...")
    await idle()
    await app.stop()

app.run(main())
