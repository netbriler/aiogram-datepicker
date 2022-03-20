import calendar
from datetime import datetime, date
from typing import Union

from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseView
from ..settings import DatepickerSettings


class DayView(BaseView):
    def __init__(self, settings: DatepickerSettings, set_view):
        super().__init__(settings)
        self.settings = settings.views['day']
        self.labels = settings.labels
        self.set_view = set_view

    def _get_action(self, view: str, action: str, year: int, month: int, day: int) -> str:
        if action in ['prev-year', 'next-year', 'prev-month', 'next-month', 'ignore']:
            return InlineKeyboardButton(self.labels[action],
                                        callback_data=self._get_callback(view, action, year, month, day))

        elif action == 'days-title':
            label = self.labels['days-title'].replace('{month}', calendar.month_name[month]) \
                .replace('{year}', str(year))

            return InlineKeyboardButton(label,
                                        callback_data=self._get_callback('month', 'set-view', year, month, day))

        elif action == 'select':
            return InlineKeyboardButton(self.labels[action],
                                        callback_data=self._get_callback(view, action, year, month, day))

    def get_markup(self, _date: date = None) -> InlineKeyboardMarkup:
        year, month, day = _date.year, _date.month, _date.day

        markup = InlineKeyboardMarkup(row_width=7)

        if len(self.settings['header']):
            markup.add(
                *[self._get_action('day', action, year, month, day) for action in self.settings['header']])

        if self.settings['show_weekdays']:
            markup.row()
            for week_day in self.settings['weekdays_labels']:
                markup.insert(
                    InlineKeyboardButton(week_day, callback_data=self._get_callback('day', 'ignore', year, month, day)))

        markup.row()
        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            for week_day in week:
                if week_day == 0:
                    markup.insert(
                        InlineKeyboardButton(' ', callback_data=self._get_callback('day', 'ignore', year, month, day)))
                    continue

                label = f'{week_day}'
                if date(year, month, week_day) == _date:
                    label = f'{week_day} *'
                elif date(year, month, week_day) == datetime.now().date():
                    label = f'• {week_day} •'

                markup.insert(InlineKeyboardButton(
                    label, callback_data=self._get_callback('day', 'set-day', year, month, week_day)
                ))

        if len(self.settings['footer']):
            markup.add(
                *[self._get_action('day', action, year, month, day) for action in self.settings['footer']])

        return markup

    async def process(self, query: CallbackQuery, action: str, _date: date) -> Union[date, bool]:
        if action == 'select':
            return _date

        elif action == 'set-day':
            await query.message.edit_reply_markup(self.get_markup(_date))

        elif action == 'prev-year':
            prev_date = date(_date.year - 1, _date.month, _date.day)
            await query.message.edit_reply_markup(self.get_markup(prev_date))

        elif action == 'next-year':
            next_date = date(_date.year + 1, _date.month, _date.day)
            await query.message.edit_reply_markup(self.get_markup(next_date))

        elif action == 'prev-month':
            prev_date = date(_date.year - int(_date.month == 1), 12 if _date.month == 1 else _date.month - 1, _date.day)
            await query.message.edit_reply_markup(self.get_markup(prev_date))

        elif action == 'next-month':
            next_date = date(_date.year + int(_date.month == 12), ((_date.month % 12) + 1), _date.day)
            await query.message.edit_reply_markup(self.get_markup(next_date))

        return False
