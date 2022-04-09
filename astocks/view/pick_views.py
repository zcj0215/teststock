from django.shortcuts import render,get_object_or_404,redirect
from astocks.forms import StockChooseForm
from django.views.generic import UpdateView, ListView
from django.views import View
from ..models import StockChoose
from boards.models import Board
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

class StockChooseListView(ListView):
    model = StockChoose
    context_object_name = 'chooses'
    template_name = 'pickstock/home.html'
    
class ByDateListView(View):
    def get(self,request):
       return HttpResponse("OK") 
   
@method_decorator(login_required, name='dispatch')    
class EditStockChooseView(UpdateView):
    model = StockChoose
    form_class = StockChooseForm
    template_name = 'pickstock/pickstock_edit.html'
    pk_url_kwarg = 'id'
    context_object_name = 'stockchoose'

    def form_valid(self, form):
        stockchoose = form.save(commit=False)
        stockchoose.boards.clear()
        stockchoose.save()
         
        formboards = self.request.POST.getlist('boards')
        print(formboards)
        for bid in formboards:
            board = get_object_or_404(Board, pk=bid) 
            if board:
                stockchoose.boards.add(board)         
            
        stockchoose.save()
        return redirect('astocks:home')

@method_decorator(login_required, name='dispatch')    
class DeleteStockChooseView(View):
    def get(self,request,id):
        
       pick = get_object_or_404(StockChoose, pk=id)
       print("name:"+pick.name) 
       if pick:
           return render(request, 'pickstock/stockchoose_confirm_delete.html', {'obj': pick })
       else:
           return redirect('astocks:home')
       
    def post(self,request,id):
        id = request.POST.get("id") 
        pick = get_object_or_404(StockChoose, pk=id)
        pick.boards.clear()
        pick.save()
        pick.delete()
        return redirect('astocks:home')