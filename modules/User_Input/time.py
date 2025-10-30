import logging
from modules.User_Input import date_helper

log = logging.getLogger(__name__)
class Time:
    def __init__(self, config):
        self.config=config
        
        self.timezone= self.config["report"]["timezone"]
        self.past_days=self.config["report"]["past_days"]
        self.past_hours=self.config["report"]["past_hours"]

        self._dates=self._get_dates()
        self.start_date=self._dates["start_date"]
        self.end_date=self._dates["end_date"]
 
        self.days=(self.end_date-self.start_date).days
        self.utc_str_1=self._dates["utc_str_1"]
        self.utc_str_2=self._dates["utc_str_2"]
        self.start_date_str=self._dates["start_date_str"]
        self.end_date_str=self._dates["end_date_str"]
        
    def _get_dates(self):
        end_date=date_helper.get_now_date(self.timezone)
        if self.config["report"]["end_time"]["now"]==False:
            year=self.config["report"]["end_time"]["year"]
            month=self.config["report"]["end_time"]["month"]
            day=self.config["report"]["end_time"]["day"]
            hour=self.config["report"]["end_time"]["hour"]
            end_date=date_helper.get_date(year, month, day, hour, 0, 0, self.timezone)
        end_date_str=date_helper.str_from_datetime(end_date)
        end_date_utc= date_helper.convert_to_utc(end_date)
        utc_str_2 = end_date_utc.isoformat()[:-6]+'Z'
        
        past_days=self.config["report"]["past_days"]
        past_hours=self.config["report"]["past_hours"]


        start_date=date_helper.subtract_time(end_date, past_days, past_hours, 0)

        start_date_str=date_helper.str_from_datetime(start_date)
        start_date_utc= date_helper.convert_to_utc(start_date)
        
        """'2021-10-29T04:15:00.281Z'"""
        utc_str_1 = start_date_utc.isoformat()[:-6]+'Z'
        return {"start_date":start_date, "end_date": end_date, "start_date_str":start_date_str, "end_date_str": end_date_str, "utc_str_1":utc_str_1, "utc_str_2":utc_str_2}
    