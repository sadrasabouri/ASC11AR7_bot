# -*- coding: utf-8 -*-
import os
import enum
import art

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
class ChatState(enum.Enum):
    """States of the conversation."""
    START = 0
    IDLE = 1
    APRINT = 2
    TPRINT = 3

HELP_MESSAGE = """
Welcome to the ASCII Art Bot! 🎨
"""
