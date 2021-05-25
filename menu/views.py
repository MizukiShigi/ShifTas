from django.shortcuts import render

# Create your views here.
class Login(LoginView):
    template_name = 'mysite/auth.html'

    def form_valid(self, form):
        messages.success(self.request, 'ログイン完了')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'ログインエラー')
        return super().form_invalid(form)