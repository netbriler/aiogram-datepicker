from datetime import datetime, date
from typing import Union, List, Dict

from .custom_action import DatepickerCustomAction
from .helpers import merge_list

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


class DatepickerSettings:
    def __init__(self, initial_date: date = datetime.now().date(), initial_view: str = 'day',
                 views: Dict[str, Dict[str, Union[str, List[str], bool]]] = None, labels: Dict[str, str] = None,
                 custom_actions: list[DatepickerCustomAction] = list()):
        if labels is None:
            labels = _default_labels
        if views is None:
            views = _default_views

        self.available_actions = list(_default_labels.keys())
        for custom_action in custom_actions:
            self.available_actions.append(custom_action.action)

        self.custom_actions = custom_actions
        self.initial_date = initial_date
        self.initial_view = self.initial_view_validate(initial_view)
        self.views = self.initial_views_validate(views)
        self.labels = self.labels_validate(labels)

    @staticmethod
    def initial_view_validate(v):
        if v not in _available_views:
            raise ValueError(f'no view named {v}')
        return v

    def initial_views_validate(self, v):
        if not isinstance(v, dict):
            raise ValueError(f'initial_views -> views should be dict')

        views = _default_views
        if 'day' in v:
            views['day'].update(v['day'])

            if len(views['day']['weekdays_labels']) != 7:
                raise ValueError(f'day -> weekdays_labels -> should be 7 weekdays labels')

        if 'month' in v:
            views['month'].update(v['month'])

            if len(views['month']['months_labels']) != 12:
                raise ValueError(f'month -> months_labels -> should be 12 months labels')

        if 'year' in v:
            views['year'].update(v['year'])

        for view in _available_views:
            if isinstance(views[view]['header'], str):
                views[view]['header'] = views[view]['header'].split(',')
            if isinstance(views[view]['footer'], str):
                views[view]['header'] = views[view]['header'].split(',')

            for action in merge_list(views[view]['header']):
                if action not in self.available_actions:
                    raise ValueError(f'views -> {view} -> header -> no action named {action}')

            for action in merge_list(views[view]['footer']):
                if action not in self.available_actions:
                    raise ValueError(f'views -> {view} -> footer -> no action named {action}')

        return views

    @staticmethod
    def labels_validate(v):
        labels = _default_labels
        labels.update(v)

        return labels
