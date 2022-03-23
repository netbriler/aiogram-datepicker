from datetime import date
from typing import Union

from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .base import BaseView
from ..helpers import merge_list
from ..settings import DatepickerSettings


class YearView(BaseView):
    def __init__(self, settings: DatepickerSettings, set_view):
        super().__init__(settings, set_view)
        self.custom_actions = []
        for custom_action in settings.custom_actions:
            self.custom_actions.append(custom_action(settings, set_view))

        self.settings = settings.views['year']
        self.labels = settings.labels
        self.set_view = set_view
        self.select_disabled = 'select' not in merge_list(self.settings['header']) \
                               and 'select' not in merge_list(self.settings['footer'])

    def _get_action(self, view: str, action: str, year: int, month: int, day: int) -> InlineKeyboardButton:
        if action in ['prev-years', 'next-years', 'ignore']:
            return InlineKeyboardButton(self.labels[action],
                                        callback_data=self._get_callback(view, action, year, month, day))

        for custom_action in self.custom_actions:
            if custom_action.action == action:
                return custom_action.get_action(view, year, month, day)

    def get_markup(self, _date: date = None, offset: int = 4) -> InlineKeyboardMarkup:
        year, month, day = _date.year, _date.month, _date.day

        markup = InlineKeyboardMarkup(row_width=3)

        markup = self._insert_actions(markup, self.settings['header'], 'year', year, month, day)

        markup.row()
        for value in range(year - offset, year + offset + 1):
            markup.insert(InlineKeyboardButton(
                f'{value}*' if year == value else str(value),
                callback_data=self._get_callback('year', 'set-year', value, month, day)
            ))

        markup = self._insert_actions(markup, self.settings['footer'], 'year', year, month, day)

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
            await self.set_view(query, 'month', _date)

        else:
            for custom_action in self.custom_actions:
                if custom_action.action == action:
                    return await custom_action.process(query, 'year', _date)

        return False
