from xml.sax import parseString
from celery.schedules import crontab
from teststock.celery import app
from .views import enter, turnover
import time

app.conf.beat_schedule = {
    # Executes every afternoon at 15:30 p.m.
    'doenter-every-afternoon': {
        'task': 'doenter',
        'schedule': crontab(hour=15, minute=40),
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
    for i in range(0,4717,200):
        if(i+200>4717):
           result = enter(i,4717,start,end)
           print(str(i)+'-'+'4717:'+result)
        else:
           result = enter(i,i+200,start,end)
           print(str(i)+'-'+str(i+200)+':'+result)
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
    for i in range(0,2585,200):
        if(i+200>2585):
           result = turnover(i,2585,start,end)
           print(str(i)+'-'+'2585:'+result)
        else:
           result = turnover(i,i+200,start,end)
           print(str(i)+'-'+str(i+200)+':'+result)
        time.sleep(10)
        
    for i in range(2591,4635,200):
        if(i+200>4635):
           result = turnover(i,4635,start,end)
           print(str(i)+'-'+'4635:'+result)
        else:
           result = turnover(i,i+200,start,end)
           print(str(i)+'-'+str(i+200)+':'+result)
        time.sleep(10)