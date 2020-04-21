import sublime
import sublime_plugin
import urllib.request


TENKI_SETTING_FILE = 'Tenki.sublime-settings'


class Tenki(sublime_plugin.EventListener):
    _status = None

    def on_activated(self, view):
        self.display_weather(view)

    def update_status(self):
        self._status = "今日の天気：" + Weather().get_weather()

    def display_weather(self, view):
        if self._status is not None:
            view.set_status('Tenki', self._status)
            return True
        elif self._status is None:
            self.update_status()
            view.set_status('Tenki', self._status)
        else:
            sublime.status_message('Tenki', "nothing here")
            return False


class Weather:

    _city = None

    def get_weather(self):
        self._city = sublime.load_settings(TENKI_SETTING_FILE).get('city')
        with urllib.request.urlopen('http://wttr.in/{}?format=3'.format(self._city)) as f:
            data = f.read().decode('utf-8')
            data = data.strip()
        return data


# 無駄ね
class Gannbare(sublime_plugin.EventListener):
    def on_activated(self, view):
        sublime.status_message("make today a happy day !")
