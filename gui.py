import wx
import wx.lib.agw.gradientbutton as GB
from pomodoro import *

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Pomodoro", 
                                   size=(200,200))
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.Center()
        self.initialize_timers()
        self.initialize_timer_label()
        self.initialize_buttons()
        self.set_sizers()
        self.set_defaults()

    def initialize_timers(self):
        self.pomodoro_timer = Pomodoro(self)
        self.break_timer = Break(self)
        self.current_timer = self.pomodoro_timer
        
    def initialize_timer_label(self):
        self.timer_label = wx.StaticText(self.panel, wx.ID_ANY)
        font = wx.Font(40, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        self.timer_label.SetFont(font)

    def initialize_buttons(self):
        self.start_btn = GB.GradientButton(self.panel, wx.ID_ANY, label="Start")
        self.start_btn.Bind(wx.EVT_BUTTON, self.on_start)
        self.cancel_btn = GB.GradientButton(self.panel, wx.ID_ANY, label="Cancel")
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

    def set_sizers(self):
        self.sizer.Add(self.timer_label, flag = wx.ALL, border=10)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.start_btn, flag=wx.ALL, border=5)
        hsizer.Add(self.cancel_btn, flag=wx.ALL, border=5) 
        self.sizer.Add(hsizer)
        self.panel.SetSizer(self.sizer, wx.ALL)
        
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
        self.Refresh()

    def on_cancel(self, event):
        self.pomodoro_timer.reset()        
        self.start_btn.SetLabel("Start")        
        self.set_defaults()
        self.Refresh()

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MainFrame().Show()
    app.MainLoop()
