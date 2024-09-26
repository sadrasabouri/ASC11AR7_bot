# -*- coding: utf-8 -*-
# pylint: disable=unused-argument

import logging
from telegram import Update
from telegram.ext import ContextTypes
import art
import time

from params import VERSION
from params import ART_VERSION_MESSAGE, BOT_VERSION_MESSAGE
from params import ChatState
from params import TELEGRAM_MESSAGE_MAX_LENGTH
from params import HELP_MESSAGE, BACK_MESSAGE
from params import GOTO_APRINT_MESSAGE, GOTO_TPRINT_MESSAGE
from params import DECORATION_ERROR_NO_DECORATION_MESSAGE, SPACE_ERROR_NO_SPACE_MESSAGE, FONT_ERROR_NO_FONT_MESSAGE
from params import APRINT_ERROR_NO_ART_FOUND_MESSAGE
from params import ALL_ARTS

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


async def bot_version(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Returns the bot version."""
    await update.message.reply_text(BOT_VERSION_MESSAGE.format(VERSION))
    logger.info(f"{update.effective_user} requested bot version.")


async def art_version(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Returns the art library version."""
    await update.message.reply_text(ART_VERSION_MESSAGE.format(art.__version__))
    logger.info(f"{update.effective_user} requested art library version.")


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns to the main menu."""
    await update.message.reply_text(BACK_MESSAGE)
    await update.message.reply_text(HELP_MESSAGE)
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
    for all_art in ALL_ARTS:
        await update.message.reply_text(all_art)
    logger.info(f"{update.effective_user} requested showing all the ASCII arts.")


async def showall_fonts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Shows all the available fonts."""
    #TODO: Use the current text instead of 'test'
    text = context.user_data.get("text", "test")
    ALL_FONT = ""
    for font in art.FONT_NAMES:
        if len(ALL_FONT) + len(f"{font}: {art.text2art(text, font)}\n") < TELEGRAM_MESSAGE_MAX_LENGTH:
            ALL_FONT += f"{font}: {art.text2art(text, font)}\n"
        else:
            await update.message.reply_text(ALL_FONT)
            ALL_FONT = f"{font}: {art.text2art(text, font)}\n"
            time.sleep(1)
    logger.info(f"{update.effective_user} requested showing all the fonts.")


async def set_space(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sets the space between the characters in tprint and aprint."""
    if len(context.args) == 0:
        await update.message.reply_text(SPACE_ERROR_NO_SPACE_MESSAGE)
    else:
        space = int(context.args[0])
        context.user_data["space"] = space
        await update.message.reply_text(f"Space between character set to {space}.")
        logger.info(f"{update.effective_user} set the space to {space}.")


async def set_font(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sets the font for tprint."""
    if len(context.args) == 0:
        await update.message.reply_text(FONT_ERROR_NO_FONT_MESSAGE)
    else:
        font = context.args[0]
        context.user_data["font"] = font
        await update.message.reply_text(f"Font set to {font}.")
        logger.info(f"{update.effective_user} set the font to {font}.")


async def set_decoration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sets the decoration for tprint."""
    if len(context.args) == 0:
        await update.message.reply_text(DECORATION_ERROR_NO_DECORATION_MESSAGE)
    else:
        decoration = context.args[0]
        context.user_data["decoration"] = decoration
        await update.message.reply_text(f"Decoration set to {decoration}.")
        logger.info(f"{update.effective_user} set the decoration to {decoration}.")


async def aprint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prints the ASCII art."""
    art_name = update.message.text
    parameters = {}
    for x in art.art.__code__.co_varnames:
        if x in context.user_data:
            parameters[x] = context.user_data[x]
    if art_name not in art.ART_NAMES:
        await update.message.reply_text(APRINT_ERROR_NO_ART_FOUND_MESSAGE.format(art_name))
    else:
        await update.message.reply_text(art.art(art_name, **parameters))
        logger.info(f"{update.effective_user} printed ASCII art.")


async def tprint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """"Prints the text with the given font."""
    text = update.message.text
    context.user_data["text"] = text
    parameters = {}
    for x in art.text2art.__code__.co_varnames:
        if x in context.user_data:
            parameters[x] = context.user_data[x]
    await update.message.reply_text(art.text2art(**parameters))
    logger.info(f"{update.effective_user} printed text.")
