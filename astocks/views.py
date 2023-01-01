from tkinter import EXCEPTION
from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import tushare as ts
import json
import time
from .models import StockList,Stocksz,Stockszc,Stocksh,Stockshk,Stockbj,Stockme
from django.http import Http404
from django.db.models import Q
from .forms import DateDataForm

ts.set_token('357f92fd3836f2d018d20b9b840897abb3e5c9a62e17895b413e05fe')
# 49da118be4e9b270b7ed565edf8fa70ba43f1d02fa33965d1fab3c38
pro = ts.pro_api()

def query(request):
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    column_list = []
    
    for row in data:
        column_list.append(row)
     
    jsonlist = []
    for index in range(data[column_list[0]].size):
        dict = {}
        for row in data:
            dict[row] = data[row][index]
        jsonlist.append(dict)
        try:
           stock = get_object_or_404(StockList, symbol=dict['symbol'])
        except Http404:
            stock = StockList.objects.create(
                ts_code = dict['ts_code'],
                symbol = dict['symbol'],
                name = dict['name'],
                area = dict['area'],
                industry = dict['industry'],
                list_date = dict['list_date']
            )
       
        
    return HttpResponse(json.dumps(jsonlist))

def single(request,code='000001',):
    stock = get_object_or_404(StockList, symbol=code)
   
    start = request.GET.get("start")
    end =  request.GET.get("end")
    if start == None or end == None:
        start = stock.list_date[:4]+'-'+stock.list_date[4:6]+'-'+stock.list_date[6:]
        end = time.strftime("%Y-%m-%d", time.localtime())
        
    code = stock.ts_code[:6]
    flag = stock.ts_code[7:]
    name = stock.name
    
    jsonlist = []
    # data = pro.daily(ts_code=stock.ts_code, start_date=start, end_date=end)
    if flag == 'SZ':
        if code[:2] == '30':  
          try:
              data = Stockszc.objects.all().filter(date__range=[start,end],code=code).order_by('-date')
              
              for row in data:
                  dict = {}
                  dict["name"] = name
                  dict["code"] = str(row.code)
                  dict["open"] = str(row.open)
                  dict["close"] = str(row.close)
                  dict["low"] = str(row.low)
                  dict["high"] = str(row.high)
                  dict["vol"] = str(row.volume)
                  dict["change"] = str(row.price_change)
                  dict["pct_chg"] = str(row.p_change)
                  dict["amount"] = str(row.amount)
                  dict["pre_close"] = str(row.pre_close)
                  dict["turnover"] = str(row.turnover)
                  dict["trade_date"] = str(row.date)
                    
                  jsonlist.append(dict) 
               
          except EXCEPTION:
              pass
        else:
          try:
              data = Stocksz.objects.all().filter(date__range=[start,end],code=code).order_by('-date')
              
              for row in data:
                  dict = {}
                  dict["name"] = name
                  dict["code"] = str(row.code)
                  dict["open"] = str(row.open)
                  dict["close"] = str(row.close)
                  dict["low"] = str(row.low)
                  dict["high"] = str(row.high)
                  dict["vol"] = str(row.volume)
                  dict["change"] = str(row.price_change)
                  dict["pct_chg"] = str(row.p_change)
                  dict["amount"] = str(row.amount)
                  dict["pre_close"] = str(row.pre_close)
                  dict["turnover"] = str(row.turnover)
                  dict["trade_date"] = str(row.date)
                    
                  jsonlist.append(dict) 
              
          except EXCEPTION:
              pass
    elif flag == 'SH':
        if code[:2] == '68':  
          try:
              data = Stockshk.objects.all().filter(date__range=[start,end],code=code).order_by('-date')
              
              for row in data:
                  dict = {}
                  dict["name"] = name
                  dict["code"] = str(row.code)
                  dict["open"] = str(row.open)
                  dict["close"] = str(row.close)
                  dict["low"] = str(row.low)
                  dict["high"] = str(row.high)
                  dict["vol"] = str(row.volume)
                  dict["change"] = str(row.price_change)
                  dict["pct_chg"] = str(row.p_change)
                  dict["amount"] = str(row.amount)
                  dict["pre_close"] = str(row.pre_close)
                  dict["turnover"] = str(row.turnover)
                  dict["trade_date"] = str(row.date)
                    
                  jsonlist.append(dict) 
              
                     
          except EXCEPTION:
              pass
        else:     
          try:
              data = Stocksh.objects.all().filter(date__range=[start,end],code=code).order_by('-date')
              
              for row in data:
                  dict = {}
                  dict["name"] = name
                  dict["code"] = str(row.code)
                  dict["open"] = str(row.open)
                  dict["close"] = str(row.close)
                  dict["low"] = str(row.low)
                  dict["high"] = str(row.high)
                  dict["vol"] = str(row.volume)
                  dict["change"] = str(row.price_change)
                  dict["pct_chg"] = str(row.p_change)
                  dict["amount"] = str(row.amount)
                  dict["pre_close"] = str(row.pre_close)
                  dict["turnover"] = str(row.turnover)
                  dict["trade_date"] = str(row.date)
                    
                  jsonlist.append(dict) 
                    
          except EXCEPTION:
              pass
    elif flag == 'BJ':
          try:
              data = Stockbj.objects.all().filter(date__range=[start,end],code=code).order_by('-date')
              
              for row in data:
                  dict = {}
                  dict["name"] = name
                  dict["code"] = str(row.code)
                  dict["open"] = str(row.open)
                  dict["close"] = str(row.close)
                  dict["low"] = str(row.low)
                  dict["high"] = str(row.high)
                  dict["vol"] = str(row.volume)
                  dict["change"] = str(row.price_change)
                  dict["pct_chg"] = str(row.p_change)
                  dict["amount"] = str(row.amount)
                  dict["pre_close"] = str(row.pre_close)
                  dict["turnover"] = str(row.turnover)
                  dict["trade_date"] = str(row.date)
                    
                  jsonlist.append(dict) 
                    
          except EXCEPTION:
              pass
               
    return HttpResponse(json.dumps(jsonlist))

