import calendar
import datetime
from datetime import timedelta

import jdatetime
from django.utils import timezone


def _ensure_tz_aware(datetime_val):
    try:
        return timezone.make_aware(datetime_val)
    except ValueError:  # tzinfo already set
        return datetime_val


def date_part(date_or_datetime):
    """
    It takes into account timezone and then generates date out of the resulting localized
    datetime object. If dates are extracted from utc datetimes, the resulting date
    might be erroneous as a result of having 3:30/4:30 difference with timezone of Tehran
    and most timezones are in utc when they get out of db or are generated using timezone
    module
    :type date_or_datetime: datetime.date | datetime.datetime
    :rtype: datetime.date
    """
    if isinstance(date_or_datetime, datetime.datetime):
        return timezone.localtime(_ensure_tz_aware(date_or_datetime)).date()
    elif isinstance(date_or_datetime, datetime.date):
        return date_or_datetime
    else:
        raise TypeError('Input should be of type date or datetime. '
                        'Found {type}'.format(type=type(date_or_datetime)))


def today():
    """
    :rtype: datetime.date
    """
    return date_part(timezone.now())


def yesterday():
    """
    :rtype: datetime.date
    """
    return today() - timedelta(days=1)


def jalali_week_day_to_gregorian(week_day):
    return {0: 5, 1: 6, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, }[week_day]


def gregorian_week_day_to_jalali(week_day):
    return {5: 0, 6: 1, 0: 2, 1: 3, 2: 4, 3: 5, 4: 6, }[week_day]


def get_week_day(week_day_name: str) -> int:
    return {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}[week_day_name]


def next_week_day(week_day, exclusive=True, from_date=None):
    """
    Returns the first upcoming day which matches the week day.
    :param week_day: the day of the week as Monday == 0 ... Saturday == 5 Sunday == 6
    :type week_day: int
    :param exclusive: determines whether this method returns today if it matches the week_day or
    else it excludes today and continues looking for another day
    :type exclusive: bool
    :param from_date: the day which the method starts calculation from. Pass None to use today.
    :type: datetime.date
    :return: the calculated Date instance
    :rtype: datetime.date
    """
    from_date = today() if from_date is None else from_date
    potential_day = from_date + timedelta(days=1 if exclusive else 0)
    while potential_day.weekday() != week_day:
        potential_day += timedelta(days=1)
    return potential_day


def next_relative_week_day(week_day, from_date=None, relative_number=0) -> datetime.date:
    from_date = today() if from_date is None else from_date
    counter = 0 if from_date.weekday() == week_day else -1
    while from_date.weekday() != week_day or counter != relative_number:
        from_date += timedelta(days=1)
        if from_date.weekday() == week_day:
            counter += 1
    return from_date


def last_week_day(week_day, exclusive=True, from_date=None):
    """
    Returns the last past day which matches the week day excluding today.
    So if week_day == SATURDAY and from_date is SATURDAY the return value will be
    from_date - timedelta(days=7)
    :param week_day: the day of the week as Monday == 0 ... Saturday == 5 Sunday == 6
    :type week_day: int
    :param exclusive: determines whether this method returns today if it matches the week_day or
    else it excludes today and continues looking for another day
    :type exclusive: bool
    :param from_date: the day which the method starts calculation from. Pass None to use today.
    :type: datetime.date
    :return: the calculated Date instance
    :rtype: datetime.date
    """
    from_date = today() if from_date is None else from_date
    potential_day = from_date - timedelta(days=1 if exclusive else 0)
    while potential_day.weekday() != week_day:
        potential_day -= timedelta(days=1)
    return potential_day


def last_friday():
    """
    :rtype: datetime.date
    """
    return last_week_day(calendar.FRIDAY)


def start_of_week(date_or_datetime=None):
    """
    :rtype: datetime.date
    """
    if date_or_datetime is None:
        date_or_datetime = timezone.now()
    date_val = date_part(date_or_datetime)
    while date_val.weekday() != calendar.SATURDAY:
        date_val -= datetime.timedelta(1)
    return date_val


def start_of_week_before(date_or_datetime=None):
    return start_of_week(date_or_datetime) - timedelta(days=7)


def end_of_week_before(date_or_datetime=None):
    return start_of_week(date_or_datetime) - timedelta(days=1)


def end_of_week(date_or_datetime=None):
    """
    :rtype: datetime.date
    """
    if date_or_datetime is None:
        date_or_datetime = timezone.now()
    date_val = date_part(date_or_datetime)
    while date_val.weekday() != calendar.FRIDAY:
        date_val += timedelta(1)
    return date_val


def start_of_month(date_or_datetime=None):
    """
    :rtype: datetime.date
    """
    if date_or_datetime is None:
        date_or_datetime = timezone.now()
    date_val = date_part(date_or_datetime)
    while jdatetime.date.fromgregorian(date=date_val).day != 1:
        date_val -= timedelta(1)
    return date_val


def end_of_month(date_or_datetime=None):
    """
    :rtype: datetime.date
    """
    if date_or_datetime is None:
        date_or_datetime = timezone.now()
    date_val = date_part(date_or_datetime)
    while jdatetime.date.fromgregorian(date=date_val).month == \
            jdatetime.date.fromgregorian(date=date_val + timedelta(1)).month:
        date_val += timedelta(1)
    return date_val


def digitize_timedelta(time_delta):
    total_seconds = int(time_delta.total_seconds())
    return '{}:{:02}'.format(total_seconds // 60 ** 2, total_seconds % 60 ** 2 // 60)


def get_string_jalali(date_or_datetime_obj, datetime_format='%Y-%m-%d %H:%M:%S',
                      date_format='%Y-%m-%d'):
    if date_or_datetime_obj:
        if isinstance(date_or_datetime_obj, datetime.datetime):
            return jdatetime.datetime.fromgregorian(
                datetime=timezone.localtime(date_or_datetime_obj)).strftime(datetime_format)
        elif isinstance(date_or_datetime_obj, datetime.date):
            return jdatetime.date.fromgregorian(date=date_or_datetime_obj).strftime(date_format)
    return '-'
