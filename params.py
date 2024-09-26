# -*- coding: utf-8 -*-
import os
import enum
import art

VERSION = "0.1"

TELEGRAM_MESSAGE_MAX_LENGTH = 4096
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
class ChatState(enum.Enum):
    """States of the conversation."""
    START = 0
    IDLE = 1
    APRINT = 2
    TPRINT = 3

BOT_VERSION_MESSAGE = "Bot version: {0}"
ART_VERSION_MESSAGE = "Art Library version: {0}"
HELP_MESSAGE = """
Welcome to the ASCII Art Bot! 🎨
Send me a command to get started:
/aprint - Print ASCII art.
/tprint - Print text with a font.
/showall_arts - Show all the available ASCII arts.
/showall_fonts - Show all the available fonts.
/space <VALUE>- Set the space character.
/font <FONT_NAME> - Set the font.
/decoration <DECORATION_NAME> - Set the decoration.
/help - Show this message.
/bot_version - Show the bot version.
/art_version - Show the art library version.
/restart - Restart the conversation.

You can always go back to the main menu by sending /back.

Enjoy! 🎉
"""
BACK_MESSAGE = "Going back to the main menu."
GOTO_APRINT_MESSAGE = "Send me a art name and I will print that ASCII art for you."
GOTO_TPRINT_MESSAGE = "Send me a text and I will print it with a font."

DECORATION_ERROR_NO_DECORATION_MESSAGE = "No decoration found with that name. Use /decoration <DECORATION_NAME> to set the decoration. For example: /decoration ==."
SPACE_ERROR_NO_SPACE_MESSAGE = "No space value found. Use /space <VALUE> to set the space between characters. For example: /space 2."
FONT_ERROR_NO_FONT_MESSAGE = "No font found with that name. Use /font <FONT_NAME> to set the font. For example: /font random."

APRINT_ERROR_NO_ART_FOUND_MESSAGE = "No ASCII art found with the name {0}. Run /showall_arts to see all the available ASCII arts."

ALL_ARTS = []
ALL_ART = ""
for art_name in art.ART_NAMES:
    if len(ALL_ART) + len(f"{art_name}: {art.art(art_name)}\n") < TELEGRAM_MESSAGE_MAX_LENGTH:
        ALL_ART += f"{art_name}: {art.art(art_name)}\n"
    else:
        ALL_ARTS.append(ALL_ART)
        ALL_ART = f"{art_name}: {art.art(art_name)}\n"
ALL_ARTS.append(ALL_ART)
