from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from astocks.models import StockList
from .models import Company
from . import models
from .LSTMPredictStock import predic
from .add_companies_to_db import add_company
from .forms import CodeForm
import json
import os
from datetime import datetime as dt
# from apscheduler.scheduler import Scheduler
import pandas as pd

# --------------- MAIN WEB PAGES -----------------------------
def redirect_root(request):
    return redirect('/prediction/pred')

def pred(request):
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            stock_code = request.POST['code']
            again = request.POST['again']
            good = request.POST['good']
            if good != 'on':
                predic.train_model(stock_code)
            else:
               if not predic.isGood(stock_code):
                  return JsonResponse({"data":False }) 
           
            recent_data, predict_data,code,name = get_hist_predict_data(stock_code,again,good)
            data = {"recent_data": recent_data, "predict_data": predict_data,"stock_code": code,"stock_name": name}
            # data['indexs'] = get_stock_index(code)
            return JsonResponse({"data": json.dumps(data)}) 
            # return render(request, "prediction/home.html", {"data": json.dumps(data),'form': form}) 
    else:
        form = CodeForm()
     
    return render(request, 'prediction/prediction.html',{'form': form})


######################################################
#      
#
######################################################
def get_hist_predict_data(stock_code,again,good):
    try:
        company = get_object_or_404(Company, stock_code=stock_code)
    except Http404:
        stock = get_object_or_404(StockList, symbol=stock_code)
        company = Company()
        company.name = stock.name
        company.stock_code = stock_code
        company.save()

    recent_data,predict_data = None,None
    
    if company.historydata_set.count() <= 0:
        history_data = models.HistoryData()
        history_data.company = company
        history_data.set_data(predic.get_hist_data(stock_code=stock_code,recent_day=22))
        history_data.save()
        recent_data = history_data.get_data()
    else:
        all_data = company.historydata_set.all()
        for single in all_data:
            now = dt.now()
            end_date = single.get_data()[-1][0]
            end_date = dt.strptime(end_date,"%Y-%m-%d")
           
            if  (now.date() > end_date.date() or good == 'on'):  # 更新历史数据
                single.set_data(predic.get_hist_data(stock_code, good, recent_day=22))
                single.save()

            recent_data = single.get_data()
            break

    if company.predictdata_set.count() <= 0:
        predict_data = models.PredictData()
        predict_data.company = company
        predict_data.set_data(predic.prediction(stock_code, good, pre_len=5))
        predict_data.save()
        predict_data = predict_data.get_data()
    else:
        all_data = company.predictdata_set.all()
        for single in all_data:
            now = dt.now()
            start_date = dt.strptime(single.start_date,"%Y-%m-%d")
            if (now.date() > start_date.date() or again == 'on' or good == 'on'):  # 更新预测数据
                single.set_data(predic.prediction(stock_code, good, pre_len=5))
                single.save()

            predict_data = single.get_data()
            break

    return recent_data,predict_data,stock_code,company.name


def get_crawl_save_data():
    """
    将10个公司的指标数据爬取并保存到数据库
    """
    # 此处应是从网上爬取数据，并保存为csv文件
    parent_dir = os.path.dirname(__file__)  # "stock_predict/views.py"
    file_dir = os.path.join(parent_dir, "stock_index/")
    for file_name in os.listdir(file_dir):
        file_path =  os.path.join(file_dir, file_name)
        data_frame = pd.read_csv(file_path)
        stock_code = file_name.split('.')[0]
        company = get_object_or_404(Company, stock_code=stock_code)
        for index,row in data_frame.iterrows():
            company.stockindex_set.create(ri_qi=row['ri_qi'],zi_jin=row['zi_jin'],qiang_du=row['qiang_du'],feng_xian=row['feng_xian'],
                zhuan_qiang=row['zhuan_qiang'],chang_yu=row['chang_yu'],jin_zi=row['jin_zi'],zong_he=row['zong_he'])


def get_stock_index(stock_code):
    """
    获取股票的各项指标数据
    """
    company = get_object_or_404(Company, stock_code=stock_code)
    if company.stockindex_set.count() <= 0:
        # 将爬取的数据存入数据库
        get_crawl_save_data()
    # 从数据库获取近三天的数据
    indexs = company.stockindex_set.all().order_by('-ri_qi')[:3].values()
    return list(indexs)

""" sched = Scheduler()
# 定时任务
# @sched.interval_schedule(seconds=2)   # 每2s执行一次
@sched.cron_schedule(hour=0,minute=0)   # 每日凌晨调度一次
def train_models():
    predic.train_all_stock()

sched.start() """
#########################################################################################
#
#
#########################################################################################