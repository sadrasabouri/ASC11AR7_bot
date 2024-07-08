# -*- coding: utf-8 -*-
# pylint: disable=unused-argument

import logging
from telegram import Update
from telegram.ext import ContextTypes

from params import ChatState, HELP_MESSAGE


logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and send user a help message."""

    await update.message.reply_text(HELP_MESSAGE)
    logger.info(f"{update.effective_user} started the conversation.")

    return ChatState.IDLE
