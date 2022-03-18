import logging
import os
import traceback
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils import executor

from aiogram_datepicker import Datepicker

storage = MemoryStorage()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ['API_TOKEN'])
dp = Dispatcher(bot, storage=storage, run_tasks_by_default=True)


class Calendar(StatesGroup):
    init = State()


@dp.errors_handler()
async def errors_handler(update, exception):
    try:
        raise exception
    except:
        exception_traceback = traceback.format_exc()

    logging.exception(f'Update: {update} \n{exception_traceback}')


@dp.message_handler(state='*')
async def _main(message: Message, state):
    await Calendar.init.set()

    datepicker = Datepicker(state, datetime.now())

    markup = await datepicker.start_calendar()
    await message.answer('Select a date: ', reply_markup=markup)


@dp.callback_query_handler(Datepicker.datepicker_callback.filter(), state=Calendar.init)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state):
    print(callback_query.message.reply_markup.inline_keyboard)

    datepicker = Datepicker(state)

    date = await datepicker.process_selection(callback_query, callback_data)
    if date:
        await callback_query.message.answer(date.strftime('%d/%m/%Y'))

    await callback_query.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
