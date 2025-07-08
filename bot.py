import os
import re
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "7284916721:AAE3nVJJPIKWgvQ59IIEpybBMEvJXM3pbHM")
DEVELOPER_ID = int(os.getenv("DEVELOPER_ID", "5755811287"))

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

PLATFORMS = {
    "youtube": r"(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+",
    "tiktok": r"(https?:\/\/)?(www\.)?tiktok\.com\/.+",
    "instagram": r"(https?:\/\/)?(www\.)?instagram\.com\/.+",
    "x": r"(https?:\/\/)?(www\.)?(twitter\.com|x\.com)\/.+",
    "snapchat": r"(https?:\/\/)?(www\.)?snapchat\.com\/.+",
}

def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📥 تنزيل فيديو", callback_data="download"),
        InlineKeyboardButton("🌐 اللغات", callback_data="languages"),
        InlineKeyboardButton("🛠️ المطور", url="https://t.me/xeps901"),
        InlineKeyboardButton("❓ المساعدة", callback_data="help"),
    )
    return kb

@dp.message_handler(commands=['start', 'help', 'about'])
async def cmd_start(message: types.Message):
    await message.answer("👋 أهلاً بك في بوت تحميل الفيديوهات بجودة عالية!\n\nاختر منصة أو أرسل الرابط مباشرة.", reply_markup=main_menu())

@dp.callback_query_handler(lambda c: c.data == "download")
async def show_platforms(call: types.CallbackQuery):
    platforms_kb = InlineKeyboardMarkup(row_width=3)
    for name, emoji in [("يوتيوب", "📺"), ("تيك توك", "🎵"), ("انستجرام", "📸"), ("X", "🦅"), ("سناب شات", "👻")]:
        code = name.lower().replace(" ", "")
        platforms_kb.insert(InlineKeyboardButton(f"{emoji} {name}", callback_data=f"platform_{code}"))
    await call.message.edit_text("اختر المنصة:", reply_markup=platforms_kb)

@dp.message_handler(lambda message: True, content_types=types.ContentType.TEXT)
async def handle_url(message: types.Message):
    url = message.text.strip()
    for platform, regex in PLATFORMS.items():
        if re.match(regex, url):
            await message.reply(f"✅ تم التعرف على المنصة: <b>{platform.capitalize()}</b>\n\n(هنا يتم تنفيذ التحميل الفعلي...)", reply_markup=main_menu())
            # هنا تضع كود التحميل الفعلي لاحقاً
            return
    await message.reply("❌ الرابط غير مدعوم أو غير صحيح!\n\nيرجى إرسال رابط من إحدى المنصات المدعومة.", reply_markup=main_menu())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
