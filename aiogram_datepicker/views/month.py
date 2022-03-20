from datetime import date
from typing import Union

from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseView
from ..settings import DatepickerSettings


class MonthView(BaseView):
    def __init__(self, settings: DatepickerSettings, set_view):
        super().__init__(settings)
        self.settings = settings.views['month']
        self.labels = settings.labels
        self.set_view = set_view
        self.months = settings.views['month']['months_labels']

    def _get_action(self, view: str, action: str, year: int, month: int, day: int) -> str:
        if action in ['prev-year', 'next-year', 'ignore']:
            return InlineKeyboardButton(self.labels[action],
                                        callback_data=self._get_callback(view, action, year, month, day))

        elif action == 'year':
            return InlineKeyboardButton(self.labels['year'].replace('{year}', year),
                                        callback_data=self._get_callback('year', 'set-view', year, month, day))

        elif action == 'select':
            return InlineKeyboardButton(self.labels[action],
                                        callback_data=self._get_callback(view, action, year, month, day))

    def get_markup(self, _date: date = None) -> InlineKeyboardMarkup:
        year, month, day = _date.year, _date.month, _date.day

        markup = InlineKeyboardMarkup(row_width=4)

        if len(self.settings['header']):
            markup.add(
                *[self._get_action('month', action, year, month, day) for action in
                  self.settings['header']])

        markup.row()
        for i, month_title in enumerate(self.months, start=1):
            markup.insert(InlineKeyboardButton(
                f'{month_title}*' if i == month else month_title,
                callback_data=self._get_callback('month', 'set-month', year, i, day)
            ))

        if len(self.settings['footer']):
            markup.add(
                *[self._get_action('month', action, year, month, day) for action in
                  self.settings['footer']])

        return markup

    async def process(self, query: CallbackQuery, action: str, _date: date) -> Union[date, bool]:
        if action == 'set-view':
            await query.message.edit_reply_markup(self.get_markup(_date))

        elif action == 'set-month':
            await query.message.edit_reply_markup(self.get_markup(_date))

        elif action == 'prev-year':
            prev_date = date(_date.year - 1, _date.month, _date.day)
            await query.message.edit_reply_markup(self.get_markup(prev_date))

        elif action == 'next-year':
            next_date = date(_date.year + 1, _date.month, _date.day)
            await query.message.edit_reply_markup(self.get_markup(next_date))

        elif action == 'select':
            await query.message.edit_reply_markup(self.set_view('day', _date))

        return False
