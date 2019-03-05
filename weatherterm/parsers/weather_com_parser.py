from weatherterm.core import ForecastType
from weatherterm.core import Forecast
from weatherterm.core import Request
from weatherterm.core import Unit
from weatherterm.core import UnitConverter

import re


class WeatherComParser:

    def __init__(self):
        self._forecast = {
            ForecastType.TODAY: self._today_forecast,
            ForecastType.FIVEDAYS: self._five_and_ten_days_forecast,
            ForecastType.TENDAYS: self._five_and_ten_days_forecast,
            ForecastType.WEEKEND: self._weekend_forecast,
        }
        self._base_url = 'http://weather.com/weather/{forecast}/1/{area}'
        self._request = Request(self._base_url)
        self._temp_regex = re.compile("([0-9]+)\D{,2}([0-9]+)")
        self._only_digits_regex = re.compile('[0-9]+')
        self._unit_converter = UnitConverter(Unit.FAHRENHEIT)

    def _get_data(self, container, search_items):
        scraped_data = {}

        for key, value in search_items.items():
            result = container.find(value, class_=key)
            data = None if result is None else result.get_text()
            if data is not None:
                scraped_data[key] = data
            return scraped_data

    def _parse(self, container, criteria):
        results = [self._get_data(item, criteria)
                   for item in container.children]

        return [result for result in results if result]

    def _clear_str_number(self, str_number):
        result = self._only_digits_regex.match(str_number)
        return '--' if result is None else result.group()

    def _get_additional_info(self, content):
        data = tuple(item.td.span.get_text()
                     for item in content.table.tbody.children)
        return data[:2]

    def _today_forecast(self, args):
        raise NotImplementedError()

    def _five_and_ten_days_forecast(self, args):
        raise NotImplementedError

    def _weekend_forecast(self, args):
        raise NotImplementedError

    def run(self, args):
        self._forecast_type = args.forecast_option
        forecast_function = self._forecast[args.forecast_option]
        return forecast_function(args)
