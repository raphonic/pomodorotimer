import wx
import wx.lib.agw.gradientbutton as GB
import wx.media
import os.path
from pomodoro import *

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Pomodoro Timer", 
                                   size=(320,300))
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.Center()
        self.initialize_timers()
        self.initialize_timer_label()
        self.initialize_buttons()
        self.initialize_status_bar()
        self.initialize_media_player()
        self.set_sizers()
        self.set_defaults()

    def initialize_timers(self):
        self.pomodoro_timer = Pomodoro(self)
        self.break_timer = Break(self)
        self.current_timer = self.pomodoro_timer
        
    def initialize_timer_label(self):
        self.timer_label_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.timer_label = wx.StaticText(self.panel, wx.ID_ANY)
        font = wx.Font(50, wx.DECORATIVE, wx.BOLD, wx.NORMAL)
        self.timer_label.SetFont(font)

    def initialize_buttons(self):
        self.start_btn = GB.GradientButton(self.panel, wx.ID_ANY, label="Start")
        self.start_btn.Bind(wx.EVT_BUTTON, self.on_start)
        self.cancel_btn = GB.GradientButton(self.panel, wx.ID_ANY, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

    def set_sizers(self):
        self.timer_label_sizer.Add((5,5),1)
        self.timer_label_sizer.Add(self.timer_label, 3, wx.TOP, 25)
        self.timer_label_sizer.Add((5,5),1)
        self.sizer.Add(self.timer_label_sizer)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add((0,0), 10)        
        hsizer.Add(self.start_btn, 5, flag=wx.TOP, border=75)
        hsizer.Add((0,0), 1)
        hsizer.Add(self.cancel_btn,5, flag=wx.TOP, border=75)                
        hsizer.Add((0,0), 3)
        self.sizer.Add(hsizer)
        self.panel.SetSizer(self.sizer) 

    def initialize_status_bar(self):
        self.status_bar = self.CreateStatusBar()
        
    def on_start(self, event):
        btnLabel = self.start_btn.GetLabel()
        if btnLabel == "Start":
            self.pomodoro_timer.Start(1000)
            self.start_btn.SetLabel("Pause")
        else:
            self.pomodoro_timer.Stop()
            self.start_btn.SetLabel("Start")

    def set_defaults(self):
        self.start_btn.SetLabel("Start")
        self.timer_label.SetLabel(self.current_timer.formatted_time_left())
        self.status_bar.SetStatusText("")
        self.Refresh()

    def on_cancel(self, event):
        self.pomodoro_timer.reset()        
        self.start_btn.SetLabel("Start")        
        self.set_defaults()
        self.Refresh()

    def initialize_media_player(self):
        self.media_player = wx.media.MediaCtrl(self)
        path = os.path.dirname(os.path.abspath(__file__)) + "/sounds/alarm-clock.wav"
        self.media_player.Load(path)

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MainFrame().Show()
    app.MainLoop()
