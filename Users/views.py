from django.core.mail import message
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import *
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

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
                email = login_form.cleaned_data["email"]
                password = login_form.cleaned_data["password"]
                remember_me = login_form.cleaned_data["remember_me"]

                # 1. Tự tìm người dùng bằng email
                user_obj = CustomUser.objects.filter(email=email).first()
                
                # 2. Đưa username của user đó cho Django kiểm tra password
                user = None
                if user_obj:
                    user = authenticate(request, username=user_obj.username, password=password)

                if user is None and user_obj is not None:
                    # User tồn tại nhưng authenticate thất bại
                    if not user_obj.is_active:
                        login_form.add_error(None, "Vui lòng xác thực email trước khi đăng nhập!")
                    else:
                        login_form.add_error(None, "Mật khẩu không đúng!")
                elif user is None:
                    login_form.add_error(None, "Email không tồn tại!")
                else:
                    # Đăng nhập thành công
                    login(request, user)
                    if remember_me:
                        request.session.set_expiry(60*60*24*30) # 30 ngày
                    else:
                        request.session.set_expiry(0) # hết khi đóng trình duyệt
                    return redirect("finances:transaction")
        elif form_type == "register":
            register_form = RegisterFrom(request.POST)

            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.is_active = False
                user.is_verified = False
                user.save()

                # Gửi email xác thực
                send_verification_email(user, request)
                
                return render(request, 'users/login.html', {
                    'login_form': login_form,
                    'register_form': register_form,
                    'message': 'Kiểm tra email để xác thực tài khoản!',
                })
            # else:
            #     print(f"Forms errors: {register_form.errors}")
        
        return render(request, "users/login.html", {
            "login_form": login_form,
            "register_form": register_form,
            "active_tab": form_type,
        })
    
  
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("users:login")
    

@method_decorator(never_cache, name='dispatch') # khong cho phép trình duyệt lưu cache 
class CustomUserView(LoginRequiredMixin, View):
    login_url = 'users:login' # Nếu chưa đăng nhập thì phải về trang login
    def get(self, request):
        customuser = CustomUser.objects.filter(id=request.user.id)
        return render(request, "users/customuser.html", { 'customuser': customuser,})

@method_decorator(never_cache, name='dispatch')
class CustomUserEditView(LoginRequiredMixin, View):
    login_url = 'users:login'
    def get(self, request):
        form = CustomUserForm(instance=request.user)
        return render(request, "users/edit_user.html", {'form': form,})

    def post(self, request):
        form = CustomUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:customuser")
        
        return render(request, 'users/edit_user.html', {'form': form})
    

@method_decorator(never_cache, name='dispatch')
class PasswordChangeView(LoginRequiredMixin, View):
    login_url = 'users:login'
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


# Xác thực email
class VerifyEmailView(View):
    def get(self, request, token):
        from .models import EmailVerification

        try:
            verification = EmailVerification.objects.get(token=token)
        except EmailVerification.DoesNotExist:
            return render(request, "users/verify_email.html", {
                'message': 'Link xác thực không hợp lệ!'
            })

        if verification.is_expired():
            return render(request, "users/verify_email.html", {
                'message': 'Link xác thực đã hết hạn!'
            })

        # kích hoạt tài khoản
        user = verification.user
        user.is_active = True
        user.is_verified = True
        user.save()

        # Xóa token sau khi xác thực
        verification.delete()

        return render(request, 'users/verify_success.html', {
            'message': 'Xác thực thành công! bạn có thể đăng nhập.'
        })