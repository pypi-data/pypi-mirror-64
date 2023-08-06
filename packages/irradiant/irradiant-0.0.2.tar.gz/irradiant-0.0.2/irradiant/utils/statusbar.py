import sys
import time
from threading import Thread, Lock
from time import sleep


class StatusBar(Thread):
    def __init__(self, min_refresh_hz=0.5, attach_stdout=True):
        # Superclass stuff
        super().__init__()
        self.setDaemon(True)

        # Params
        self.min_refresh_hz = min_refresh_hz
        self.attach_stdout = attach_stdout
        self._stdout_write = sys.stdout.write
        if self.attach_stdout:
            sys.stdout.write = self.stdout_hook

        self.data = {}
        self.last_print_time = time.time()
        self.last_num_characters = 0
        self.lock = Lock()
        self.stop = False
        self.start()

    def stdout_hook(self, *args, **kwargs):
        orig_str = args[0]
        newline_pos = orig_str.rfind("\n")
        if newline_pos != -1:
            # If there is a newline, print spaces first according to previous status bar length to clear it
            self._stdout_write(orig_str[:newline_pos] + " " * (self.last_num_characters - len(orig_str)) + "\n")

            # Reprint the status bar
            self.last_num_characters = self.print_status_bar()
        else:
            self._stdout_write(orig_str)

    def print_status_bar(self):
        self.lock.acquire()
        num_characters = self._stdout_write(str(self) + "\r")
        sys.stdout.flush()
        self.lock.release()

        return num_characters

    def __repr__(self):
        statusbar = "\u21AA "
        for key, value in self.data.items():
            statusbar += " %s: %s " % (str(key), str(value))
        return statusbar

    def run(self):
        while not self.stop:
            current_time = time.time()

            if current_time - self.last_print_time >= self.min_refresh_hz:
                self.print_status_bar()
                self.last_print_time = current_time

            sleep(self.min_refresh_hz)

    def detach(self):
        self.stop = True
        if self.attach_stdout:
            sys.stdout.write = self._stdout_write
