from tkinter import EXCEPTION
from django.shortcuts import render,get_object_or_404,redirect
from astocks.forms import StockLimitupForm
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.views import View
from ..models import StockLimitup,LimitupType,Stocks,StockList,Stocksz,Stockszc,Stocksh,Stockshk,Stockbj
from boards.models import Board
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.utils import timezone
import time
import json

class StockChooseListView(ListView):
    model = StockLimitup
    context_object_name = 'limitups'
    template_name = 'pickstock/limitup.html'
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
        self.limitups = StockLimitup.objects.all()
        queryset = self.limitups.order_by('-pick_date')
        return queryset
    
def byDateListView(request):
    by = request.GET.get('by') 
    if by:
        limitups = StockLimitup.objects.all().filter(limitup_date=by)
    
        return render(request, 'pickstock/limitup_list_by_date.html', {'limitups': limitups,'by':by })
    else:
        return redirect('astocks:limitup')

def byTypeListView(request):
    bytype = request.GET.get('bytype') 
    type = get_object_or_404(LimitupType, pk=bytype) 
    limitups = StockLimitup.objects.filter(types__name__in = [type.name]).order_by('-pick_date')
    
    return render(request, 'pickstock/limitup_list_by_type.html', {'limitups': limitups,'limituptype':type })

def byBoardListView(request):
    byboard = request.GET.get('byboard') 
    board = get_object_or_404(Board, pk=byboard) 
    limitups = StockLimitup.objects.filter(boards__name__in = [board.name]).order_by('-pick_date')
   
    return render(request, 'pickstock/limitup_list_by_board.html', {'limitups': limitups,'limitupboard':board})
        
@method_decorator(login_required, name='dispatch')    
class EditStockChooseView(UpdateView):
    model = StockLimitup
    form_class = StockLimitupForm
    template_name = 'pickstock/limitup_edit.html'
    pk_url_kwarg = 'id'
    context_object_name = 'stocklimitup'
    
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
        stocklimitup = form.save(commit=False)
        stocklimitup.types.clear()
        stocklimitup.boards.clear()
        stocklimitup.save()
         
        formtypes = self.request.POST.getlist('types')
        for tid in formtypes:
            type = get_object_or_404(LimitupType, pk=tid) 
            if type:
                stocklimitup.types.add(type) 
         
        formboards = self.request.POST.getlist('boards')
        for bid in formboards:
            board = get_object_or_404(Board, pk=bid) 
            if board:
                stocklimitup.boards.add(board)         
            
        stocklimitup.save()
        
        keys = self.request.session.keys()
        
        if 'by' in keys and self.request.session['by']:
            del self.request.session['by']
            pick_date_str = str(stocklimitup.pick_date)
            return redirect('/astocks/limitup_date?by='+pick_date_str)
        if 'bytype' in keys and self.request.session['bytype']:
            bytype = self.request.session['bytype']
            del self.request.session['bytype']
            return redirect('/astocks/limitup_type?bytype='+bytype)
        if 'byboard' in keys and self.request.session['byboard']:
            byboard = self.request.session['byboard']
            del self.request.session['byboard']
            return redirect('/astocks/limitup_board?byboard='+byboard)
        
        else:    
            return redirect('astocks:limitup')
        
@method_decorator(login_required, name='dispatch')    
class DeleteStockChooseView(View):
    def get(self,request,id):
        
       pick = get_object_or_404(StockLimitup, pk=id)
       if pick:    
          return render(request, 'pickstock/limitup_confirm_delete.html', {'obj': pick })
       else:
          return redirect('astocks:limitup')
       
    def post(self,request,id):
        id = request.POST.get("id") 
        pick = get_object_or_404(StockLimitup, pk=id)
        pick.boards.clear()
        pick.save()
        pick_date_str = str(pick.pick_date)
        pick.delete()
        
        return redirect('astocks:limitup')        

@method_decorator(login_required, name='dispatch')    
class DeleteStockChooseByDateView(View):
    def get(self,request,id,by):
        
       pick = get_object_or_404(StockLimitup, pk=id)
       if pick:
            if by:
               request.session['by'] = by        
            return render(request, 'pickstock/limitup_confirm_delete.html', {'obj': pick })
       else:
           return redirect('astocks:limitup')
       
    def post(self,request,id,by):
        id = request.POST.get("id") 
        pick = get_object_or_404(StockLimitup, pk=id)
        pick.boards.clear()
        pick.save()
        pick_date_str = str(pick.pick_date)
        pick.delete()
        
        keys = request.session.keys()
        if 'by' in keys and request.session['by']:
            del request.session['by']
            return redirect('/astocks/limitup_date?by='+pick_date_str)
        else:    
            return redirect('astocks:limitup')
        
@method_decorator(login_required, name='dispatch')    
class DeleteStockChooseByTypeView(View):
    def get(self,request,id,bytype):
        
       pick = get_object_or_404(StockLimitup, pk=id)
       if pick:
            if bytype:
               request.session['bytype'] = bytype        
            return render(request, 'pickstock/limitup_confirm_delete.html', {'obj': pick })
       else:
           return redirect('astocks:limitup')
       
    def post(self,request,id,bytype):
        id = request.POST.get("id") 
        pick = get_object_or_404(StockLimitup, pk=id)
        pick.boards.clear()
        pick.types.clear()
        pick.save()
        pick.delete()
        
        keys = request.session.keys()
        if 'bytype' in keys and request.session['bytype']:
            del request.session['bytype']
            return redirect('/astocks/limitup_type?bytype='+bytype)
        else:    
            return redirect('astocks:limitup')
        
@method_decorator(login_required, name='dispatch')    
class DeleteStockChooseByBoardView(View):
    def get(self,request,id,byboard):
        
       pick = get_object_or_404(StockLimitup, pk=id)
       if pick:
            if byboard:
               request.session['byboard'] = byboard        
            return render(request, 'pickstock/limitup_confirm_delete.html', {'obj': pick })
       else:
           return redirect('astocks:limitup')
       
    def post(self,request,id,byboard):
        id = request.POST.get("id") 
        pick = get_object_or_404(StockLimitup, pk=id)
        pick.boards.clear()
        pick.types.clear()
        pick.save()
        pick.delete()
        
        keys = request.session.keys()
        if 'byboard' in keys and request.session['byboard']:
            del request.session['byboard']
            return redirect('/astocks/limitup_board?byboard='+byboard)
        else:    
            return redirect('astocks:limitup')
        
def limitup_detail(request, name):
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
