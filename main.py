import os
import pickle
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# بارگذاری توکن از محیط
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# بارگذاری دیکشنری از فایل


def load_courses():
    with open('courses.pkl', 'rb') as f:
        return pickle.load(f)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello Tell Me What Course You Want')


def search_courses(keyword):
    courses = load_courses()
    results = {course: link for course,
               link in courses.items() if keyword.lower() in course.lower()}
    return results


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyword = update.message.text
    results = search_courses(keyword)
    if results:
        response = "\n\n".join(
            [f"**{course}**: [{link}]({link})" for course, link in results.items()])
        await update.message.reply_text(
            f'**Found the following courses for "{
                keyword}":** ˙✧˖°🎓 ༘⋆｡ ˚\n\n{response}',
            parse_mode='MarkdownV2'
        )
    else:
        await update.message.reply_text(f'No Course Was Found For "{keyword}".')


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    app.run_polling()


if __name__ == '__main__':
    main()
