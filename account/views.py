from django.http import HttpRequest
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from .forms import LoginForm, OtpLoginForm, CheckOtpForm, AddressCreationForm
import ghasedakpack
from random import randint
from uuid import uuid4


from .models import Otp, User, City, UserAddress

SMS = ghasedakpack.Ghasedak("42e64e967622806110066c9743b25d63169bc079ba0c8bedde43d491c3664360")


class UserRegister(TemplateView):
    template_name = "account/otp_login.html"



class UserLogin(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})


    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                form.add_error("username", "نام کاربری یا رمز عبور اشتباه است")
        else:
            form.add_error("username", 'اطلاعات اشتباه است')
        return render(request, 'account/login.html', {"form": form})


class OtpLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = OtpLoginForm()
        return render(request, 'account/otp_login.html', {'form': form})

    def post(self, request):
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000, 9999)
            # SMS.verification(
            #     {'receptor': cd['phone'], 'type': '1', 'templates': 'randcode', 'param1': randcode})
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'], code=randcode, token=token)
            print(randcode)
            return redirect(reverse('account:user_checkotp') + f'?token={token}')
        else:
            form.add_error("phone", 'اطلاعات اشتباه است')
        return render(request, 'account/otp_login.html', {"form": form})





class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, 'account/check_otp.html', {'form': form})


    def post(self, request):
        token = request.GET.get('token')
        if not token:
            return redirect(reverse('account:user_register'))
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], token=token).exists():
                otp = Otp.objects.get(token=token)
                user, is_create = User.objects.get_or_create(phone=otp.phone)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                otp.delete()
                return redirect("/")
        else:
            form.add_error("phone", 'اطلاعات اشتباه است ')
        return render(request, 'account/check_otp.html', {"form": form})


class AddAddressView(View):
    def post(self, request):
        user_address = UserAddress.objects.all()
        form = AddressCreationForm(request.POST)
        cities = City.objects.all()
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
        return render(request, 'account/profile/addresses.html', {'form': form, 'city': cities, 'user_address': user_address})

    def get(self, request):
        form = AddressCreationForm()
        cities = City.objects.all()
        user_address = UserAddress.objects.all()
        return render(request, 'account/profile/addresses.html',{'form': form, 'city': cities, 'user_address': user_address})


class AddressDeleteView(View):
    def post(self, request, id, *args, **kwargs):
        address = get_object_or_404(UserAddress, id=id)
        address.delete()
        return redirect("account:add_address")


def logout_view(request):
    logout(request)
    return redirect('home:home')


class PersonalInformation(TemplateView):
    template_name = "account/profile/personal-info.html"


