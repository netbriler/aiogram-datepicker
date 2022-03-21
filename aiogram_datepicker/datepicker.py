from datetime import datetime, date

from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData

from .settings import DatepickerSettings
from .views import DayView, MonthView, YearView


class Datepicker:
    datepicker_callback = CallbackData('datepicker', 'view', 'action', 'year', 'month', 'day')
    ignore_callback = datepicker_callback.new('', 'ignore', -1, -1, -1)

    def __init__(self, settings: DatepickerSettings = None):
        if settings is None:
            settings = DatepickerSettings()

        self.settings = settings

        self.views = {
            'day': DayView(settings, set_view=self.set_view),
            'month': MonthView(settings, set_view=self.set_view),
            'year': YearView(settings, set_view=self.set_view),
        }

    def start_calendar(self):
        return self.views[self.settings.initial_view].get_markup(self.settings.initial_date)

    async def set_view(self, query: CallbackQuery, view: str, _data: date):
        if view not in ['day', 'month', 'year']:
            return False
        return await query.message.edit_reply_markup(self.views[view].get_markup(_data))

    async def process(self, query: CallbackQuery, data: CallbackData) -> date:
        action = data['action']

        view = data['view']
        if action == 'ignore' or view not in self.views:
            await query.answer(cache_time=60)
            return False

        _date = datetime(int(data['year']), int(data['month']), int(data['day'])).date()

        try:
            return await self.views[view].process(query, action, _date)
        except:
            await query.answer(cache_time=60)

        return False
