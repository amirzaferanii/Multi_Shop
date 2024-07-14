from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path('<int:pk>', views.ProductDetail.as_view(), name="product_detail"),
    path('list', views.ProductListView.as_view(), name="product_list"),
    path('mainrender' ,views.CategoryRenderPartial.as_view(), name="main_render"),
    path("category/<slug:slug>" , views.Category_detail, name="category_detail")

]