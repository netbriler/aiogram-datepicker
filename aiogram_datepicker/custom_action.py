from abc import ABC, abstractmethod
from datetime import date

from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from .callback_data import datepicker_callback


class DatepickerCustomAction(ABC):
    _datepicker_callback: CallbackData = datepicker_callback

    action: str
    label: str

    def __init__(self, settings, set_view):
        super().__init__()
        self.settings = settings
        self.set_view = set_view

    def _get_callback(self, view: str, action: str, year: int, month: int, day: int) -> str:
        return self._datepicker_callback.new(view, action, year, month, day)

    @abstractmethod
    def get_action(self, view: str, year: int, month: int, day: int) -> InlineKeyboardButton:
        pass

    @abstractmethod
    async def process(self, query: CallbackQuery, view: str, _date: date) -> bool:
        pass
