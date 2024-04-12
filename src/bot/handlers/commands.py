from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CommandHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id: int = update.effective_chat.id

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            'Приветствуем Вас в чат-боте проекта '
            '"Код памяти". Чат-бот поможет Вам оформить '
            'биографию или эпитафию для страницы памяти.\n\n'
            'Чат-бот разработан в рамках "Гагарин Хакатона" '
            'и является концепцией.'
        )
    )
    buttons = [
        [
            InlineKeyboardButton(
                text='Эпитафией',
                callback_data='create_epitach'
            )
        ],
        [
            InlineKeyboardButton(
                text='Биографией',
                callback_data='create_biography'
            )
        ]

    ]
    reply = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(
        chat_id=chat_id,
        text='С чем Вам помочь?',
        reply_markup=reply
    )


start_command = CommandHandler('start', start)

