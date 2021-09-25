from datetime import timedelta, datetime

from utiltask2 import conference_timing


class Conference(conference_timing):
    conf_id = 0

    def __init__(self):
        
        # getting the talks for conference and also other testinputs
        
        super(Conference, self).__init__()
        Conference.conf_id += 1
        self.conf_talks = {}
        self.conftalk_list = Conference.conf_readinput()

     
    def conf_readinput():
        '''

        :return: This is to return the input from the text file
        '''
        
        __talks = {}
        talk_lines = []
        try:
            talk_lines = [line.strip() for line in open('input1.txt')]
        except FileNotFoundError as e:
            print('Wrong File', e)
        for rd_line in talk_lines:
            title, minutes = rd_line.rsplit(maxsplit=1)
            try:
                minutes = int(minutes[:-3])
            # getting the value error
            except ValueError:
                minutes = 5
            __talks[rd_line] = minutes
        return __talks

    def conf_talks2(self, st_time, end_time):
        
        '''

        :param st_time: start of the talk
        :param end_time: end of talk
        :return: getting the time for conference tals
        '''
        
        start = timedelta(hours=st_time)
        for key, value in list(self.conftalk_list.items()):
            prev = start + timedelta(minutes=int(value))
            if prev <= timedelta(hours=end_time):
                self.conf_talks[(datetime.min + start).strftime('%I:%M %p')] = key
                self.conftalk_list.popitem()
                start += timedelta(minutes=int(value))
        return self.conf_talks

    def getting_output(self):
        
        """

        :return:gets the lunch, id, and other events for conference
        """
        
        while not len(self.conftalk_list) is 0:
            print('Track %s' % Conference.conf_id)
            self.conf_out2(9, 12)
            print('%s  %s' % (self.conf_lunch, 'Lunch'))
            self.conf_out2(13, 17)
            print('%s  %s' % (self.conf_end, 'Networking Event'))
            Conference.conf_id += 1

    def conf_out2(self, start, end):
        """

        :param start: start time
        :param end: end time
        :return:  other parameters except the lunch,id etc
        """
        
        for time, title in sorted(self.conf_talks2(start, end).items()):
            print(time, '', title)
        # clear previous entries
        self.conf_talks.clear()


if __name__ == '__main__':
    obj = Conference()
    obj.getting_output()
