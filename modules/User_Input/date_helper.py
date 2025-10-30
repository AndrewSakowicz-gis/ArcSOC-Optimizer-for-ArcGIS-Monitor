import zoneinfo, pytz
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
def get_timezones():
    return zoneinfo.available_timezones()
def get_now_date(timezone):
    tz = pytz.timezone(timezone)
    return datetime.now(tz)

def get_date(year, month, day, hour, minute, second, timezone):
    dt=datetime(year, month, day, hour, minute, 0)
    if timezone is not None:
         dt= datetime(year, month, day, hour, minute, second, tzinfo=ZoneInfo(timezone))
    return dt
def now_UTC_str():
    now_date_utc=get_now_date("UTC")
    return now_date_utc.isoformat()[:-6]+'Z'
def convert_to_utc(date):
    return date.astimezone(pytz.timezone("UTC"))
def date_from_timestamp(timeStamp):
    return datetime.fromtimestamp(timeStamp)
def date_from_timestamp_tz(timeStamp, timeZoneStr):
    tz = pytz.timezone(timeZoneStr)
    dt= datetime.fromtimestamp(timeStamp, tz)
    return dt.astimezone(pytz.timezone(timeZoneStr))
def subtract_time(date, days, hours, minutes):
    d=date-timedelta(days=days)
    d= d-timedelta(hours=hours)
    d= d-timedelta(minutes=minutes)
    return d
def add_time(date, days, hours):
    d=date+timedelta(days=days)
    d= d+timedelta(hours=hours)
    return d
def past_UTC_str(days, hours, minutes):
    now_date_utc=get_now_date("UTC")
    start_date_utc_low=subtract_time(now_date_utc, days, hours, minutes)
    return start_date_utc_low.isoformat()[:-6]+'Z'
def get_minute(date):
    return date.minute
def get_hour(date):
    return date.hour
def get_day(date):
    return date.day
def get_month(date):
    return date.month
def get_year(date):
    return date.year
def get_week(date):
    return date.week
def get_weekday(date):
    week_day=None
    wd =date.weekday()
    if wd==0:
        week_day="Monday"
    if wd==1:
        week_day="Tuesday"   
    if wd==2:
        week_day="Wednesday"
    if wd==3:
        week_day="Thursday"
    if wd==4:
        week_day="Friday"
    if wd==5:
        week_day="Saturday"
    if wd==6:
        week_day="Sunday"
    return week_day

def str_from_datetime(date):
    return date.strftime("%y/%m/%d %H:%M")
def timestamp_from_date(date):
    return datetime.timestamp(date)
# def utcfromtimestamp(timestamp): 
#     return datetime.utcfromtimestamp(timestamp) 

# def date_from_timestamp(timestamp):
#     return datetime.fromtimestamp(timestamp)
# def get_now_timestamp():
#     return timestamp_from_date(datetime.now())



# def datetime_from_str(datetime_str):
#     """2012-11-01T04:16:13-0400"""
#     t = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
#     return t
    #dt = datetime(2021, 9, 21, 12, 50, 56 , tzinfo=ZoneInfo("America/Los_Angeles"))
#

