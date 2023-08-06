import threading
import time


def _test(name, value1, value2):
    print("thread {} working".format(name))
    time.sleep(1)
    value1 *= 5
    value2 *= 2
    return value1, value2


class MyThread (threading.Thread):
    THREAD_LOCK = threading.Lock()

    def __init__(self, function, *argv):
        threading.Thread.__init__(self)
        self.function = function
        self.args = argv
        self.rtn = None

    def run(self):
        MyThread.THREAD_LOCK.acquire()
        self.rtn = self.function(*self.args)
        MyThread.THREAD_LOCK.release()


def _main():
    thread1 = MyThread(_test, 'one', 1, 2)
    thread2 = MyThread(_test, 'two', 2, 3)
    thread1.start()
    thread2.start()
    print('main working')
    thread1.join()
    thread2.join()
    print(thread1.rtn[0], thread1.rtn[1])
    print(thread2.rtn)
    print ("Exiting Main Thread")

if __name__ == '__main__':
    _main()
