import os
import pickle
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load the bot token from the environment variable
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Load the dictionary from the file


def load_courses():
    try:
        with open('courses.pkl', 'rb') as f:
            courses = pickle.load(f)
            print(f"Courses loaded: {courses}")
            return courses
    except Exception as e:
        print(f"Error loading courses: {e}")
        return {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Please send me a keyword to search for courses.')


def search_courses(keyword):
    courses = load_courses()
    keyword = keyword.lower()
    print(f"Searching for keyword: {keyword}")
    results = {}
    # Iterate through each key in the dictionary
    for course, link in courses.items():
        temp = str(course).lower()
        if keyword in temp:
            results[course] = link
    print(f"Search results: {results}")
    return results


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyword = update.message.text
    results = search_courses(keyword)
    if results:
        response = "\n\n".join(
            [f"{course}: [{link}]({link})" for course, link in results.items()])
        await update.message.reply_text(
            f'Found the following courses for "{
                keyword}": ˙✧˖°🎓 ༘⋆｡ ˚\n\n{response}',
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
