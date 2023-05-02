from aiogram import Bot, Dispatcher, executor as exc
from aiogram.types import CallbackQuery, Message
import keyboards
import answers
import config

bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def cmd_start(message: Message):
    await message.answer(answers.start, reply_markup=keyboards.main_menu)

exc.start_polling(dp, skip_updates=True)