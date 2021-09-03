from time import localtime, sleep
import datetime


class Alarm:
    timer_active = False
    on_alarm = None
    alarm_time = None

    def __init__(self, alarm_struct_time, on_alarm):
        if not callable(on_alarm):
            raise TypeError(on_alarm)
        if not isinstance(alarm_struct_time, datetime.datetime):
            raise TypeError('alarm_struct_time must be datetime.datetime')

        self.on_alarm = on_alarm
        self.alarm_time = alarm_struct_time

    def run(self):
        """
        Синхронно запускает цикл таймера. TODO: Сделать его асинхронным, чтобы в отдельном потоке без ожидания запускался
        """
        print('Timer started')

        def ticking():
            while self.timer_active:
                if is_alarm_time():
                    self.on_alarm()
                    sleep(60)
                sleep(1)

        def is_alarm_time():
            loc = localtime()
            dt = self.alarm_time
            return loc.tm_hour == dt.hour and loc.tm_min == dt.minute

        if not self.timer_active:
            self.timer_active = True
            ticking()

    def stop(self):
        self.timer_active = False


if __name__ == '__main__':
    alarm_time = datetime.datetime(2021, 1, 1, hour=9, minute=36)


    def print_alarm():
        print('alarm!')


    al = Alarm(alarm_time, print_alarm)
    al.run()
    input('до тех пор, пока run синхронен, вы никогда не увидите этот текст')
