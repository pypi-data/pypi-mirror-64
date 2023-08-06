import threading
import bRusky.sendSMS
import bRusky.sendCALLS
from bRusky.exceptions import TypeError
import time


class threaded_spamer(threading.Thread):
    def __init__(self, number, enable_proxy: bool):
        threading.Thread.__init__(self)
        self.enable_proxy = enable_proxy
        self.number = number

    def spamSMS(self):
        spamer = bRusky.sendSMS.spamer(number=self.number, enable_proxy=self.enable_proxy)
        spamer.start()

    def spamCALLS(self):
        spamer = bRusky.sendCALLS.spamer(number=self.number, enable_proxy=self.enable_proxy, name='Константин')
        spamer.start()

    def run(self):
        thread = threading.Thread(target=self.spamCALLS)
        thread.start()
        while True:
            thread = threading.Thread(target=self.spamSMS)
            thread.start()
            time.sleep(60)


class Rusky:
    def __init__(self, number: str, enable_proxy: bool):
        if type(enable_proxy) == bool and type(number) == str:
            self.proxy = enable_proxy
            self.number = number
        else:
            raise TypeError("Error")

    def start(self):
        thread = threaded_spamer(number=self.number, enable_proxy=self.proxy)
        thread.start()
