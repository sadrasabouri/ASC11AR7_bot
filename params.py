# -*- coding: utf-8 -*-
import os
import enum
import art


TELEGRAM_MESSAGE_MAX_LENGTH = 4096
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
class ChatState(enum.Enum):
    """States of the conversation."""
    START = 0
    IDLE = 1
    APRINT = 2
    TPRINT = 3

HELP_MESSAGE = """
Welcome to the ASCII Art Bot! 🎨
Send me a command to get started:
/aprint - Print ASCII art.
/tprint - Print text with a font.
/showall_arts - Show all the available ASCII arts.
/showall_fonts - Show all the available fonts.
/space [VALUE]- Set the space character.
/font [FONT_NAME] - Set the font.
/decoration [DECORATION_NAME] - Set the decoration.

You can always go back to the main menu by sending /back.

Enjoy! 🎉
"""
BACK_MESSAGE = "Going back to the main menu."
GOTO_APRINT_MESSAGE = "Send me a art name and I will print that ASCII art for you."
GOTO_TPRINT_MESSAGE = "Send me a text and I will print it with a font."
