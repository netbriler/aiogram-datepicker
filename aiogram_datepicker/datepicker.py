import calendar
from datetime import datetime, timedelta, date

from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


class Datepicker:
    datepicker_callback = CallbackData('datepicker', 'view', 'action', 'year', 'month', 'day')
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ignore_callback = datepicker_callback.new('', 'ignore', -1, -1, -1)

    def __init__(self, state, initial_date=datetime.now()):
        self.state = state
        self.initial_date = initial_date

    async def init(self):
        async with self.state.proxy() as proxy:
            proxy.setdefault('datepicker_selected', self.initial_date.strftime('%Y-%m-%d'))
            await self.select_date(datetime.strptime(proxy['datepicker_selected'], '%Y-%m-%d').date())

    def _get_callback(self, view: str, action: str, year: int, month: int, day: int) -> str:
        return self.datepicker_callback.new(view, action, year, month, day)

    async def select_date(self, _date: date):
        self.selected_date = _date

        async with self.state.proxy() as proxy:
            proxy['datepicker_selected'] = _date.strftime('%Y-%m-%d')

    async def start_calendar(self):
        await self.init()

        return self.get_days_view(self.initial_date)

    def get_days_view(self, _date: date = None) -> InlineKeyboardMarkup:
        year, month, day = _date.year, _date.month, _date.day

        markup = InlineKeyboardMarkup(row_width=7)
        markup.add(
            InlineKeyboardButton('<<', callback_data=self._get_callback('day', 'prev-year', year, month, day)),
            InlineKeyboardButton(f'{calendar.month_name[month]} {year}',
                                 callback_data=self._get_callback('month', 'set-view', year, month, day)),
            InlineKeyboardButton('>>', callback_data=self._get_callback('day', 'next-year', year, month, day))
        )

        markup.row()
        for week_day in ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']:
            markup.insert(InlineKeyboardButton(week_day, callback_data=self.ignore_callback))

        markup.row()
        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            for week_day in week:
                if week_day == 0:
                    markup.insert(InlineKeyboardButton(' ', callback_data=self.ignore_callback))
                    continue

                label = f'{week_day}'
                if date(year, month, week_day) == self.selected_date:
                    label = f'{week_day} *'
                elif date(year, month, week_day) == datetime.now().date():
                    label = f'• {week_day} •'

                markup.insert(InlineKeyboardButton(
                    label, callback_data=self._get_callback('day', 'set-day', year, month, week_day)
                ))

        markup.add(
            InlineKeyboardButton('<', callback_data=self._get_callback('day', 'prev-month', year, month, day)),
            InlineKeyboardButton(
                'Select',
                callback_data=self._get_callback('day', 'select', self.selected_date.year, self.selected_date.month,
                                                 self.selected_date.day)),
            InlineKeyboardButton('>', callback_data=self._get_callback('day', 'next-month', year, month, day))
        )

        return markup

    def get_month_view(self, _date: date = None) -> InlineKeyboardMarkup:
        year, month, day = _date.year, _date.month, _date.day

        markup = InlineKeyboardMarkup(row_width=4)
        markup.add(
            InlineKeyboardButton('<<', callback_data=self._get_callback('month', 'prev-year', year, month, day)),
            InlineKeyboardButton(year, callback_data=self._get_callback('year', 'set-view', year, month, day)),
            InlineKeyboardButton('>>', callback_data=self._get_callback('month', 'next-year', year, month, day))
        )

        markup.row()
        for i, month_title in enumerate(self.months, start=1):
            markup.insert(InlineKeyboardButton(
                f'{month_title}*' if i == month else month_title,
                callback_data=self._get_callback('month', 'set-month', year, i, day)
            ))

        markup.add(
            InlineKeyboardButton('Select', callback_data=self._get_callback('month', 'select', year, month, day))
        )

        return markup

    def get_year_view(self, _date: date = None, offset: int = 4) -> InlineKeyboardMarkup:
        year, month, day = _date.year, _date.month, _date.day

        markup = InlineKeyboardMarkup(row_width=3)
        for value in range(year - offset, year + offset + 1):
            markup.insert(InlineKeyboardButton(
                f'{value}*' if self.selected_date.year == value else str(value),
                callback_data=self._get_callback('year', 'set-year', value, month, day)
            ))

        markup.add(
            InlineKeyboardButton('<<', callback_data=self._get_callback('year', 'prev-years', year, month, day)),
            InlineKeyboardButton('>>', callback_data=self._get_callback('year', 'next-years', year, month, day))
        )

        return markup

    async def day_actions(self, query: CallbackQuery, action: str, _date: date) -> date:
        if action == 'select':
            return self.selected_date

        elif action == 'set-day':
            await self.select_date(_date)
            await query.message.edit_reply_markup(self.get_days_view(_date))

        elif action == 'prev-year':
            prev_date = date(_date.year - 1, _date.month, _date.day)
            await query.message.edit_reply_markup(self.get_days_view(prev_date))

        elif action == 'next-year':
            next_date = date(_date.year + 1, _date.month, _date.day)
            await query.message.edit_reply_markup(self.get_days_view(next_date))

        elif action == 'prev-month':
            prev_date = date(_date.year - int(_date.month == 1), 12 if _date.month == 1 else _date.month - 1, _date.day)
            await query.message.edit_reply_markup(self.get_days_view(prev_date))

        elif action == 'next-month':
            next_date = date(_date.year + int(_date.month == 12), ((_date.month % 12) + 1), _date.day)
            await query.message.edit_reply_markup(self.get_days_view(next_date))

        return False

    async def month_actions(self, query: CallbackQuery, action: str, _date: date) -> date:
        if action == 'set-view':
            await query.message.edit_reply_markup(self.get_month_view(_date))

        elif action == 'set-month':
            await query.message.edit_reply_markup(self.get_month_view(_date))

        elif action == 'prev-year':
            prev_date = date(_date.year - 1, _date.month, _date.day)
            await query.message.edit_reply_markup(self.get_month_view(prev_date))

        elif action == 'next-year':
            next_date = date(_date.year + 1, _date.month, _date.day)
            await query.message.edit_reply_markup(self.get_month_view(next_date))

        elif action == 'select':
            await self.select_date(_date)
            await query.message.edit_reply_markup(self.get_days_view(_date))

        return False

    async def year_actions(self, query: CallbackQuery, action: str, _date: date) -> date:
        if action == 'set-view':
            await query.message.edit_reply_markup(self.get_year_view(_date))

        elif action == 'prev-years':
            prev_date = date(_date.year - 9, _date.month, _date.day)
            await query.message.edit_reply_markup(self.get_year_view(prev_date))

        elif action == 'next-years':
            next_date = date(_date.year + 9, _date.month, _date.day)
            await query.message.edit_reply_markup(self.get_year_view(next_date))

        elif action == 'set-year':
            await self.select_date(_date)
            await query.message.edit_reply_markup(self.get_month_view(_date))

        return False

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> date:
        await self.init()

        action = data['action']

        if action == 'ignore':
            await query.answer(cache_time=60)
            return False

        view = data['view']
        _date = datetime(int(data['year']), int(data['month']), int(data['day'])).date()

        try:
            if view == 'day':
                return await self.day_actions(query, action, _date)
            elif view == 'month':
                return await self.month_actions(query, action, _date)
            elif view == 'year':
                return await self.year_actions(query, action, _date)
        except:
            await query.answer(cache_time=60)

        return False
