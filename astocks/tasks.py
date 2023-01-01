from xml.sax import parseString
from celery.schedules import crontab
from teststock.celery import app
from .views import enter, turnover
import time

app.conf.beat_schedule = {
    # Executes every afternoon at 15:30 p.m.
    'doenter-every-afternoon': {
        'task': 'doenter',
        'schedule': crontab(hour=16, minute=10),
        'args': (),
    },
    'doturnover-every-afternoon':{
        'task':'doturnover',
        'schedule': crontab(hour=17, minute=45),
        'args':()
    }   
}

@app.task(name='doenter')
def doenter():
    start = time.strftime("%Y%m%d", time.localtime())
    end = time.strftime("%Y%m%d", time.localtime())
    for i in range(0,4790,100):
        if(i+100>4790):
           result = enter(i,4790,start,end)
           print(str(i)+'-'+'4790:'+result)
        else:
           result = enter(i,i+100,start,end)
           print(str(i)+'-'+str(i+100)+':'+result)
        time.sleep(60)

@app.task(name='doturnover')
def doturnover():
    ltime = time.localtime()
    start = ''
    if(ltime.tm_mday-1)==0:
        start = str(ltime.tm_year)+'-'+str(ltime.tm_mon)+'-'+str(ltime.tm_mday)
    else:
        start = str(ltime.tm_year)+'-'+str(ltime.tm_mon)+'-'+str(ltime.tm_mday-1)
    end = str(ltime.tm_year)+'-'+str(ltime.tm_mon)+'-'+str(ltime.tm_mday+1)
    for i in range(0,2585,100):
        if(i+100>2585):
           result = turnover(i,2585,start,end)
           print(str(i)+'-'+'2585:'+result)
        else:
           result = turnover(i,i+100,start,end)
           print(str(i)+'-'+str(i+100)+':'+result)
        time.sleep(10)
        
    for i in range(2591,4635,100):
        if(i+100>4635):
           result = turnover(i,4635,start,end)
           print(str(i)+'-'+'4635:'+result)
        else:
           result = turnover(i,i+100,start,end)
           print(str(i)+'-'+str(i+100)+':'+result)
        time.sleep(10)