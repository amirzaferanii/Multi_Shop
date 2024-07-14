from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.UserLogin.as_view(), name='user_login'),
    path('otplogin', views.OtpLoginView.as_view(), name='otp_login'),
    path('checkotp', views.CheckOtpView.as_view(), name='user_checkotp'),
    path('logout', views.logout_view, name='user_logout'),
    path('add/address', views.AddAddressView.as_view(), name='add_address'),
    path('delete/<str:id>/', views.AddressDeleteView.as_view(), name='address_delete'),
    path('personal_information',views.PersonalInformation.as_view(),name='personal_information'),


]
