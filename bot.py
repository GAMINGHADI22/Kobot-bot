import telebot
import os

TOKEN = os.getenv("8373105920:AAF5VbDpWBJqQD6pPXOO3efDTwctwkbfGi8")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(TOKEN)

users = set()

@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.from_user.id)
    bot.reply_to(message, "🤖 Bot Active!")

@bot.message_handler(commands=['post'])
def post(message):
    if message.from_user.id == ADMIN_ID:
        text = message.text.replace("/post", "").strip()
        bot.send_message(CHANNEL_ID, text)
        bot.reply_to(message, "✅ Posted!")
    else:
        bot.reply_to(message, "❌ Not allowed!")

print("Bot Running...")
bot.infinity_polling()
