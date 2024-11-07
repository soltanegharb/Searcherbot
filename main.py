import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from courses import courses

# تعریف تابع جستجو


def search_courses(courses, keyword):
    keyword = keyword.lower()
    results = {key: value for key, value in courses.items()
               if keyword in key.lower()}
    return results


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('سلام! لطفاً یک کلمه کلیدی بفرستید تا دوره‌های مربوطه را جستجو کنم.')


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyword = update.message.text
    results = search_courses(courses, keyword)
    if results:
        response = "\n".join([link for course, link in results.items()])
    else:
        await update.message.reply_text(f'هیچ دوره‌ای برای "{keyword}" پیدا نشد.')


def main():
    # بارگذاری توکن بات از متغیرهای محیطی
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

    print("بات در حال اجراست...")
    app.run_polling()


if __name__ == "__main__":
    main()
