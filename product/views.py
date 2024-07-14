from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView,ListView
from .models import Category

from product.models import Product


class ProductDetail(DetailView):
    template_name = "product/product_details.html"
    model = Product



class CategoryRenderPartial(TemplateView):
    template_name = 'includes/main_navbar.html'
    def get_context_data(self, **kwargs):
        context = super(CategoryRenderPartial, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context


class ProductListView(ListView):
    model = Product
    template_name = "product/product_list.html"
    context_object_name = 'products'
    paginate_by = 9

def Category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.product_set.all()
    return render(request, "product/product_list.html", {"products": products})







