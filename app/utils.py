import pytz


APPOINTMENT_START_TIME = 9
APPOINTMENT_END_TIME = 17
NO_APPOINTMENT_WEEKDAY_CODE = 6
PH_TIMEZONE = pytz.timezone('Asia/Manila')


def utc_to_local(utc_dt, local_tz=PH_TIMEZONE):
    """
    Changes a utc/naive datetime to an aware one.

    Args:
        utc_dt (datetime): The naive datetime object to be converted.
        local_tz (pytz): Timezone information.

    Returns:
        datetime: The timezone aware datetime.
    """
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)
