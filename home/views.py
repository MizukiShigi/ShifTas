from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from staff.models import Staff
from django.contrib.auth import login

# Create your views here.
def guest_login(request):
    guest_user = User.objects.get(username='guest')
    login(request, guest_user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('home')

class Login(LoginView):
    template_name = 'snipets/auth.html'

    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

class HomeView(TemplateView):
    template_name = 'snipets/home.html'

    def get(self, request):
        login_user = Staff.objects.get(staff=request.user)
        print(login_user)
        context = {'user':login_user}
        return render(self.request, self.template_name, context)