def enter(beginindex,endindex,start,end):
    for index in range(int(beginindex),int(endindex)):
         stock = get_object_or_404(StockList, pk=index+1)
         code = stock.ts_code[:6]
         flag = stock.ts_code[7:]
         #start = time.strftime("%Y%m%d", time.localtime())
         #end = time.strftime("%Y%m%d", time.localtime())
          
         data = pro.daily(ts_code=stock.ts_code, start_date=start, end_date=end)
         
         column_list = []
    
         for row in data:
            column_list.append(row)
            
         jsonlist = []
         for index in range(data[column_list[0]].size):
             dict = {}
             for row in data:
                dict[row] = data[row][index]
            
             mydate = dict['trade_date'][:4]+'-'+dict['trade_date'][4:6]+'-'+dict['trade_date'][6:]
             if flag == 'SZ':
               if code[:2] == '30':  
                 try:
                    stock = get_object_or_404(Stockszc, code=code,date=mydate)
                 except Http404:
                    stock = Stockszc.objects.create(
                       code = code,
                       open = dict['open'],
                       high = dict['high'],
                       close = dict['close'],
                       pre_close = dict['pre_close'],
                       low = dict['low'],
                       volume = dict['vol'],
                       amount = dict['amount']*1000/10000,
                       price_change = dict['change'],
                       p_change = dict['pct_chg'],
                       date = mydate
                    )
               else:
                 try:
                    stock = get_object_or_404(Stocksz, code=code,date=mydate)
                 except Http404:
                    stock = Stocksz.objects.create(
                       code = code,
                       open = dict['open'],
                       high = dict['high'],
                       close = dict['close'],
                       pre_close = dict['pre_close'],
                       low = dict['low'],
                       volume = dict['vol'],
                       amount = dict['amount']*1000/10000,
                       price_change = dict['change'],
                       p_change = dict['pct_chg'],
                       date = mydate
                    )
             elif flag == 'SH':
               if code[:2] == '68':  
                 try:
                    stock = get_object_or_404(Stockshk, code=code,date=mydate)
                 except Http404:
                   stock = Stockshk.objects.create(
                      code = code,
                      open = dict['open'],
                      high = dict['high'],
                      close = dict['close'],
                      pre_close = dict['pre_close'],
                      low = dict['low'],
                      volume = dict['vol'],
                      amount = dict['amount']*1000/10000,
                      price_change = dict['change'],
                      p_change = dict['pct_chg'],
                      date = mydate
                   ) 
               else:     
                 try:
                    stock = get_object_or_404(Stocksh, code=code,date=mydate)
                 except Http404:
                    stock = Stocksh.objects.create(
                       code = code,
                       open = dict['open'],
                       high = dict['high'],
                       close = dict['close'],
                       pre_close = dict['pre_close'],
                       low = dict['low'],
                       volume = dict['vol'],
                       amount = dict['amount']*1000/10000,
                       price_change = dict['change'],
                       p_change = dict['pct_chg'],
                       date = mydate
                    )
             elif flag == 'BJ':
               try:
                 stock = get_object_or_404(Stockbj, code=code,date=mydate)
               except Http404:
                 stock = Stockbj.objects.create(
                   code = code,
                   open = dict['open'],
                   high = dict['high'],
                   close = dict['close'],
                   pre_close = dict['pre_close'],
                   low = dict['low'],
                   volume = dict['vol'],
                   amount = dict['amount']*1000/10000,
                   price_change = dict['change'],
                   p_change = dict['pct_chg'],
                   date = mydate
                 )
    return 'OK'
 
