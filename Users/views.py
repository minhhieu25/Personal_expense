from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterFrom
from .models import CustomUser
# Create your views here.
class AuthView(View):
    def get(self, request):
        # nếu đăng nhập rồi thì không cần đăng nhập nữa
        if request.user.is_authenticated:
            return redirect('finances:transaction')
        
        return render(request, "users/login.html", {
                'login_form': LoginForm(),
                'register_form': RegisterFrom(),
            }
        )
    
    def post(self, request):
        form_type = request.POST.get('form_type')

        login_form = LoginForm()
        register_form = RegisterFrom()

        if form_type == "login":
            login_form = LoginForm(request.POST)

            if login_form.is_valid():
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                remember_me = login_form.cleaned_data["remember_me"]

                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    if remember_me:
                        request.session.set_expiry(60*60*24*30) # 30 ngày
                    else:
                        request.session.set_expiry(0) # hết khi đóng trình duyệt
                    return redirect("finances:transaction")
                else:
                    login_form.add_error(None, "Tên đăng nhập hoặc mật khẩu không đúng!")

        elif form_type == "register":
            register_form = RegisterFrom(request.POST)

            if register_form.is_valid():
                register_form.save()
                return redirect("users:login")
            else:
                print(f"Forms errors: {register_form.errors}")
        
        return render(request, "users/login.html", {
            "login_form": login_form,
            "register_form": register_form,
            "active_tab": form_type,
        })
    
  
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("users:login")
    

        

        