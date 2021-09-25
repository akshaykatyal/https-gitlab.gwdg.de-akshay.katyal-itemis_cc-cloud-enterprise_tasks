from datetime import timedelta, datetime


class conference_timing:
    def __init__(self):
        
        """The Conference day is divided into the morning,lunch,afternoon,end"""
        
        self.conf_morn = (datetime.min+ timedelta(hours=  9)).strftime('%I:%M %p')
        self.conf_lunch = (datetime.min+ timedelta(hours=12)).strftime('%I:%M %p')
        self.conf_afternoon = (datetime.min+ timedelta(hours=13)).strftime('%I:%M %p')
        self.conf_end = (datetime.min+ timedelta(hours=17)).strftime('%I:%M %p')

