from tkinter import EXCEPTION
from django.shortcuts import render,get_object_or_404,redirect
from astocks.forms import StockChooseForm
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.views import View
from ..models import StockChoose,ChooseType,Stocks,StockList,Stocksz,Stockszc,Stocksh,Stockshk,Stockbj
from boards.models import Board
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.utils import timezone
import time
import json


class StockChooseListView(ListView):
    model = StockChoose
    context_object_name = 'chooses'
    template_name = 'pickstock/home.html'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        keys = self.request.session.keys()
        if 'by' in keys and self.request.session['by']:
            del self.request.session['by']
        if 'bytype' in keys and self.request.session['bytype']:
            del self.request.session['bytype']
        if 'byboard' in keys and self.request.session['byboard']:
            del self.request.session['byboard']
            
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        self.chooses = StockChoose.objects.all()
        queryset = self.chooses.order_by('-pick_date')
        return queryset
    
def byDateListView(request):
    by = request.GET.get('by') 
    chooses = StockChoose.objects.all().filter(pick_date=by)
    
    return render(request, 'pickstock/pickstock_list_by_date.html', {'chooses': chooses, 'by':by })

def byTypeListView(request):
    bytype = request.GET.get('bytype') 
    type = get_object_or_404(ChooseType, pk=bytype) 
    chooses = StockChoose.objects.filter(types__name__in = [type.name]).order_by('-pick_date')
   
    return render(request, 'pickstock/pickstock_list_by_type.html', {'chooses': chooses,'choosetype':type })

def byBoardListView(request):
    byboard = request.GET.get('byboard') 
    board = get_object_or_404(Board, pk=byboard) 
    chooses = StockChoose.objects.filter(boards__name__in = [board.name]).order_by('-pick_date')
   
    return render(request, 'pickstock/pickstock_list_by_board.html', {'chooses': chooses,'chooseboard':board})
        
@method_decorator(login_required, name='dispatch')
class EditStockChooseView(UpdateView):
    model = StockChoose
    form_class = StockChooseForm
    template_name = 'pickstock/pickstock_edit.html'
    pk_url_kwarg = 'id'
    context_object_name = 'stockchoose'
    
    def get_context_data(self, **kwargs):
        by = self.kwargs.get('by')
        bytype = self.kwargs.get('bytype')
        byboard = self.kwargs.get('byboard')
        if by:
            self.request.session['by'] = by
        if bytype:
            self.request.session['bytype'] = bytype
            
        if byboard:
            self.request.session['byboard'] = byboard
            
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        stockchoose = form.save(commit=False)
        stockchoose.types.clear()
        stockchoose.boards.clear()
        stockchoose.save()
        
        formtypes = self.request.POST.getlist('types')
        for tid in formtypes:
            type = get_object_or_404(ChooseType, pk=tid) 
            if type:
                stockchoose.types.add(type)
         
        formboards = self.request.POST.getlist('boards')
        for bid in formboards:
            board = get_object_or_404(Board, pk=bid) 
            if board:
                stockchoose.boards.add(board)         
            
        stockchoose.save()
        
        keys = self.request.session.keys()
        
        if 'by' in keys and self.request.session['by']:
            del self.request.session['by']
            pick_date_str = str(stockchoose.pick_date)
            return redirect('/astocks/choose_date?by='+pick_date_str)
        if 'bytype' in keys and self.request.session['bytype']:
            bytype = self.request.session['bytype']
            del self.request.session['bytype']
            return redirect('/astocks/choose_type?bytype='+bytype)
        if 'byboard' in keys and self.request.session['byboard']:
            byboard = self.request.session['byboard']
            del self.request.session['byboard']
            return redirect('/astocks/choose_board?byboard='+byboard)
        
        else:    
            return redirect('astocks:home')
        
@method_decorator(login_required, name='dispatch')    
class DeleteStockChooseView(View):
    def get(self,request,id):
        
       pick = get_object_or_404(StockChoose, pk=id)
       if pick:    
          return render(request, 'pickstock/stockchoose_confirm_delete.html', {'obj': pick })
       else:
          return redirect('astocks:home')
       
    def post(self,request,id):
        id = request.POST.get("id") 
        pick = get_object_or_404(StockChoose, pk=id)
        pick.boards.clear()
        pick.types.clear()
        pick.save()
        pick.delete()
        
        return redirect('astocks:home')        

@method_decorator(login_required, name='dispatch')    
class DeleteStockChooseByDateView(View):
    def get(self,request,id,by):
        
       pick = get_object_or_404(StockChoose, pk=id)
       if pick:
            if by:
               request.session['by'] = by        
            return render(request, 'pickstock/stockchoose_confirm_delete.html', {'obj': pick })
       else:
           return redirect('astocks:home')
       
    def post(self,request,id,by):
        id = request.POST.get("id") 
        pick = get_object_or_404(StockChoose, pk=id)
        pick.boards.clear()
        pick.types.clear()
        pick.save()
        pick_date_str = str(pick.pick_date)
        pick.delete()
        
        keys = request.session.keys()
        if 'by' in keys and request.session['by']:
            del request.session['by']
            return redirect('/astocks/choose_date?by='+pick_date_str)
        else:    
            return redirect('astocks:home')

@method_decorator(login_required, name='dispatch')    
class DeleteStockChooseByTypeView(View):
    def get(self,request,id,bytype):
        
       pick = get_object_or_404(StockChoose, pk=id)
       if pick:
            if bytype:
               request.session['bytype'] = bytype        
            return render(request, 'pickstock/stockchoose_confirm_delete.html', {'obj': pick })
       else:
           return redirect('astocks:home')
       
    def post(self,request,id,bytype):
        id = request.POST.get("id") 
        pick = get_object_or_404(StockChoose, pk=id)
        pick.boards.clear()
        pick.types.clear()
        pick.save()
        pick.delete()
        
        keys = request.session.keys()
        if 'bytype' in keys and request.session['bytype']:
            del request.session['bytype']
            return redirect('/astocks/choose_type?bytype='+bytype)
        else:    
            return redirect('astocks:home')
        
@method_decorator(login_required, name='dispatch')    
class DeleteStockChooseByBoardView(View):
    def get(self,request,id,byboard):
        
       pick = get_object_or_404(StockChoose, pk=id)
       if pick:
            if byboard:
               request.session['byboard'] = byboard        
            return render(request, 'pickstock/stockchoose_confirm_delete.html', {'obj': pick })
       else:
           return redirect('astocks:home')
       
    def post(self,request,id,byboard):
        id = request.POST.get("id") 
        pick = get_object_or_404(StockChoose, pk=id)
        pick.boards.clear()
        pick.types.clear()
        pick.save()
        pick.delete()
        
        keys = request.session.keys()
        if 'byboard' in keys and request.session['byboard']:
            del request.session['byboard']
            return redirect('/astocks/choose_board?byboard='+byboard)
        else:    
            return redirect('astocks:home')
        
def choose_detail(request, name):
    stock = get_object_or_404(Stocks, name=name)
    boards = stock.boards
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
        
    
    return render(request, 'stock.html', {'stock':stock,'boards':boards,"data": json.dumps(jsonlist)})
