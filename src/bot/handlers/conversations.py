from typing import Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes


WORK, MEMORIES, ACHIEVEMENTS, HOBBY, CHARACTER, QUOTES, CHECK_OBJECTIONS, OBJECTIONS, DONE, EXTRA = range(10)


async def create_epitach(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data['type'] = 'epitach'
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Кем работал(а) и чем занимался(лась) он/она?',
    )
    return WORK


async def create_biography(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data['type'] = 'biography'
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Кем работал(а) и чем занимался(лась) он/она?',
    )
    return WORK


async def memories(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data['work'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            'Есть ли какие-то особые моменты или '
            'воспоминания, которые вы ассоциируете '
            'с этим человеком?'
        ),
    )
    return MEMORIES


async def achievements(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data['memories'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            'Какие его/её достижения вы считаете '
            'наиболее значимыми?'
        ),
    )
    return ACHIEVEMENTS


async def hobby(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data['achievements'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            'Какие увлечения или хобби были у него/неё?'
        ),
    )
    return HOBBY


async def character(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data['hobby'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            'Какие черты характера вы могли бы в нём/ней отметить?'
        ),
    )
    return CHARACTER


async def quotes(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data['character'] = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            'Есть ли любимые цитаты или выражения, '
            'которые он/она часто говорил(а)?'
        ),
    )
    return QUOTES


async def check_objections(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data['quotes'] = update.message.text
    result = 'Итоговый текст...' 
    context.user_data['result'] = result
    buttons = [
        [
            InlineKeyboardButton(
                text='Все супер',
                callback_data='done'
            )
        ],
        [
            InlineKeyboardButton(
                text='Есть замечания',
                callback_data='objections'
            )
        ]

    ]
    reply = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            f'Вот что у меня получилось:\n{result}'
        ),
        reply_markup=reply
    )
    return CHECK_OBJECTIONS


async def update_result(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            'Напишите свои замечания, пожалуйста.'
        ),
    )
    return OBJECTIONS


async def objections(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    objections = update.message.text
    result = 'Итоговый текст с замечаниями...' 
    context.user_data['result'] = result
    buttons = [
        [
            InlineKeyboardButton(
                text='Все супер',
                callback_data='done'
            )
        ],
        [
            InlineKeyboardButton(
                text='Есть замечания',
                callback_data='objections'
            )
        ]

    ]
    reply = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            f'Вот что у меня получилось:\n{result}'
        ),
        reply_markup=reply
    )
    return CHECK_OBJECTIONS


async def done(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    result = context.user_data['result']
    _type = context.user_data['type']
    if context.user_data['type'] == 'epitach':
        extra = 'Хотите также создать биографию?'
    else: 
        extra = 'Хотите также создать эпитафию?'
    buttons = [
        [
            InlineKeyboardButton(
                text=extra,
                callback_data='extra'
            )
        ],
        [
            InlineKeyboardButton(
                text='Начать заново',
                callback_data='restart'
            )
        ]

    ]
    reply = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            f'Итоговый результат:\n{result}'
        ),
        reply_markup=reply
    )
    return EXTRA


async def check_extra(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    result = 'Итоговый текст...' 
    context.user_data['result'] = result
    context.user_data['type'] = (
        'epitach' if context.user_data['type'] == 'biography'
        else 'biography'
    )
    buttons = [
        [
            InlineKeyboardButton(
                text='Все супер',
                callback_data='done'
            )
        ],
        [
            InlineKeyboardButton(
                text='Есть замечания',
                callback_data='objections'
            )
        ]

    ]
    reply = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            f'Вот что у меня получилось:\n{result}'
        ),
        reply_markup=reply
    )
    return CHECK_OBJECTIONS


async def restart(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> int:
    # context.user_data = {}
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
        chat_id=update.effective_chat.id,
        text='С чем Вам помочь?',
        reply_markup=reply
    )

    return ConversationHandler.END

    

add_page_conversation = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=create_epitach,
            pattern='create_epitach'
        ),
        CallbackQueryHandler(
            callback=create_biography,
            pattern='create_biography'
        ),
    ],
    states={
        WORK: [MessageHandler(filters.TEXT & ~filters.COMMAND, callback=memories)],
        MEMORIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, callback=achievements)],
        ACHIEVEMENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, callback=hobby)],
        HOBBY: [MessageHandler(filters.TEXT & ~filters.COMMAND, callback=character)],
        CHARACTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, callback=quotes)],
        QUOTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, callback=check_objections)],
        CHECK_OBJECTIONS: [
            CallbackQueryHandler(callback=update_result, pattern='objections'),
            CallbackQueryHandler(callback=done, pattern='done')
        ],
        OBJECTIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, callback=objections)],
        EXTRA: [
            CallbackQueryHandler(callback=check_extra, pattern='extra'),
            CallbackQueryHandler(callback=restart, pattern='restart')
        ]
    },
    fallbacks=[],
)