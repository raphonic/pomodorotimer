import wx

class TimeDuration(wx.Timer):
    Duration = 0
    
    def __init__(self, parent):
        wx.Timer.__init__(self,parent)
        self.completed = False
        self.time_left = self.Duration

    def decrement_one_sec(self):
        self.time_left -= 1

    def reset(self):
        self.time_left = self.Duration

    def mark_as_complete(self):
        self.completed = True

    def is_complete(self):
        return self.time_left == 0

    def formatted_time_left(self):
        hours = self.time_left / 60
        mins = self.time_left % 60
        if mins == 0: 
            return str(hours) + ":" + str(mins) + "0"
        else:
            return str(hours) + ":" + str(mins)

class Pomodoro(TimeDuration):
    Duration = 3

class Break(TimeDuration):
    Duration = 2

    
