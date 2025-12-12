from apscheduler.schedulers.background import BackgroundScheduler
from .models import  Reminders,db
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta


def init_scheduler(app):
    scheduler = BackgroundScheduler()

    def check_reminders():
        with app.app_context():
            now=datetime.utcnow()
            print("Checking reminders at:", now)

            due_reminders=Reminders.query.filter(Reminders.schedule_time<=now).all()
            print("Found:", len(due_reminders), "due reminders")  
                     
            for reminder in due_reminders:
                print(f"Reminder triggered:{reminder.message} at {now}")

                if reminder.repeat_frequency :
                    freq=reminder.repeat_frequency.lower()

                    if freq == "daily":
                        reminder.schedule_time+= timedelta(days=1)
                    elif freq=="weekly":
                        reminder.schedule_time+=timedelta(weeks=1)
                    elif freq=="monthly":
                        reminder.schedule_time+=relativedelta(months=1)   
                    elif freq=="every 2 months":
                        reminder.schedule_time+=relativedelta(months=2)
                    elif freq=="yearly":
                        reminder.schedule_time+=relativedelta(years=1)
                     
                    
                    else:# if custom
                        try:
                            minutes=int(freq)
                            reminder.schedule_time+=timedelta(minutes=minutes)
                        except ValueError:
                            reminder.repeat_frequency = "none"
                else:
                    reminder.schedule_time = now + timedelta(days=365*100)

            db.session.commit()

    scheduler.add_job(check_reminders,"interval",seconds=20)
    scheduler.start()
