import os
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, InlineQueryHandler, filters, ContextTypes
from uuid import uuid4
from courses import courses

# Define the search function


def search_courses(dictionary, keyword):
    keyword = keyword.lower()
    results = {key: value for key, value in dictionary.items()
               if keyword in key.lower()}
    return results

# Start command handler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Please send me a keyword to search for courses.')

# Inline query handler


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query
    if not query:
        return

    results = search_courses(courses, query)
    articles = [InlineQueryResultArticle(
        id=str(uuid4()),
        title=course,
        input_message_content=InputTextMessageContent(f"{course}: {link}")
    ) for course, link in results.items()]

    await update.inline_query.answer(articles, cache_time=1)

# Command to trigger inline search


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyword = ' '.join(context.args)
    results = search_courses(courses, keyword)
    if results:
        response = "\n\n".join(
            [f"{course}: {link}" for course, link in results.items()])
        await update.message.reply_text(
            f'Found the following courses for "{keyword}":\n\n{response}'
        )
    else:
        await update.message.reply_text(f'No courses found for "{keyword}".')


def main():
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    app.add_handler(InlineQueryHandler(inline_query))

    print("Starting the bot...")
    app.run_polling()


if __name__ == "__main__":
    main()
