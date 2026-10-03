import requests
from pyrogram import Client, filters, idle

# ==========================================
# مقادیر خود را دقیقاً در متغیرهای زیر جایگزین کنید:
# ==========================================
API_ID = 12345678  # آیدی خود را اینجا به صورت عدد (بدون کوتیشن) وارد کنید
API_HASH = "YOUR_API_HASH"  # ای‌پی‌آی هش خود را بین کوتیشن‌ها بگذارید
SESSION_STRING = "YOUR_SESSION_STRING"  # سشن استرینگ طولانی خود را بین کوتیشن‌ها بگذارید
WEBHOOK_URL = "YOUR_N8N_WEBHOOK_URL"  # لینک کامل وب‌هوک n8n را بین کوتیشن‌ها بگذارید
# ==========================================

TARGET_USERNAME = "abshode_abasnezhad"

app = Client("n8n_forwarder", session_string=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# فیلتر فقط برای کانال عباس نژاد
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
        # ارسال پیام به وب‌هوک n8n
        response = requests.post(WEBHOOK_URL, json=data, timeout=10)
        print(f"✅ پیام {message.id} با موفقیت به n8n ارسال شد! Status: {response.status_code}")
    except Exception as e:
        print(f"❌ خطا در ارسال به n8n: {e}")

async def main():
    print("🚀 در حال روشن شدن...")
    await app.start()
    
    print(f"🔄 در حال اتصال اختصاصی به کانال هدف (@{TARGET_USERNAME})...")
    try:
        # اگر عضو نباشید، عضو می‌شود و آیدی را شناسایی می‌کند
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
