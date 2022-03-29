from django.shortcuts import render

# Create your views here.from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Persons
from .forms import SignUpForm, SignInForm, PersonsForm
from astocks.forms import StockChooseForm
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.forms import NON_FIELD_ERRORS

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user
def home(request):
    return redirect('boards:home')   
     
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('boards:home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
     
def login(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
              auth_login(request, user)
              next = request.POST['next']
              if next != '':
                  return redirect(next)
              else:  
                return redirect('boards:home')
            else:
              next = request.POST['next'] 
              form._errors[NON_FIELD_ERRORS] = form.error_class(['请输入正确的用户名和密码。'])
              
    else:
        form = SignInForm()
        if request.GET.get('next') is not None:
          next = request.GET.get('next')
        else:
          next = ''  
        
    return render(request, 'login.html', {'form': form, 'next':next})

@login_required
def new_person(request):
    if request.method == 'POST':
        form = PersonsForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.save()
            return redirect('boards:home')
    else:
        form = PersonsForm()
    return render(request, 'person.html', {'form': form})

@login_required
def new_pick(request):
    if request.method == 'POST':
        form = StockChooseForm(request.POST)
        if form.is_valid():
            pick = form.save(commit=False)
            pick.save()
            return redirect('boards:home')
    else:
        form = StockChooseForm()
    return render(request, 'pickstock.html', {'form': form})