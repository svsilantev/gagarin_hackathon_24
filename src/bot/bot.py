import os

from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, CallbackQueryHandler

from bot.handlers import commands, conversations, callbacks


token = os.getenv('BOT_TOKEN')

bot = ApplicationBuilder() \
    .token(token) \
    .build() \

bot.add_handler(commands.start_command)
# bot.add_handler(commands.add_page_command)
# bot.add_handler(CallbackQueryHandler(callbacks.add_fio, 'add_page'))
bot.add_handler(conversations.add_page_conversation)