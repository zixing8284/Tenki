
import sublime
import sublime_plugin
import subprocess


# turn on/off radio
popo = None
# if quit radio
leave = None
# if new tab
v = None
# if start OpenMyRadio
sign = None


class OpenMyRadio(sublime_plugin.WindowCommand):
    TENKI_SETTING_FILE = 'Tenki.sublime-settings'
    RADIO_LIST = None

    def run(self):
        global v
        global sign
        if not popo and not sign:
            sign = True
            v = self.window.new_file()
            self.window.focus_view(v)
            global leave
            leave = v.id()
            v.set_scratch(True)
            v.set_name("Sublime Radio")
            v.run_command('insert', {'characters': '不要关闭此页面，然后打开一个调频'})
            v.set_read_only(True)

        self.RADIO_LIST = sublime.load_settings(
            self.TENKI_SETTING_FILE).get('radio_list')
        self.window.show_quick_panel(
            [self.RADIO_LIST[index][0]
                for index in range(len(self.RADIO_LIST))],
            self.on_done,
            sublime.KEEP_OPEN_ON_FOCUS_LOST)

    def on_done(self, index):
        if index == -1:
            return
        Listen(sublime_plugin.WindowCommand).run()


class Listen(sublime_plugin.WindowCommand):

    def run(self):
        global popo
        global v
        if not popo:
            if not sign:
                v = self.window.new_file()
                self.window.focus_view(v)
                global leave
                leave = v.id()
                # we dont need to save
                v.set_scratch(True)
                v.set_name("Sublime Radio")
                v.run_command('insert', {'characters': '不要关闭此页面，你最喜欢的调频播放中'})
                # it cant be edited
                v.set_read_only(True)
            try:
                popo = subprocess.Popen(
                    "ffplay -loglevel quiet \
                    -nodisp http://live.xmcdn.com/live/1065/64.m3u8")
                # Do not display CMD window
                # st = subprocess.STARTUPINFO
                # st.dwFlags = subprocess.STARTF_USESHOWWINDOW
                # st.wShowWindow = subprocess.SW_HIDE
                # popo = subprocess.Popen("ffplay -loglevel quiet -nodisp \
                #       http://live.xmcdn.com/live/12/64.m3u8", \
                #       stdin=subprocess.PIPE,stdout=subprocess.PIPE, \
                #       stderr=subprocess.PIPE,startupinfo=st)
            except Exception:
                print("something wrong here")
        elif leave:
            v.set_read_only(False)
            v.run_command('insert', {'characters': '\n已经打开一个调频'})
            v.set_read_only(True)
            print("已经打开一个调频")


class Stop(sublime_plugin.WindowCommand):
    def run(self):
        global popo
        if popo:
            popo.terminate()
            popo = None
            # v = None
        else:
            pass


class Quit(sublime_plugin.EventListener):
    def on_close(self, view):
        if view.id() == leave:
            print(leave)
            print(view.id())
            Stop(sublime_plugin.WindowCommand).run()
            global v
            global sign
            v = None
            sign = None
            print(popo)
        else:
            pass
