import wx
import datetime
from time import strptime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
Engine = create_engine('sqlite:///pomodoros.db', echo=False)
Base = declarative_base()

def get_first_day_of_week(date):
    day_of_week = datetime.date(*strptime(str(date), '%Y-%m-%d')[0:3]).weekday()
    start = date - datetime.timedelta(days=day_of_week)
    end = date + datetime.timedelta(days=6 - day_of_week)
    return start,end

class PomodoroLog(Base):
    __tablename__ = "pomodorologs"
 
    id = Column(Integer, primary_key=True)
    completed_at = Column(Date, default=datetime.date.today())

    def __init__(self, completed_at=None):
        if completed_at is not None: self.completed_at = completed_at
        
    @staticmethod
    def get_logs():
        today = Session.query(PomodoroLog).filter(PomodoroLog.completed_at == datetime.date.today()).count()
        start, end = get_first_day_of_week(datetime.date.today())
        this_week = Session.query(PomodoroLog).filter(PomodoroLog.completed_at.between(start, end)).count()
        all_time = Session.query(PomodoroLog).count()
        return [today, this_week, all_time]
    
Base.metadata.create_all(Engine)
SessionMaker = sessionmaker(bind=Engine)
Session = SessionMaker()
 
class TimeDuration(wx.Timer):
    Duration = 0
    
    def __init__(self, parent):
        wx.Timer.__init__(self,parent)
        self.parent = parent
        self.completed = False
        self.time_left = self.Duration
        self.parent.Bind(wx.EVT_TIMER, self.on_update, self)

    def decrement_one_sec(self):
        self.time_left -= 1

    def reset(self):
        self.Stop()
        self.time_left = self.Duration

    def mark_as_complete(self):
        self.completed = True

    def is_complete(self):
        return self.time_left == 0

    def formatted_time_left(self):
        hours = self.time_left / 60
        mins = self.time_left % 60
        fmt_str = str(hours).zfill(2) + ":" + str(mins).zfill(2)
        return fmt_str

    def on_update(self, event):
        if self.is_complete():
            self.on_completed()
        else:
            self.decrement_one_sec()
            self.parent.timer_label.SetLabel(self.formatted_time_left())

    def on_completed(self):
        self.reset()
        self.mark_as_complete()

class Pomodoro(TimeDuration):
    Duration = 25 * 60

    def on_completed(self):
        TimeDuration.on_completed(self)
        self.parent.break_timer.Start()
        self.parent.current_timer = self.parent.break_timer
        self.parent.set_defaults()
        self.parent.status_bar.SetStatusText("Break Time")
        self.parent.media_player.Play()

class Break(TimeDuration):
    Duration = 5 * 60

    def on_completed(self):
        TimeDuration.on_completed(self)
        self.parent.current_timer = self.parent.pomodoro_timer
        self.parent.set_defaults()
        self.parent.media_player.Play()
        Session.add(PomodoroLog())
        Session.commit()
