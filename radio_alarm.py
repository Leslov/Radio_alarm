from datetime import datetime
from sys import argv

from Radio_impl import RadioImpl
from alarm import Alarm


def get_time():
    time_str = argv[1] if len(argv) > 1 else None
    try:
        if not time_str:
            time_str = input('Введите время будильника в формате hh:mm: ')
        time = tuple(int(x) for x in time_str.split(':'))
    except Exception as ex:
        print('Некорректно указано время')
        exit(-1)
    return time


if __name__ == '__main__':
    time = get_time()
    alarm_time = datetime(2021, 1, 1, hour=time[0], minute=time[1])
    radio = RadioImpl()
    alarm = Alarm(alarm_time, radio.play)
    alarm.run()
