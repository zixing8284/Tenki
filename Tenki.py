import sublime
import sublime_plugin
import urllib.request
from datetime import datetime
from .rajio import Switching

# todo: clickable? in the status bar
# todo: display selectable in status bar

TENKI_SETTING_FILE = 'Tenki.sublime-settings'


# show weather in status bar
class Weather:

    @staticmethod
    def get_weather():
        _city = sublime.load_settings(TENKI_SETTING_FILE).get('city')
        with urllib.request.urlopen(
                'http://wttr.in/{}?format=3'.format(_city)) as f:
            data = f.read().decode('utf-8')
            data = data.strip()
        return data


class Tenki(sublime_plugin.EventListener):
    _status = None

    def on_activated_async(self, view):
        self.display_weather(view)

    def update_status(self):
        self._status = Weather.get_weather()

    def display_weather(self, view):
        if self._status is not None:
            view.set_status('Tenki', "{}{},{}".format(
                Time.get_time(), self._status, Switching.data))
            # return True
        elif self._status is None:
            self.update_status()
            view.set_status('Tenki', "{}{},{}".format(
                Time.get_time(), self._status, Switching.data))
        else:
            sublime.status_message('Tenki', "nothing here")
            # return False
        # sublime.set_timeout(
        #     lambda: self.display_weather(view), 1000)
        sublime.set_timeout_async(
            lambda: self.display_weather(view), 1000)


class Time:

    @staticmethod
    def get_time():
        _time = sublime.load_settings(TENKI_SETTING_FILE).get('time', True)
        if _time:
            time = datetime.now().strftime("%H:%M:%S") + ","
        else:
            # time = ""
            time = ""
        return time

# 無駄ね
# class Gannbare(sublime_plugin.EventListener):
#     def on_activated(self, view):
#         sublime.status_message("make today a happy day !")
