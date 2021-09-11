from PySide6.QtCore import QTimer

import pyperclip

class ClipboardWatcher():
    def __init__(self,timer:QTimer, predicate, callback, pause=1000):
        self.timer = timer
        self.timer.setInterval(pause)
        self.timer.timeout.connect(self.run)
        self._predicate = predicate
        self._callback = callback
        self._pause = pause
        self._stopping = False
        self.recent_value=''

    def run(self):       
        tmp_value = pyperclip.paste()
        if tmp_value != self.recent_value:
            self.recent_value = tmp_value
            if self._predicate(self.recent_value):
                self._callback(self.recent_value)

    def stop(self):
        self.timer.stop()

    def start(self):
        self.timer.start(self._pause)