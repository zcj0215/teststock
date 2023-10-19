from django.shortcuts import render,get_object_or_404,redirect
from astocks.forms import StockChooseForm
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.views import View
from ..models import StockChoose,ChooseType
from boards.models import Board
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


class StockChooseListView(ListView):
    model = StockChoose
    context_object_name = 'chooses'
    template_name = 'pickstock/home.html'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        keys = self.request.session.keys()
        if 'by' in keys and self.request.session['by']:
            del self.request.session['by']
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        self.chooses = StockChoose.objects.all()
        queryset = self.chooses.order_by('-pick_date')
        return queryset
    
def byDateListView(request):
    by = request.GET.get('by') 
    chooses = StockChoose.objects.all().filter(pick_date=by)
    
    return render(request, 'pickstock/pickstock_list_by_date.html', {'chooses': chooses })

def byTypeListView(request):
    by = request.GET.get('by') 
    type = get_object_or_404(ChooseType, pk=by) 
    chooses = StockChoose.objects.filter(types__name__in = [type.name]).order_by('-pick_date')
   
    return render(request, 'pickstock/pickstock_list_by_type.html', {'chooses': chooses })
        
@method_decorator(login_required, name='dispatch')    
class EditStockChooseView(UpdateView):
    model = StockChoose
    form_class = StockChooseForm
    template_name = 'pickstock/pickstock_edit.html'
    pk_url_kwarg = 'id'
    context_object_name = 'stockchoose'
    
    def get_context_data(self, **kwargs):
        by = self.kwargs.get('by')
        if by:
            self.request.session['by'] = by
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
        pick.save()
        pick_date_str = str(pick.pick_date)
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
        pick.save()
        pick_date_str = str(pick.pick_date)
        pick.delete()
        
        keys = request.session.keys()
        if 'by' in keys and request.session['by']:
            del request.session['by']
            return redirect('/astocks/choose_date?by='+pick_date_str)
        else:    
            return redirect('astocks:home')
         