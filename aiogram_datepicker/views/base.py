from abc import ABC, abstractmethod
from datetime import date
from typing import Union

from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from ..callback_data import datepicker_callback


class BaseView(ABC):
    _datepicker_callback: CallbackData = datepicker_callback

    def _get_callback(self, view: str, action: str, year: int, month: int, day: int) -> str:
        return self.datepicker_callback.new(view, action, year, month, day)

    @abstractmethod
    def __init__(self, settings: dict):
        pass

    @property
    def datepicker_callback(self) -> CallbackData:
        return self._datepicker_callback

    @abstractmethod
    def get_markup(self, _date: date = None) -> InlineKeyboardMarkup:
        pass

    @abstractmethod
    async def process(self, query: CallbackQuery, action: str, _date: date) -> Union[date, bool]:
        pass
