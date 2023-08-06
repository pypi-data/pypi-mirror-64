from thompcoutils.test_utils import assert_test


class CronTimeException(Exception):
    pass


class CronTime:

    def __init__(self, day_of_week=0, month=0, day_of_month=0, hour=0, minute=0):
        self.day_of_week = day_of_week
        self.month = month
        self.day_of_month = day_of_month
        self.hour = hour
        self.minute = minute

    def __str__(self):
        return CronTime.strfcrontime(self, '%w %d %m %H %M')

    # allowed characters are:
    # %w single digit weekday (0=Sunday)
    # %d two digit day of the month
    # %m two digit month
    # %H two digit hour
    # %M two digit minute
    def strfpcrontime(source_string, format_string):
        cron_time = CronTime()
        j = 0
        i = 0
        for r in range(0, len(format_string)):
            if i > len(format_string) - 1:
                break
            if format_string[i] == '%':
                fmt = format_string[i+1]
                if fmt == 'w':
                    cron_time.day_of_week = int(source_string[j:j+1])
                    i += 1
                elif fmt == 'm':
                    cron_time.month = int(source_string[j:j+2])
                elif fmt == 'd':
                    cron_time.day_of_month = int(source_string[j:j+2])
                elif fmt == 'H':
                    cron_time.hour = int(source_string[j:j+2])
                elif fmt == 'M':
                    cron_time.minute = int(source_string[j:j+2])
                else:
                    raise CronTimeException("%{} not recognised as a CronTime format".format(fmt))
            i += 1
            j += 1
        return cron_time

    def strfcrontime(self, format_string):
        str = ''
        i = 0
        for y in range(0, len(format_string)):
            if i > len(format_string) -1:
                break
            if format_string[i] == '%':
                fmt = format_string[i+1]
                if fmt == 'w':
                    str += '{:1d}'.format(self.day_of_week)
                elif fmt == 'm':
                    str += '{:02d}'.format(self.month)
                elif fmt == 'd':
                    str += '{:02d}'.format(self.day_of_month)
                elif fmt == 'H':
                    str += '{:02d}'.format(self.hour)
                elif fmt == 'M':
                    str += '{:02d}'.format(self.minute)
                else:
                    raise CronTimeException("%{} not recognised as a CronTime format".format(fmt))
                i += 1
            else:
                str += format_string[i]
            i += 1
        return str


def _test_crontime():
    format_string = '%w %d %m %H %M'
    source_string = '1 02 03 04 05'
    cron_time = CronTime.strfpcrontime(source_string, format_string)
    assert_test(cron_time.day_of_week == 1)
    assert_test(cron_time.day_of_month == 2)
    assert_test(cron_time.month == 3)
    assert_test(cron_time.hour == 4)
    assert_test(cron_time.minute == 5)
    print(cron_time)
    str = cron_time.strfcrontime(format_string)
    assert_test(str == source_string)


if __name__ == "__main__":
    _test_crontime()