def selectStock(page, limit):
    queryset = StockList.objects.all().order_by('symbol')
    paginator = Paginator(queryset, limit)
    
    try:
        stocks = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        stocks = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        stocks = paginator.page(paginator.num_pages)
    
    
    jsonlist = []
    for stock in stocks:
        
        dict = {}
        dict["area"] = stock.area
        dict["industry"] = stock.industry
        dict["list_date"] = stock.list_date
        dict["name"] = stock.name
        dict["symbol"] = stock.symbol
        dict["ts_code"] = stock.ts_code
        jsonlist.append(dict)
    return jsonlist
 
def stockList(request):
    start = request.GET.get('page', 1)  
    limit = request.GET.get('page', 20)
 
    jsonlist = selectStock(start, limit)
  
    return HttpResponse(json.dumps(jsonlist))

def search(request):
    like = request.GET.get("like")
    jsonlist = []
    if like != None:
        stocks = StockList.objects.all().filter(Q(name__contains=like)|Q(industry__contains=like)|Q(symbol__contains=like))
         
        for stock in stocks:
           dict = {}
           dict["area"] = stock.area
           dict["industry"] = stock.industry
           dict["list_date"] = stock.list_date
           dict["name"] = stock.name
           dict["symbol"] = stock.symbol
           dict["ts_code"] = stock.ts_code
           jsonlist.append(dict)
           
    return HttpResponse(json.dumps(jsonlist))

def turnover(beginindex,endindex,trade_date1,trade_date2):

    for index in range(int(beginindex),int(endindex)):
    # for index in range(4618, 4635):
         stock = get_object_or_404(StockList, pk=index+1)
         code = stock.ts_code[:6]
         flag = stock.ts_code[7:]
         # trade_date1 = stock.list_date
         
         data = ts.get_hist_data(code, start=trade_date1, end=trade_date2)
         
         column_list = []
    
         for row in data:
            column_list.append(row)
            
         jsonlist = []
         for index in range(data[column_list[0]].size):
             dict = {}
             for row in data:
                dict[row] = data[row][index]
            
             mydate = data.index[index]
             if flag == 'SZ':
               if code[:2] == '30':  
                 try:
                    stock = get_object_or_404(Stockszc, code=code,date=mydate)
                    stock.turnover = dict['turnover']
                    stock.save()
                 except Http404:
                    pass
               else:
                 try:
                    stock = get_object_or_404(Stocksz, code=code,date=mydate)
                    stock.turnover = dict['turnover']
                    stock.save()
                 except Http404:
                    pass
             elif flag == 'SH':
               if code[:2] == '68':  
                 try:
                    stock = get_object_or_404(Stockshk, code=code,date=mydate)
                    stock.turnover = dict['turnover']
                    stock.save()
                 except Http404:
                   pass
               else:     
                 try:
                    stock = get_object_or_404(Stocksh, code=code,date=mydate)
                    stock.turnover = dict['turnover']
                    stock.save()
                 except Http404:
                   pass
             elif flag == 'BJ':
               try:
                 stock = get_object_or_404(Stockbj, code=code,date=mydate)
                 stock.turnover = dict['turnover']
                 stock.save()
               except Http404:
                 pass
    return 'OK'
  
def handledd(request):
    if request.method == 'POST':
        form = DateDataForm(request.POST)
        if form.is_valid():
            beginindex = request.POST['beginindex']
            endindex = request.POST['endindex']
            begindate = request.POST['begindate']
            enddate = request.POST['enddate']
            enter(beginindex,endindex,begindate,enddate)
            return redirect('home')
    else:
        form = DateDataForm()
    return render(request, 'handledd.html', {'form': form})
  
def handleto(request):
    if request.method == 'POST':
        form = DateDataForm(request.POST)
        if form.is_valid():
            beginindex = request.POST['beginindex']
            endindex = request.POST['endindex']
            begindate = request.POST['begindate']
            enddate = request.POST['enddate']
            turnover(beginindex,endindex,begindate,enddate)
            return redirect('home')
    else:
        form = DateDataForm()
    return render(request, 'handledd.html', {'form': form})


