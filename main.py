# main.py
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from courses import courses

# Define the search function


def search_courses(dictionary, keyword):
    keyword = keyword.lower()
    results = {key: value for key, value in dictionary.items()
               if keyword in key.lower()}
    return results


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Please send me a keyword to search for courses.')


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyword = update.message.text
    results = search_courses(courses, keyword)
    if results:
        response = "\n".join(
            [f"**{course}**: [{link}]({link})" for course, link in results])
        await update.message.reply_text(
            f'**Found the following courses for "{keyword}":**\n{response}',
            parse_mode='MarkdownV2'
        )
    else:
        await update.message.reply_text(f'No courses found for "{keyword}".')


def main():
    # Load your bot token from environment variables
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

    print("Starting the bot...")
    app.run_polling()


if __name__ == "__main__":
    main()
