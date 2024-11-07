import os
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load the bot token from the environment variable
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Create a SQLite database connection


def create_connection(db_file):
    return sqlite3.connect(db_file)

# Search courses in the database


def search_courses(conn, keyword):
    keyword = f"%{keyword.lower()}%"
    sql_search = """SELECT name, link FROM courses WHERE LOWER(name) LIKE ?"""
    cursor = conn.cursor()
    cursor.execute(sql_search, (keyword,))
    return cursor.fetchall()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Please send me a keyword to search for courses.')


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyword = update.message.text
    conn = create_connection("courses.db")
    results = search_courses(conn, keyword)
    conn.close()
    if results:
        response = "\n".join(
            [f"**{name}**: [{link}]({link})" for name, link in results])
        await update.message.reply_text(
            f'**Found the following courses for "{keyword}":**\n{response}',
            parse_mode='MarkdownV2'
        )
    else:
        await update.message.reply_text(f'No courses found for "{keyword}".')


def main():
    print("Starting the bot")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    app.run_polling()


if __name__ == '__main__':
    main()
