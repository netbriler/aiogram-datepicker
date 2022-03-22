import logging
import os
from datetime import datetime, date

from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardButton
from aiogram.types import Message, CallbackQuery
from aiogram.utils import executor

from aiogram_datepicker import Datepicker, DatepickerSettings, DatepickerCustomAction

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ['API_TOKEN'])
dp = Dispatcher(bot, run_tasks_by_default=True)


def _get_datepicker_settings():
    class TodayAction(DatepickerCustomAction):
        action: str = 'today'
        label: str = 'Today'

        def get_action(self, view: str, year: int, month: int, day: int) -> InlineKeyboardButton:
            return InlineKeyboardButton(self.label,
                                        callback_data=self._get_callback(view, self.action, year, month, day))

        async def process(self, query: CallbackQuery, view: str, _date: date) -> bool:
            if view == 'day':
                await self.set_view(query, 'day', datetime.now().date())
                return False
            elif view == 'month':
                await self.set_view(query, 'month', date(_date.year, datetime.now().date().month, _date.day))
                return False
            elif view == 'year':
                await self.set_view(query, 'month', date(datetime.now().date().year, _date.month, _date.day))
                return False

    class CancelAction(DatepickerCustomAction):
        action: str = 'cancel'
        label: str = 'Cancel'

        def get_action(self, view: str, year: int, month: int, day: int) -> InlineKeyboardButton:
            return InlineKeyboardButton(self.label,
                                        callback_data=self._get_callback(view, self.action, year, month, day))

        async def process(self, query: CallbackQuery, view: str, _date: date) -> bool:
            if view == 'day':
                await query.message.delete()
                return False

    return DatepickerSettings(
        initial_view='month',
        views={
            'day': {
                'footer': ['prev-month', 'today', 'next-month', ['cancel']],
            },
            'month': {
                'footer': ['today']
            },
            'year': {
                'header': ['today'],
            }
        },
        custom_actions=[TodayAction, CancelAction]
    )


@dp.message_handler(state='*')
async def _main(message: Message):
    datepicker = Datepicker(_get_datepicker_settings())

    markup = datepicker.start_calendar()
    await message.answer('Select a date: ', reply_markup=markup)


@dp.callback_query_handler(Datepicker.datepicker_callback.filter())
async def _process_datepicker(callback_query: CallbackQuery, callback_data: dict):
    datepicker = Datepicker(_get_datepicker_settings())

    _date = await datepicker.process(callback_query, callback_data)
    if _date:
        await callback_query.message.answer(_date.strftime('%d/%m/%Y'))

    await callback_query.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
