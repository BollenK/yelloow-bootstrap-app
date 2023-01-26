import calendar
import os
import sys
from datetime import datetime, timedelta
from enum import Enum

cur_path = os.getcwd()
sys.path.append(cur_path + "/src")


from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from yelloow.shared.database.database import engine
from yelloow_models.models import Date


class Day(str, Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"
    ISO = "ISO"


class STRFTIMEFirstDayOfWeek(str, Enum):
    Monday = "%W"
    Sunday = "%U"
    ISO = "%V"


DATE_RANGE_START = "01-01-2001"
DATE_RANGE_END = "31-12-2030"
DATE_FORMAT = "%d-%m-%Y"
# WEEKDAY() starts at 0, whereas, day, month start at 1
WEEK_DAY_NUMS = (
    [0, 1, 2, 3, 4] if STRFTIMEFirstDayOfWeek.Monday else [6, 0, 1, 2, 3]
)  # Make solution for iso (only when needed)
FISCAL_YEAR_START_MONTH = 1
FIRST_DAY_OF_WEEK: Day = Day.Monday


_first_day_of_week_to_strftime_first_day_of_week_mapping = {
    Day.Monday: STRFTIMEFirstDayOfWeek.Monday,
    Day.Sunday: STRFTIMEFirstDayOfWeek.Sunday,
    Day.ISO: STRFTIMEFirstDayOfWeek.ISO,
}

_STRFTIME_WEEKDAY_NAME = "%A"
_STRFTIME_WEEKDAY_ABBREV = "%a"
_STRFTIME_MONTH_NAME = "%B"
_STRFTIME_MONTH_NAME_ABBREV = "%b"
_STRFTIME_YEAR_NUM_FULL = "%Y"
_STRFTIME_MONTH_NUM = "%m"
_STRFTIME_DAY_NUM = "%d"
_STRFTIME_FIRST_DAY_OF_WEEK = (
    _first_day_of_week_to_strftime_first_day_of_week_mapping[
        FIRST_DAY_OF_WEEK
    ].value
)


def get_date_key_from_datetime(date_time: datetime) -> int:
    return int(
        date_time.strftime(
            _STRFTIME_YEAR_NUM_FULL + _STRFTIME_MONTH_NUM + _STRFTIME_DAY_NUM
        )
    )


def get_delta_in_days_from_date_range(start: datetime, end: datetime) -> int:
    return (end - start).days


def get_quarter_from_datetime(date_time: datetime) -> int:
    return ((date_time.month - 1) // 3) + 1


def construct_date_from_datetime(
    date_time: datetime, start_date_time: datetime
) -> Date:
    return Date(
        date_key=get_date_key_from_datetime(date_time),
        full_date=date_time,
        day_of_week=date_time.weekday() + 1,
        day_num_in_month=date_time.day,
        day_num_overall=get_delta_in_days_from_date_range(
            start_date_time, date_time
        )
        + 1,
        day_name=date_time.strftime(_STRFTIME_WEEKDAY_NAME),
        day_abbrev=date_time.strftime(_STRFTIME_WEEKDAY_ABBREV),
        weekday_flag=date_time.weekday() in WEEK_DAY_NUMS,
        week_num_in_year=date_time.strftime(_STRFTIME_FIRST_DAY_OF_WEEK),
        month=date_time.month,
        month_name=date_time.strftime(_STRFTIME_MONTH_NAME),
        month_abbrev=date_time.strftime(_STRFTIME_MONTH_NAME_ABBREV),
        quarter=get_quarter_from_datetime(date_time),
        year=date_time.year,
        yearmo=date_time.strftime(
            _STRFTIME_YEAR_NUM_FULL + _STRFTIME_MONTH_NUM
        ),
        last_day_in_month_flag=date_time.day
        == calendar.monthrange(date_time.year, date_time.month)[1],
    )


def seed_dates(session: Session):
    start_dt: datetime = datetime.strptime(DATE_RANGE_START, DATE_FORMAT)
    end_dt: datetime = datetime.strptime(DATE_RANGE_END, DATE_FORMAT)
    num_of_days = (end_dt - start_dt).days

    dates = [
        construct_date_from_datetime(start_dt + timedelta(days=i), start_dt)
        for i in range(num_of_days)
    ]
    import pandas as pd
    s = pd.DataFrame([date.__dict__ for date in dates])
    s.drop("_sa_instance_state", axis=1, inplace=True)
    s.set_index("date_key", inplace=True)
    s.to_csv("./dates.csv")
    session.add_all(dates)
    session.commit()


if __name__ == "__main__":
    session: Session = sessionmaker(bind=engine)()

    seed_dates(session)
