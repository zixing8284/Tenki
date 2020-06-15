import sublime
import sublime_plugin
import subprocess
import platform

TENKI_SETTING_FILE = 'Tenki.sublime-settings'


class Switching(sublime_plugin.EventListener):
    nigeru = None
    hitname_go = None
    hitfm_go = None
    radio_list = None
    popo = None
    status = False

    def on_activated_async(self, view):
        if self.status is False:
            my_favorite = sublime.load_settings(
                TENKI_SETTING_FILE).get('favorite')
            Switching.hitname_go = tuple(my_favorite)[0]
            Switching.hitfm_go = tuple(my_favorite.values())[0]
            Switching.radio_list = sublime.load_settings(
                TENKI_SETTING_FILE).get('radio_list')
            self.status = True
        else:
            pass
        self.show_listening(view)

    def show_listening(self, view):
        if Switching.popo:
            # view.set_status('Tenki', 'Now Playing: ' + ListenCommand.urlname)
            Switching.data = 'Now Playing: {}'.format(ListenCommand.urlname)
        else:
            # view.set_status('Tenki', 'NO Playing')
            Switching.data = 'No Playing'
        return Switching.data


class ListenCommand(sublime_plugin.WindowCommand):
    init = False
    v = None
    popo = None
    url = None
    urlname = None

    def init_new_file(self):
        return self.window.new_file()

    def turn_on(self, url, urlname):
        if platform.system() == 'Windows':
            # DO NOT show CMD window
            # The STARTUPINFO class and following constants are
            # only available on Windows.
            st = subprocess.STARTUPINFO
            st.dwFlags = subprocess.STARTF_USESHOWWINDOW
            st.wShowWindow = subprocess.SW_HIDE
            # self.popo = Switching.popo = subprocess.Popen(
            #     "ffplay -loglevel quiet -nodisp " + url,
            #     stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            #     stderr=subprocess.PIPE, startupinfo=st)
            self.popo = Switching.popo = subprocess.Popen(
                "ffplay -loglevel quiet -nodisp " + url, startupinfo=st)

            # # show CMD window default
            # self.popo = Switching.popo = subprocess.Popen(
            #     "ffplay -loglevel quiet \
            #     -nodisp " + url)

        # Linux
        else:
            self.popo = Switching.popo = subprocess.Popen(
                ['ffplay', '-loglevel', 'quiet', '-nodisp', str(url)])

        self.v.set_read_only(False)
        self.v.run_command(
            'insert',
            {'characters': '正在播放中：' + urlname + '\n'})
        self.v.set_read_only(True)

    def turn_off(self, url, urlname):
        if not Switching.popo:
            self.turn_on(url=url, urlname=urlname)
        else:
            self.v.set_read_only(False)
            # if self.url != url:
            if ListenCommand.url != url:
                self.popo.terminate()
                self.v.run_command(
                    'insert',
                    {'characters': '切换调频\n'})
                self.turn_on(url=url, urlname=urlname)
            else:
                self.v.run_command(
                    'insert',
                    {'characters': '正在播放这个调频\n'})
            self.v.set_read_only(True)

    def run(self, hitfm=None, hitname=None, selfie=True, inital=True):
        # if not ListenCommand.init:
        if not self.init:
            self.v = ListenCommand.v = self.init_new_file()
            self.window.focus_view(self.v)
            # remember to reset this in QuitCommand
            ListenCommand.init = True
            Switching.nigeru = self.v.id()
            # new tab name
            self.v.set_name("ST网络广播")
            # no need store new tab
            self.v.set_scratch(True)
            self.v.run_command(
                'insert',
                {'characters': '不要关闭此页面，然后打开一个调频\n'})
        # if select Listen My favorite radio
        if selfie:
            hitfm = Switching.hitfm_go
            hitname = Switching.hitname_go
        try:
            ListenCommand.urlname = hitname
            self.turn_off(hitfm, hitname)
            # self.url = hitfm
            ListenCommand.url = hitfm
        except Exception as e:
            print(e)
            print("error here")
            self.v.run_command(
                'insert',
                {'characters': 'something\'s wrong\n'})
            pass
        self.v.set_read_only(True)


class OpenMyRadioCommand(sublime_plugin.WindowCommand):

    # def run(self, hitfm=None, hitname=None, selfie=False, inital=True):
    def run(self):
        self.window.show_quick_panel(
            [Switching.radio_list[index][0]
                for index in range(len(Switching.radio_list))],
            self.on_done,
            sublime.KEEP_OPEN_ON_FOCUS_LOST)

    def on_done(self, index):
        if index == -1:
            return
        self.window.run_command(
            'listen',
            {'hitfm': Switching.radio_list[index][1],
             'hitname': Switching.radio_list[index][0],
             'selfie': False})


class StopCommand(sublime_plugin.WindowCommand):

    def run(self):
        if Switching.popo:
            Switching.popo.terminate()
            ListenCommand.v.set_read_only(False)
            ListenCommand.v.run_command(
                'insert',
                {'characters': '停止了播放\n'})
            ListenCommand.v.set_read_only(True)
            Switching.popo = None
            # ListenCommand.url = None
        pass


class Quit(sublime_plugin.EventListener):

    def on_close(self, view):
        if view.id() == Switching.nigeru:
            StopCommand(sublime_plugin.WindowCommand).run()
            ListenCommand.init = False
        else:
            pass
