from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config

main_menu = InlineKeyboardMarkup()
main_menu.add(InlineKeyboardButton(text="Click", web_app=WebAppInfo(url=config.SITE_URL)))