from tkinter import EXCEPTION
from django.http import Http404, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count

from .forms import NewTopicForm, PostForm, CodeForm
from .models import Board, Topic, Post, BoardType
from astocks.models import Stocks,StockList,Stocksz,Stockszc,Stocksh,Stockshk,Stockbj,Stocksector
from django.views.generic import UpdateView, ListView
from django.utils import timezone
import time
import json
import pandas as pd
import talib

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'
    paginate_by = 20

class ByTypeBoardListView(ListView):
    model = Stocksector
    context_object_name = 'boards'
    template_name = 'homebytype.html'
    paginate_by = 20
   
    def get_context_data(self, **kwargs):
        kwargs['type'] = self.type
        return super().get_context_data(**kwargs)    

    def get_queryset(self):
        self.type = get_object_or_404(BoardType, pk=self.kwargs.get('type_pk'))
        bds = Board.objects.filter(type = self.type)
        date =  Stocksector.objects.last().date
        names = []
        for board in bds:
            names.append(board.name)
        queryset = Stocksector.objects.filter(name__in = names,date=date).order_by('-growth')
        return queryset
    
    
class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset

class StockListView(ListView):
    model = Stocks
    context_object_name = 'stockses'
    template_name = 'stocks.html'
    paginate_by = 5
    

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        kwargs['data'] = self.data
        kwargs['form'] = self.form
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, name=self.kwargs.get('name'))
        self.form = CodeForm()
        jsonlist = []
        key = self.kwargs.get('name') + time.strftime("%Y-%m-%d", time.localtime())
        
        if self.request.session.get(key):
            self.data = json.dumps(jsonlist)
        else:
            self.request.session[key] = key  
            try:
                data = Stocksector.objects.all().filter(name=self.board.name).order_by('-date')
                for row in data:
                  dict = {}
                  dict["name"] = self.board.name
                  dict["code"] = str(row.code)
                  dict["open"] = str(row.open)
                  dict["close"] = str(row.close)
                  dict["low"] = str(row.low)
                  dict["high"] = str(row.high)
                  dict["vol"] = str(row.volume)
                  dict["trade_date"] = str(row.date)  
                  jsonlist.append(dict) 
               
            except EXCEPTION:
                pass
        
            self.data = json.dumps(jsonlist)
        
        queryset = Stocks.objects.filter(boards__name__in = [self.board.name]).order_by('-growth')
        return queryset

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('-created_at')
        return queryset
    
