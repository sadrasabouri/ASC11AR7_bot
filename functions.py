# -*- coding: utf-8 -*-
# pylint: disable=unused-argument

import logging
from telegram import Update
from telegram.ext import ContextTypes
from art import art, text2art
from art import ART_NAMES, FONT_NAMES

from params import ChatState
from params import TELEGRAM_MESSAGE_MAX_LENGTH
from params import HELP_MESSAGE, BACK_MESSAGE
from params import GOTO_APRINT_MESSAGE, GOTO_TPRINT_MESSAGE

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and send user a help message."""
    await update.message.reply_text(HELP_MESSAGE)
    logger.info(f"{update.effective_user} started the conversation.")

    return ChatState.IDLE


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Restarts the conversation."""
    context.user_data["space"] = None
    context.user_data["font"] = None
    context.user_data["decoration"] = None
    await update.message.reply_text(HELP_MESSAGE)
    logger.info(f"{update.effective_user} restarted the conversation.")

    return ChatState.IDLE


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns to the main menu."""
    await update.message.reply_text(BACK_MESSAGE)
    logger.info(f"{update.effective_user} returned to the main menu.")

    return ChatState.IDLE


async def goto_aprint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Goes to the ASCII art print state."""
    await update.message.reply_text(GOTO_APRINT_MESSAGE)
    logger.info(f"{update.effective_user} entered the ASCII art print state.")

    return ChatState.APRINT


async def goto_tprint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Goes to the text print state."""
    await update.message.reply_text(GOTO_TPRINT_MESSAGE)
    logger.info(f"{update.effective_user} entered the text print state.")

    return ChatState.TPRINT


async def showall_arts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Shows all the available ASCII arts."""
    #TODO: Use given parameters
    result = "\n".join([f"{art_name}: {art(art_name)}" for art_name in ART_NAMES])
    #TODO: Fix the truncation problem
    for i in range(0, len(result), TELEGRAM_MESSAGE_MAX_LENGTH):
        await update.message.reply_text(result[i:i+TELEGRAM_MESSAGE_MAX_LENGTH])
    logger.info(f"{update.effective_user} requested showing all the ASCII arts.")

    return ChatState.IDLE


async def showall_fonts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Shows all the available fonts."""
    #TODO: Use the current text instead of 'test'
    #TODO: Use given parameters
    result = "\n".join([f"{font}: {text2art('test', font)}" for font in FONT_NAMES])
    #TODO: Fix the truncation problem
    for i in range(0, len(result), TELEGRAM_MESSAGE_MAX_LENGTH):
        await update.message.reply_text(result[i:i+TELEGRAM_MESSAGE_MAX_LENGTH])
    logger.info(f"{update.effective_user} requested showing all the fonts.")

    return ChatState.IDLE


async def set_space(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sets the space between the characters in tprint and aprint."""
    space = context.args[0]
    #TODO: validation
    context.user_data["space"] = space
    await update.message.reply_text(f"Space between character set to {space}.")
    logger.info(f"{update.effective_user} set the space to {space}.")

    return ChatState.IDLE


async def set_font(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sets the font for tprint."""
    font = context.args[0]
    #TODO: validation
    context.user_data["font"] = font
    await update.message.reply_text(f"Font set to {font}.")
    logger.info(f"{update.effective_user} set the font to {font}.")

    return ChatState.IDLE


async def set_decoration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sets the decoration for tprint."""
    decoration = context.args[0]
    #TODO: validation
    context.user_data["decoration"] = decoration
    await update.message.reply_text(f"Decoration set to {decoration}.")
    logger.info(f"{update.effective_user} set the decoration to {decoration}.")
    return ChatState.IDLE


async def aprint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prints the ASCII art."""
    art_name = update.message.text
    #TODO: Save text in user_data
    await update.message.reply_text(art(art_name, **context.user_data))
    logger.info(f"{update.effective_user} printed ASCII art.")

    return ChatState.APRINT


async def tprint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """"Prints the text with the given font."""
    text = update.message.text
    #TODO: Save text in user_data
    await update.message.reply_text(text2art(text, **context.user_data))
    logger.info(f"{update.effective_user} printed text.")

    return ChatState.TPRINT
