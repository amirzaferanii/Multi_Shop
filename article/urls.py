from django.urls import path
from . import views

app_name = "article"

urlpatterns = [
    path('',views.ArticleListView.as_view(),name="article"),
    path('detail/<int:pk>',views.ArticleDetail.as_view(),name="detail")

]