@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('boards:topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('boards:topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

def stock_detail(request, board_name, stock_name):
    stock = get_object_or_404(Stocks, name=stock_name)
    boards = stock.boards
    if board_name == stock.name:
        board_name = stock.blockname
    stock = get_object_or_404(StockList, symbol=stock.code)
  
    start = request.GET.get("start")
    end =  request.GET.get("end")
    if start == None or end == None:
        start = stock.list_date[:4]+'-'+stock.list_date[4:6]+'-'+stock.list_date[6:]
        end = time.strftime("%Y-%m-%d", time.localtime())
        
    code = stock.ts_code[:6]
    flag = stock.ts_code[7:]
    name = stock.name
    jsonlist = []
    blocklist = []
   
    try:
        data = Stocksector.objects.all().filter(name=board_name).order_by('-date')
        
        for row in data:
            dict = {}
            dict["name"] = board_name 
            dict["code"] = str(row.code)
            dict["open"] = str(row.open)
            dict["close"] = str(row.close)
            dict["low"] = str(row.low)
            dict["high"] = str(row.high)
            dict["vol"] = str(row.volume)
            dict["trade_date"] = str(row.date)  
            blocklist.append(dict)         
    except EXCEPTION:
        pass
    blocklist.reverse()
    mybpd = pd.DataFrame(blocklist,columns=['name','code','open','close','low','high','vol','trade_date'])
    #bcci = round(calculate_CCI(mybpd), 2).tolist()
    bsignals = generate_signals(mybpd)
    
    key = code + time.strftime("%Y-%m-%d", time.localtime())
    
    if request.session.get(key):
        return render(request, 'stock.html', {'stock':stock,'boards':boards,"data": json.dumps(jsonlist),"bdata":json.dumps(blocklist),"signals":{},"bsignals":bsignals.to_json()})
    else:
        request.session[key] = key
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
                      dict["capital_inflow"] = str(row.capital_inflow)
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
                      dict["capital_inflow"] = str(row.capital_inflow)  
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
                      dict["capital_inflow"] = str(row.capital_inflow)  
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
                      dict["capital_inflow"] = str(row.capital_inflow)  
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
                  dict["capital_inflow"] = str(row.capital_inflow)  
                  jsonlist.append(dict) 
                    
          except EXCEPTION:
              pass
        jsonlist.reverse()
        
        mypd = pd.DataFrame(jsonlist,columns=['name','code','open','close','low','high','vol','change','pct_chg','amount','pre_close','turnover','trade_date','capital_inflow'])
        # cci = round(calculate_CCI(mypd), 2).tolist() 
        signals = generate_signals(mypd)
             
        return render(request, 'stock.html', {'stock':stock,'boards':boards,"data": json.dumps(jsonlist),"bdata":json.dumps(blocklist),"signals":signals.to_json(),"bsignals":bsignals.to_json()})
    
def calculate_CCI(data,n=14):
    
    cci = talib.CCI(data["high"].astype(float),data["low"].astype(float),data["close"].astype(float),timeperiod=n)
 
    return  cci

def calculate_KDJ(data,n=9,m1=3,m2=3):
    
    k,d = talib.STOCH(data["high"].astype(float),data["low"].astype(float),data["close"].astype(float),fastk_period=n,slowk_period=m1,slowd_period=m2)
    j = 3*d - 2*k
    
    return  k, d, j

def generate_signals(data):
    
    k, d, j = calculate_KDJ(data)
    cci1 = round(calculate_CCI(data), 2)
    cci2 = round(calculate_CCI(data,89), 2)
    
    signals = pd.DataFrame(index=data.index)
    signals['k'] = k
    signals['d'] = d
    signals['j'] = j
    signals['cci1'] = cci1
    signals['cci2'] = cci2
    #生成买入和卖出信号
    signals['buy_signal'] = ((signals['k'] < 20) & (signals['d'] < 20) & (signals['cci1'] < -100)).astype(int)
    signals['sell_signal'] = ((signals['k'] > 80) & (signals['d'] > 80) & (signals['cci1'] > 100)).astype(int)
    signals['ybuy_signal'] = ((signals['cci2'] < 300) & (signals['cci2'].shift(-1).fillna(method="ffill") > 300)).astype(int)
    signals['ysell_signal'] = ((signals['cci2'] > 300) & (signals['cci2'].shift(-1).fillna(method="ffill") < 300)).astype(int)
    
    return signals
    
    
def query(request):
    if request.method == 'POST':
        stock_code = request.POST['code']
        blockname = request.POST['blockname']
        try:
            stock = get_object_or_404(Stocks, code=stock_code, boards__name__in = [blockname])
            data = {"result":"success","stockname":stock.name}
            return JsonResponse({"data": json.dumps(data)})
        except Http404:
            data = {"result":"fail"}
            return JsonResponse({"data": json.dumps(data)})  
def blockquery(request):
    if request.method == 'POST':
        blockname = request.POST['blockname']
        try:
            board = get_object_or_404(Board, name=blockname)
            data = {"result":"success"}
            return JsonResponse({"data": json.dumps(data)})
        except Http404:
            data = {"result":"fail"}
            return JsonResponse({"data": json.dumps(data)})  

@method_decorator(login_required, name='dispatch')    
class TopicUpdateView(UpdateView):
    model = Topic
    form_class = NewTopicForm
    template_name = 'edit_topic.html'
    pk_url_kwarg = 'topic_pk'
    context_object_name = 'topic'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(starter=self.request.user)

    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.last_updated = timezone.now()
        topic.save()
        post = Post.objects.create(
            message=form.cleaned_data.get('message'),
            topic=topic,
            created_by=self.request.user
        )
        return redirect('boards:board_topics', pk=topic.board.pk) 


@method_decorator(login_required, name='dispatch')    
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('boards:topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)
