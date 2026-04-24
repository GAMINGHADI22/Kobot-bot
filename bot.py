import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import time

# ======================
# 🔐 CONFIG
# ======================
TOKEN = "8373105920:AAGvG57H3FTlocm6URgeEk9vAw2mp18qjw0"   # 👉 BotFather থেকে নেবে
CHANNEL_ID = "@bangladeshkobor"

ADMIN_ID = 7288385191       # 👉 তোমার Telegram ID (UserInfoBot থেকে নাও)

bot = telebot.TeleBot(TOKEN)

users = set()

# ======================
# 🔥 START
# ======================
@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.from_user.id)
    bot.reply_to(message, "🤖 Bot Active!\nAdmin post system ready.")

# ======================
# 🔐 ADMIN CHECK
# ======================
def is_admin(message):
    return message.from_user.id == ADMIN_ID

# ======================
# 📝 TEXT POST
# ======================
@bot.message_handler(content_types=['text'])
def text_handler(message):
    users.add(message.from_user.id)

    if is_admin(message):
        bot.send_message(CHANNEL_ID, message.text)
        bot.reply_to(message, "✅ Text posted to channel!")
    else:
        bot.reply_to(message, "❌ Only admin can post!")

# ======================
# 📸 PHOTO POST
# ======================
@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    if is_admin(message):
        file_id = message.photo[-1].file_id
        bot.send_photo(CHANNEL_ID, file_id, caption=message.caption or "")
        bot.reply_to(message, "📸 Photo posted!")
    else:
        bot.reply_to(message, "❌ Only admin can post!")

# ======================
# 🎥 VIDEO POST
# ======================
@bot.message_handler(content_types=['video'])
def video_handler(message):
    if is_admin(message):
        bot.send_video(CHANNEL_ID, message.video.file_id, caption=message.caption or "")
        bot.reply_to(message, "🎬 Video posted!")
    else:
        bot.reply_to(message, "❌ Only admin can post!")

# ======================
# 🔘 PANEL BUTTON
# ======================
@bot.message_handler(commands=['panel'])
def panel(message):
    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton("📢 Channel", url="https://t.me/" + CHANNEL_ID.replace("@",""))
    btn2 = InlineKeyboardButton("👥 Users", callback_data="users")

    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, "👇 Control Panel:", reply_markup=markup)

# ======================
# 🔘 BUTTON ACTION
# ======================
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "users":
        bot.answer_callback_query(call.id, f"👥 Total Users: {len(users)}")

# ======================
# ⏱ AUTO POST SYSTEM
# ======================
def auto_post():
    while True:
        try:
            bot.send_message(CHANNEL_ID, "🔥 Auto post active...")
            time.sleep(3600)  # 1 hour
        except:
            pass

threading.Thread(target=auto_post).start()

# ======================
# ▶️ RUN BOT
# ======================
print("🤖 Bot Running...")
bot.infinity_polling()
