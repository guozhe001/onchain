from datetime import datetime, timedelta
from unittest import TestCase

from util import date_util


class Test(TestCase):
    def test_is_date(self):
        date, is_date = date_util.is_date("2021-06-17 10:34")
        TestCase.assertTrue(self, is_date)
        TestCase.assertIsNotNone(self, date)

    def test_not_date(self):
        date, is_date = date_util.is_date("2021-06-17 10:34 hello")
        TestCase.assertFalse(self, is_date)
        TestCase.assertIsNone(self, date)

    def test_format_default_datetime(self):
        print(date_util.format_default_datetime(1623945600000))

    def test_to_date(self):
        date = datetime.fromisoformat("2021-06-17 10:34:00")
        print(date)
        print(type(date))
        print(date.timestamp())

    def test_interval_hours(self):
        date1 = datetime.fromisoformat("2021-08-11 10:34:00")
        date2 = datetime.fromisoformat("2021-08-11 12:38:01")
        hours = date_util.interval_hours(date2, date1)
        self.assertEqual(2, hours)

    def test_interval_hours1(self):
        date1 = datetime.fromisoformat("2021-08-11 10:34:00")
        date2 = datetime.fromisoformat("2021-08-11 12:38:01")
        hours = date_util.interval_hours(date1, date2)
        self.assertEqual(-2, hours)

    def test_interval_hours2(self):
        date1 = datetime.fromisoformat("2021-08-12 10:34:00")
        date2 = datetime.fromisoformat("2021-08-11 12:38:01")
        hours = date_util.interval_hours(date1, date2)
        self.assertEqual(21, hours)

    def test_interval(self):
        date1 = datetime.fromisoformat("2021-08-12 10:34:00")
        date2 = datetime.fromisoformat("2021-08-11 10:34:00")
        hours = date_util.interval(date1, date2, 60)
        self.assertEqual(24 * 60, hours)

    def test_interval1(self):
        date1 = datetime.fromisoformat("2021-08-12 10:00:00")
        date2 = datetime.fromisoformat("2021-08-11 10:34:00")
        hours = date_util.interval(date1, date2, 60)
        self.assertEqual(24 * 60 - 34, hours)

    def test_interval3(self):
        date1 = datetime.fromisoformat("2021-08-11 10:59:00")
        date2 = datetime.fromisoformat("2021-08-11 10:34:00")
        hours = date_util.interval(date1, date2, 60)
        self.assertEqual(59 - 34, hours)

    def test_interval2(self):
        date1 = datetime.fromisoformat("2021-08-11 10:59:00")
        date2 = datetime.fromisoformat("2021-08-11 10:34:00")
        self.assertTrue(date1 > date2)
        hours = date_util.interval(date2, date1, 60)
        self.assertEqual(34 - 59, hours)

    def test_date_hour(self):
        print(datetime.now().hour)

    def test_print_len(self):
        print(len('1109860f79f14ebaabe7086b863a90a2'))

    def test_format_unix_datetime(self):
        unix_datetime = date_util.format_unix_datetime(date_util.date_format, int(datetime.now().timestamp()))
        print(unix_datetime)

    def test_str_to_datetime(self):
        _datetime = date_util.str_to_datetime("2021-08-23 12:20:00")
        print(_datetime)
        self.assertTrue(isinstance(_datetime, datetime))

    def test_get_start_time_of_day(self):
        day = date_util.get_start_time_of_day(datetime.now())
        print(day)
        self.assertEqual(0, day.hour)
        self.assertEqual(0, day.minute)
        self.assertEqual(0, day.second)
        self.assertEqual(0, day.microsecond)

    def test_is_same_minute(self):
        now = date_util.str_to_datetime("2021-10-20 14:46:32")
        for i in range(5):
            date2 = now - timedelta(seconds=(1 + i) * 10)
            is_same_minute = date_util.is_same_minute(date2, now)
            print(f"i={i}, date1={now} and date2={date2} is {'' if is_same_minute else 'not'} same minute!")
            if i < 3:
                self.assertTrue(is_same_minute)
            else:
                self.assertFalse(is_same_minute)

    def test_to_start_of_day(self):
        d = date_util.str_to_datetime("2021-10-20 14:02:30")
        print(d)
        start_day = date_util.to_start_of_day(d)
        print(start_day)
        td: timedelta = d - start_day
        self.assertEqual(0, td.days)
        self.assertEqual(14 * 60 * 60 + 2 * 60 + 30, td.seconds)

    def test_to_rfc3339(self):
        now = datetime.now()
        rfc_ = date_util.to_rfc3339(now)
        print(type(rfc_))
        print(rfc_)
        self.assertTrue(isinstance(rfc_, str))

    def test_date_to_str(self):
        to_str = date_util.date_to_str(datetime.now())
        print(to_str)

    def test_date_to_str1(self):
        to_str = date_util.date_to_str(datetime.now(), date_util.date_format_1)
        print(to_str)

    def test_is_not_zero_time(self):
        now = datetime.now()
        is_zero_time = date_util.is_zero_time(now)
        print(f"{now} is {'' if is_zero_time else 'not'} zero time")

    def test_is_zero_time(self):
        dt = date_util.str_to_datetime("2020-10-01 00:00:00")
        is_zero_time = date_util.is_zero_time(dt)
        print(f"{dt} is {'' if is_zero_time else 'not '}zero time")
