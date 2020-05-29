import sublime
import sublime_plugin
import urllib.request
from datetime import datetime
from .rajio import Switching

# todo: clickable? in the status bar
# todo: display selectable in status bar **args

TENKI_SETTING_FILE = 'Tenki.sublime-settings'

settings = sublime.load_settings(TENKI_SETTING_FILE)

time = settings.get('time', True)

tenki = settings.get('tenki', True)

radio = settings.get('radio', True)

# array_list = [x for x in [time, tenki, radio] if x and True]
array_list = [time, tenki, radio]
print(array_list)


class Time:

    @staticmethod
    def get_time():
        _time = sublime.load_settings(TENKI_SETTING_FILE).get('time', True)
        if _time:
            show_time = datetime.now().strftime("%H:%M:%S")
        else:
            # time = ""
            show_time = ""
        return show_time


# get weather information
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

    def get_status(self):
        new_array = [Time.get_time(), self._status, Switching.data]
        bad_array = []
        for index, item in enumerate(array_list):
            if array_list[index] is True:
                bad_array.append(new_array[index])
        # print(bad_array)
        bad_array_str = ','.join(bad_array)
        # print(bad_array_str)
        return bad_array_str

    def on_activated_async(self, view):
        self.display_weather(view)

    def update_status(self):
        self._status = Weather.get_weather()

    def display_weather(self, view):

        if any(array_list):
            if self._status is not None:
                # view.set_status('Tenki', "{}{},{}".format(
                #     Time.get_time(), self._status, Switching.data))
                view.set_status('Tenki', self.get_status())
                # return True
            elif self._status is None:
                self.update_status()
                # view.set_status('Tenki', array_list)
                # view.set_status('Tenki', "{}{},{}".format(
                #     Time.get_time(), self._status, Switching.data))
                view.set_status('Tenki', self.get_status())
            else:
                sublime.status_message('Tenki', "nothing here")
                # return False
            # sublime.set_timeout(
            #     lambda: self.display_weather(view), 1000)
            if time is not False:
                sublime.set_timeout_async(
                    lambda: self.display_weather(view), 1000)
        else:
            pass


# 無駄ね
# class Gannbare(sublime_plugin.EventListener):
#     def on_activated(self, view):
#         sublime.status_message("make today a happy day !")
