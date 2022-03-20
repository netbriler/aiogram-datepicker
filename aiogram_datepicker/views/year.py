from datetime import date
from typing import Union

from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseView
from ..settings import DatepickerSettings


class YearView(BaseView):
    def __init__(self, settings: DatepickerSettings, set_view):
        super().__init__(settings)
        self.settings = settings.views['year']
        self.labels = settings.labels
        self.set_view = set_view

    def _get_action(self, view: str, action: str, year: int, month: int, day: int) -> str:
        if action in ['prev-years', 'next-years', 'ignore']:
            return InlineKeyboardButton(self.labels[action],
                                        callback_data=self._get_callback(view, action, year, month, day))

    def get_markup(self, _date: date = None, offset: int = 4) -> InlineKeyboardMarkup:
        year, month, day = _date.year, _date.month, _date.day

        markup = InlineKeyboardMarkup(row_width=3)

        if len(self.settings['header']):
            markup.add(
                *[self._get_action('year', action, year, month, day) for action in
                  self.settings['header']])

        for value in range(year - offset, year + offset + 1):
            markup.insert(InlineKeyboardButton(
                f'{value}*' if year == value else str(value),
                callback_data=self._get_callback('year', 'set-year', value, month, day)
            ))

        if len(self.settings['footer']):
            markup.add(
                *[self._get_action('year', action, year, month, day) for action in
                  self.settings['footer']])

        return markup

    async def process(self, query: CallbackQuery, action: str, _date: date) -> Union[date, bool]:
        if action == 'set-view':
            await query.message.edit_reply_markup(self.get_markup(_date))

        elif action == 'prev-years':
            prev_date = date(_date.year - 9, _date.month, _date.day)
            await query.message.edit_reply_markup(self.get_markup(prev_date))

        elif action == 'next-years':
            next_date = date(_date.year + 9, _date.month, _date.day)
            await query.message.edit_reply_markup(self.get_markup(next_date))

        elif action == 'set-year':
            await query.message.edit_reply_markup(self.set_view('month', _date))

        return False
