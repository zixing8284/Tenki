import sublime
import sublime_plugin
import urllib.request


class Tenki(sublime_plugin.EventListener):
    _status = None

    def on_activated(self, view):
        self.display_weather(view)

    def update_status(self):
        self._status = Weather().get_weather()

    def display_weather(self, view):
        if self._status is None:
            self.update_status()
        if self._status is not None:
            view.set_status('Tenki', self._status)


class Weather():
    def get_weather(self):
        with urllib.request.urlopen('http://wttr.in/Zhengzhou?format=3') as f:
            data = f.read().decode('utf-8')
            data = data.strip()
        return data


# 無駄ね
class Gannbare(sublime_plugin.EventListener):
    def on_activated(self, view):
        sublime.status_message("make today a happy day !")
