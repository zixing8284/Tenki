import sublime
import sublime_plugin
import subprocess

TENKI_SETTING_FILE = 'Tenki.sublime-settings'


class Switching(sublime_plugin.EventListener):
    nigeru = None
    hitname_go = None
    hitfm_go = None
    radio_list = None

    def on_activated_async(self, view):
        my_favorite = sublime.load_settings(
            TENKI_SETTING_FILE).get('favorite')
        Switching.hitname_go = tuple(my_favorite)[0]
        Switching.hitfm_go = tuple(my_favorite.values())[0]
        Switching.radio_list = sublime.load_settings(
            TENKI_SETTING_FILE).get('radio_list')


class ListenCommand(sublime_plugin.WindowCommand):
    init = False
    v = None
    popo = None

    def init_new_file(self):
        return self.window.new_file()

    def turn_on(self, url):
        self.popo = subprocess.Popen(
            "ffplay -loglevel quiet \
            -nodisp " + url)

    def turn_off(self):
        self.popo.terminate()

    def run(self, hitfm=None, hitname=None, selfie=True, inital=True):
        if not self.init:
            self.v = self.init_new_file()
            self.window.focus_view(self.v)
            # 页面被关闭时记得重置它
            self.init = True
            Switching.nigeru = self.v.id()
            # new tab name
            self.v.set_name("ST网络广播")
            # no need store new tab
            self.v.set_scratch(True)

        if selfie:
            hitfm = Switching.hitfm_go
            print(Switching.hitfm_go)
            print(hitfm)
            hitname = Switching.hitname_go
        try:
            self.turn_on(hitfm)
        except Exception as e:
            print(e)
            print("something wrong here")


class OpenMyRadioCommand(sublime_plugin.WindowCommand):

    def run(self):
        pass


class StopCommand(sublime_plugin.WindowCommand):
    def run(self):
        pass


class Quit(sublime_plugin.EventListener):
    def on_close(self, view):
        if view.id() == Switching.nigeru:
            StopCommand(sublime_plugin.WindowCommand).run()
            ListenCommand.init = False
        else:
            pass
