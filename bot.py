import telebot

TOKEN = "8373105920:AAF5VbDpWBJqQD6pPXOO3efDTwctwkbfGi8"
CHANNEL_ID = "@bangladeshkobor"
ADMIN_ID = 7288385191

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 Bot working!")

@bot.message_handler(commands=['post'])
def post(message):
    if message.from_user.id == ADMIN_ID:
        text = message.text.replace("/post", "").strip()
        bot.send_message(CHANNEL_ID, text)
        bot.reply_to(message, "✅ Posted!")
    else:
        bot.reply_to(message, "❌ Not allowed!")

print("Bot running...")
bot.infinity_polling()
