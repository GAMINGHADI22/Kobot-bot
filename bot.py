import feedparser
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = "8373105920:AAGvG57H3FTlocm6URgeEk9vAw2mp18qjw0"
CHANNEL_ID = "@bangladeshkobor"

# RSS feeds
FEEDS = {
    "all": [
        "https://www.prothomalo.com/feed",
        "https://bdnews24.com/?widgetName=rssfeed&widgetId=1151&getXmlFeed=true"
    ],
    "sports": [
        "https://www.prothomalo.com/sports/feed"
    ],
    "tech": [
        "https://bdnews24.com/technology?widgetName=rssfeed&widgetId=1151&getXmlFeed=true"
    ]
}

subscribers = set()

# 🔹 Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📰 All News", callback_data="all")],
        [InlineKeyboardButton("⚽ Sports", callback_data="sports")],
        [InlineKeyboardButton("💻 Tech", callback_data="tech")],
        [InlineKeyboardButton("🔔 Subscribe", callback_data="sub")],
        [InlineKeyboardButton("❌ Unsubscribe", callback_data="unsub")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("🇧🇩 Bangladesh News Bot\nChoose option:", reply_markup=reply_markup)

# 🔹 Fetch news
def get_news(category):
    urls = FEEDS.get(category, [])
    news_list = []

    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
            news_list.append(f"👉 {entry.title}\n{entry.link}")

    return "\n\n".join(news_list[:10])

# 🔹 Button click
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data in ["all", "sports", "tech"]:
        news = get_news(data)
        await query.edit_message_text(f"📰 {data.upper()} NEWS:\n\n{news}")

    elif data == "sub":
        subscribers.add(query.from_user.id)
        await query.edit_message_text("✅ Subscribed! You will get auto news.")

    elif data == "unsub":
        subscribers.discard(query.from_user.id)
        await query.edit_message_text("❌ Unsubscribed.")

# 🔹 Auto news sender (User + Channel)
async def auto_news(app):
    while True:
        news = get_news("all")

        # send to users
        for user_id in subscribers:
            try:
                await app.bot.send_message(chat_id=user_id, text=f"🔴 Auto News:\n\n{news}")
            except:
                pass

        # send to channel
        try:
            await app.bot.send_message(chat_id=CHANNEL_ID, text=f"📰 Channel Update:\n\n{news}")
        except:
            print("Channel send failed")

        await asyncio.sleep(3600)

# 🔹 Main
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.job_queue.run_once(lambda *_: asyncio.create_task(auto_news(app)), 1)

    print("Bot running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
