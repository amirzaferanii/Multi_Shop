from django.urls import path
from . import views
from .views import update_cart_item_quantity

app_name = "cart"

urlpatterns = [
    path('detail', views.CartDetailView.as_view(), name="cart_detail"),
    path('add/<int:pk>', views.CartAddView.as_view(), name='cart_add'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/add', views.OrderCreationView.as_view(), name='order_create'),
    path('update/', update_cart_item_quantity, name='update_cart_item_quantity'),
    path('delete/<str:id>',views.CartDeleteView.as_view(),name="delete_cart"),



    ]
