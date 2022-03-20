# Aiogram datepicker widget

## Installing

    pip install aiogram-datepicker

## Simple usage
    import logging
    import os
    from datetime import datetime
    
    from aiogram import Bot, Dispatcher
    from aiogram.types import Message, CallbackQuery
    from aiogram.utils import executor
    
    from aiogram_datepicker import Datepicker, DatepickerSettings
    
    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(token=os.environ['API_TOKEN'])
    dp = Dispatcher(bot, run_tasks_by_default=True)
    
    def _get_datepicker_settings():
        return DatepickerSettings() # some [Settings](#Settings)
    
    @dp.message_handler(state='*')
    async def _main(message: Message):
        datepicker = Datepicker(_get_datepicker_settings())
    
        markup = datepicker.start_calendar()
        await message.answer('Select a date: ', reply_markup=markup)
    
    
    @dp.callback_query_handler(Datepicker.datepicker_callback.filter())
    async def _process_datepicker(callback_query: CallbackQuery, callback_data: dict):
        datepicker = Datepicker(_get_datepicker_settings())
    
        date = await datepicker.process(callback_query, callback_data)
        if date:
            await callback_query.message.answer(date.strftime('%d/%m/%Y'))
    
        await callback_query.answer()
    
    
    if __name__ == '__main__':
        executor.start_polling(dp, skip_updates=True)


#Settings
    DatepickerSettings(
        initial_view='day', #available views -> day, month, year
        initial_date=datetime.now().date(), # default date
        views={
            'day': {
                'show_weekdays': True,
                'weekdays_labels': ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'],
                'header': ['prev-year', 'days-title', 'next-year'],
                'footer': ['prev-month', 'select', 'next-month'],
                #available actions -> prev-year, days-title, next-year, prev-month, select, next-month, ignore
            },
            'month': {
                'months_labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                'header': ['prev-year', 'year', 'next-year'],
                'footer': ['select'],
                #available actions -> prev-year, year, next-year, select, ignore
            },
            'year': {
                'header': [],
                'footer': ['prev-years', 'next-years'],
                #available actions -> prev-years, ignore, next-years
            }
        },
        labels={
            'prev-year': '<<',
            'next-year': '>>',
            'prev-years': '<<',
            'next-years': '>>',
            'days-title': '{month} {year}',
            'selected-day': '{day} *',
            'selected-month': '{month} *',
            'present-day': '• {day} •',
            'prev-month': '<',
            'select': 'Select',
            'next-month': '>',
            'ignore': ''
        }
    )

## Demo:

![aiogram-datepicker](https://i.imgur.com/15hSnwZ.gif)
