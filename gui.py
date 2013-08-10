import wx
import wx.lib.agw.gradientbutton as GB
from pomodoro import *

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Pomodoro", 
                                   size=(200,200))
 
        panel = wx.Panel(self, wx.ID_ANY)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.Center()

        self.initialize_timers()
        
        self.timer_label = wx.StaticText(panel, wx.ID_ANY)
        font = wx.Font(40, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.timer_label.SetFont(font)

        self.start_btn = GB.GradientButton(panel, wx.ID_ANY, label="Start")
        self.start_btn.Bind(wx.EVT_BUTTON, self.on_start)

        self.cancel_btn = GB.GradientButton(panel, wx.ID_ANY, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)
        
        sizer.Add(self.timer_label, flag = wx.ALL, border=10)
        
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.start_btn, flag=wx.ALL, border=5)
        hsizer.Add(self.cancel_btn, flag=wx.ALL, border=5) 
        sizer.Add(hsizer)

        panel.SetSizer(sizer, wx.ALL)

        self.set_defaults()

    def initialize_timers(self):
        self.pomodoro_timer = Pomodoro(self)
        self.Bind(wx.EVT_TIMER, self.update, self.pomodoro_timer)

    def on_start(self, event):
        btnLabel = self.start_btn.GetLabel()
        if btnLabel == "Start":
            self.pomodoro_timer.Start(1000)
            self.start_btn.SetLabel("Pause")
        else:
            self.pomodoro_timer.Stop()
            self.start_btn.SetLabel("Start")

    def on_pomodoro_completed(self):
        self.pomodoro_timer.Stop()
        self.pomodoro_timer.mark_as_complete()
        self.pomodoro_timer.reset()
        self.set_defaults()
        self.start_break()

    def start_break(self):
        self.pomodoro_timer.Start()

    def set_defaults(self):
        self.start_btn.SetLabel("Start")
        self.timer_label.SetLabel(self.pomodoro_timer.formatted_time_left()) 
        self.Refresh()

    def on_cancel(self, event):
        self.pomodoro_timer.reset()        
        self.pomodoro_timer.Stop()
        self.start_btn.SetLabel("Start")        
        self.set_defaults()
        self.Refresh()

    def update_pomodoro(self):
        self.timer_label.SetLabel(self.pomodoro_timer.formatted_time_left()) 
        
    def update(self, event):
        if self.pomodoro_timer.is_complete():
            self.on_pomodoro_completed()
        else:
            self.pomodoro_timer.decrement_one_sec()
            self.update_pomodoro()

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MainFrame().Show()
    app.MainLoop()
