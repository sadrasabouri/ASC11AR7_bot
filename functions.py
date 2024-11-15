# -*- coding: utf-8 -*-
# pylint: disable=unused-argument

import logging
from telegram import Update
from telegram.ext import ContextTypes
import art
import time

from params import DEFAULT_VALUE_REPR
from params import VERSION
from params import ART_VERSION_MESSAGE, BOT_VERSION_MESSAGE
from params import ChatState
from params import HELP_MESSAGE, BACK_MESSAGE
from params import GOTO_APRINT_MESSAGE, GOTO_TPRINT_MESSAGE
from params import DECORATION_ERROR_NO_DECORATION_MESSAGE, SPACE_ERROR_NO_SPACE_MESSAGE, FONT_ERROR_NO_FONT_MESSAGE
from params import APRINT_ERROR_NO_ART_FOUND_MESSAGE

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


async def showall_arts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a link to the ASCII art site."""
    await update.message.reply_text(
        "Check out all available arts here: [ASCII Art List](https://www.ascii-art.site/ArtList.html)",
        parse_mode="Markdown"
    )


async def showall_fonts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Shows all the available fonts."""
    await update.message.reply_text(
        "Check out all available fonts here: [Font List](https://www.ascii-art.site/FontList.html)",
        parse_mode="Markdown"
    )


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


async def get_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Shows the current settings."""
    space = context.user_data.get("space", DEFAULT_VALUE_REPR)
    font = context.user_data.get("font", DEFAULT_VALUE_REPR)
    decoration = context.user_data.get("decoration", DEFAULT_VALUE_REPR)
    text = context.user_data.get("text", DEFAULT_VALUE_REPR)
    await update.message.reply_text(f"Space: {space}\nFont: {font}\nDecoration: {decoration}\nText: {text}")
    logger.info(f"{update.effective_user} requested the current settings.")


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
