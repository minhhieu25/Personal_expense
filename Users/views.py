from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin

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
    
class CustomUserView(View):
    def get(self, request):
        customuser = CustomUser.objects.filter(id=request.user.id)
        return render(request, "users/customuser.html", { 'customuser': customuser,})


class CustomUserEditView(View):
    def get(self, request):
        form = CustomUserForm(instance=request.user)
        return render(request, "users/edit_user.html", {'form': form,})

    def post(self, request):
        form = CustomUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:customuser")
        
        return render(request, 'users/edit_user.html', {'form': form})
    

class PasswordChangeView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm()
        
        return render(request, "Users/password_change.html", {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = request.user
            # Kiểm tra mật khẩu hiện tại
            if not user.check_password(form.cleaned_data['old_password']):
                form.add_error('old_password', 'Mật khẩu hiện tại không đúng!')
                return render(request, "Users/password_change.html", {'form': form})
            # Đổi mật khẩu
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            # Đăng nhập lại vì session bị reset sau khi đổi mật khẩu
            login(request, user)
            return redirect('users:customuser')
        return render(request, "users/password_change.html", {'form': form})

        