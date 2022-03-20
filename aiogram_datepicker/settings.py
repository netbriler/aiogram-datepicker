from datetime import datetime, date
from typing import Union, List, Dict

from pydantic import BaseModel, validator

_available_views = ('day', 'month', 'year')

_default_views = {
    'day': {
        'weekdays_labels': ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'],

        'header': ['prev-year', 'days-title', 'next-year'],

        'show_weekdays': True,

        'footer': ['prev-month', 'select', 'next-month'],
    },
    'month': {
        'months_labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],

        'header': ['prev-year', 'year', 'next-year'],

        'footer': ['select']
    },
    'year': {
        'header': [],

        'footer': ['prev-years', 'next-years']
    }
}

_default_labels = {
    'prev-year': '<<',
    'next-year': '>>',
    'prev-years': '<<',
    'next-years': '>>',
    'days-title': '{month} {year}',
    'year': '{year}',
    'selected-day': '{day} *',
    'selected-month': '{month} *',
    'present-day': '• {day} •',
    'prev-month': '<',
    'select': 'Select',
    'next-month': '>',
    'ignore': ''
}


class DatepickerSettings(BaseModel):
    initial_view: str = 'day'
    initial_date: date = datetime.now().date()

    views: Dict[str, Dict[str, Union[str, List[str], bool]]] = _default_views
    labels: Dict[str, str] = _default_labels

    @validator('initial_view')
    def initial_view_validator(cls, v):
        if v not in _available_views:
            raise ValueError(f'no view named {v}')
        return v

    @validator('views')
    def initial_views_validator(cls, v):
        views = _default_views
        if 'day' in v:
            if len(v['day']['weekdays_labels']) != 7:
                raise ValueError(f'should be 7 weekdays labels {v}')

            views['day'].update(v['day'])

        if 'month' in v:
            if len(v['month']['months_labels']) != 12:
                raise ValueError(f'should be 12 months labels {v}')

            views['month'].update(v['month'])

        if 'year' in v:
            views['year'].update(v['year'])

        for view in _available_views:
            if isinstance(views[view]['header'], str):
                views[view]['header'] = views[view]['header'].split(',')
            if isinstance(views[view]['footer'], str):
                views[view]['header'] = views[view]['header'].split(',')

            for action in views[view]['header']:
                if action not in _default_labels.keys():
                    raise ValueError(f'header -> no label named {v}')

            for action in views[view]['footer']:
                if action not in _default_labels.keys():
                    raise ValueError(f'footer -> no label named {v}')

        return views

    @validator('labels')
    def labels_validator(cls, v):
        labels = _default_labels
        labels.update(v)

        return labels
