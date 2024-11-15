#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from telegram import Update
from telegram.ext import (
    Application,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

import functions
from params import TELEGRAM_TOKEN, ChatState


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log")
    ])
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    DEFAULT_COMMANDS = [
                CommandHandler("start", functions.start),
                CommandHandler("help", functions.start),
                CommandHandler("bot_version", functions.bot_version),
                CommandHandler("art_version", functions.art_version),
                CommandHandler("restart", functions.restart),
                CommandHandler("aprint", functions.goto_aprint),
                CommandHandler("tprint", functions.goto_tprint),
                CommandHandler("showall_arts", functions.showall_arts),
                CommandHandler("showall_fonts", functions.showall_fonts),
                CommandHandler("showall_decors", functions.showall_decors),
                CommandHandler("space", functions.set_space),
                CommandHandler("font", functions.set_font),
                CommandHandler("decoration", functions.set_decoration),
                CommandHandler("status", functions.get_status),
    ]
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", functions.start)],
        states={
            ChatState.START: DEFAULT_COMMANDS,
            ChatState.IDLE: DEFAULT_COMMANDS,
            ChatState.APRINT: [
                CommandHandler("back", functions.back),
                *DEFAULT_COMMANDS,
                MessageHandler(filters.TEXT, functions.aprint),
            ],
            ChatState.TPRINT: [
                CommandHandler("back", functions.back),
                *DEFAULT_COMMANDS,
                MessageHandler(filters.TEXT, functions.tprint),
            ],
        },
        fallbacks=[CommandHandler("back", functions.back)],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
