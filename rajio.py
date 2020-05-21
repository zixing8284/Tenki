
import sublime
import sublime_plugin
import subprocess


## todo on_done() 判断正在当前调频时选中当前调频提示输出：正在播放此调频
## todo on_done() 切换调频时播放调频，提示输出
## todo ListenCommand() 正在播放当前时，提示输出：正在播放此调频，从其他调频切换时播放调频，提示输出：正在播放最喜欢的调频


class Switching:
    # turn on/off radio
    popo = None
    # if newtab exists
    leave = None
    # if close tab
    v = None
    # if init newtab
    sign = None


class OpenMyRadioCommand(sublime_plugin.WindowCommand):
    TENKI_SETTING_FILE = 'Tenki.sublime-settings'
    RADIO_LIST = None

    def run(self):
        if not Switching.popo and not Switching.sign:
            Switching.sign = True
            Switching.v = self.window.new_file()
            self.window.focus_view(Switching.v)
            Switching.leave = Switching.v.id()
            Switching.v.set_scratch(True)
            Switching.v.set_name("Sublime Radio")
            Switching.v.run_command(
                'insert', {'characters': '不要关闭此页面，然后打开一个调频'})
            Switching.v.set_read_only(True)

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
        # ListenCommand(sublime_plugin.WindowCommand).run()
        self.window.run_command('listen')


class ListenCommand(sublime_plugin.WindowCommand):

    def run(self):
        if not Switching.popo:
            if not Switching.sign:
                Switching.sign = True
                Switching.v = self.window.new_file()
                self.window.focus_view(Switching.v)
                Switching.leave = Switching.v.id()
                # we dont need to save
                Switching.v.set_scratch(True)
                Switching.v.set_name("Sublime Radio")
                Switching.v.run_command(
                    'insert', {'characters': '不要关闭此页面，你最喜欢的调频播放中'})
                # it should not be editable
                Switching.v.set_read_only(True)
            try:
                Switching.popo = subprocess.Popen(
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
        elif Switching.leave:
            Switching.v.set_read_only(False)
            Switching.v.run_command('insert', {'characters': '\n已经打开一个调频'})
            Switching.v.set_read_only(True)
            print("已经打开一个调频")


class StopCommand(sublime_plugin.WindowCommand):
    def run(self):
        if Switching.popo:
            Switching.popo.terminate()
            Switching.popo = None
        else:
            pass


class Quit(sublime_plugin.EventListener):
    def on_close(self, view):
        if view.id() == Switching.leave:
            StopCommand(sublime_plugin.WindowCommand).run()
            Switching.v = None
            Switching.sign = None
        else:
            pass
