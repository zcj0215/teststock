from xml.sax import parseString
from celery.schedules import crontab
from teststock.celery import app
from .views import enter
import time

app.conf.beat_schedule = {
    # Executes every afternoon at 15:30 p.m.
    'add-every-afternoon': {
        'task': 'doenter',
        'schedule': crontab(hour=16, minute=1),
        'args': (),
    },
    'test-every-afternoon':{
        'task':'turnover',
        'schedule': crontab(hour=16, minute=1),
        'args':()
    }   
}

@app.task(name='doenter',)
def doenter():
    for i in range(0,4717,200):
        if(i+200>4717):
           result = enter(i,4717,'20220302','20220315')
           print(str(i)+'-'+'4717:'+result)
        else:
           result = enter(i,i+200,'20220302','20220315')
           print(str(i)+'-'+str(i+200)+':'+result)
        time.sleep(60)

@app.task(name='turnover')
def turnover():
    print("ok")