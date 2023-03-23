from datetime import datetime


def is_date_equal(first: datetime, second: datetime) -> bool:
    is_year_equal = first.year == second.year
    is_month_equal = first.month == second.month
    is_day_equal = first.day == second.day

    return is_month_equal and is_day_equal and is_year_equal


def is_date_more(first: datetime, second: datetime) -> bool:
    is_year_more = first.year >= second.year
    is_month_more = first.month >= second.month
    is_day_more = first.day > second.day

    return is_month_more and is_day_more and is_year_more


def is_date_less(first: datetime, second: datetime) -> bool:
    is_year_less = first.year <= second.year
    is_month_less = first.month <= second.month
    is_day_less = first.day < second.day

    return is_month_less and is_day_less and is_year_less
