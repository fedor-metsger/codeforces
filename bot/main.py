
import logging
import os
from dotenv import load_dotenv

from telegram import (
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)

from config.settings import BASE_DIR
from bot.db import get_topics, get_problems_by_tag


load_dotenv(BASE_DIR / '.env')

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

TOPIC, DIFFICULTY = range(2)

topics = {}
selections = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    msg = "Добрый день. Я бот, который помогает подбирать задания на сайте Codeforces.com.\n" \
        "Если хотите прекратить разговор, напишите /cancel.\n\n" \
        "В ином случае выберите тему задания:\n"
    global topics
    topics = get_topics()
    keyboard = []
    for k in topics:
        msg = msg + f'{k} - {topics[k]}\n'
        if not keyboard or len(keyboard[-1]) % 6 == 0:
            keyboard.append([])
        keyboard[-1].append(InlineKeyboardButton(k, callback_data=k))

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(msg, reply_markup=reply_markup)

    return TOPIC

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global selections
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f'Выбрана тема: "{topics[query.data]}"\n'
                                       "Отлично. Теперь сообщите желаемую сложность задания\n"
                                       "или пошлите /cancel для завершения разговора:"
                                  )
    selected_topic = query.data
    user = update.callback_query.from_user
    user_id = update.callback_query.from_user.id
    selections[user_id] = {"topic": selected_topic, "difficulty": None}
    logger.info("Topic of %s: %s", user.first_name, selected_topic)

    return DIFFICULTY

def get_ten_nearest(probs: list, diff: int):
    sorted_probs = sorted(probs, key=lambda d: abs(d["difficulty"] - diff))
    return sorted_probs[0:10]

async def difficulty(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Сложность для %s: %s", user.first_name, update.message.text)
    user_topic = selections[user.id]["topic"]
    problems = get_problems_by_tag(int(user_topic))
    sorted10 = get_ten_nearest(problems, int(update.message.text))
    msg = "Замечательно! Высылаю вам варианты заданий:"
    for p in sorted10:
        msg = msg + f'\n{p["number"]} ({p["difficulty"]}) - "{p["name"]}"'
    await update.message.reply_text(msg)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "До свидания! Заглядывайте ещё.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token(os.getenv("TG_BOT_TOKEN")).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            # TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, topic)],
            TOPIC: [CallbackQueryHandler(button)],
            DIFFICULTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, difficulty)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    # application.add_handler(CallbackQueryHandler(button))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()