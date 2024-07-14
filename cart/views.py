from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.views.decorators.http import require_POST
from .cart_module import Cart
from product.models import Product
from .models import Order, OrderItem



class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, "cart/cart_detail.html", context={'cart': cart})


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        size, color, quantity = request.POST.get('size', 'خالی'), request.POST.get('color', 'خالی'), request.POST.get(
            'quantity', 'خالی')
        cart = Cart(request)
        cart.add(product, quantity, color, size)
        return redirect("cart:cart_detail")


class OrderDetailView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        return render(request, "cart/order_detail.html", {"order": order})


class OrderCreationView(View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=cart.total())
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], color=item['color'], size=item['size'] , price=item['price'], quantity=item['quantity'])
        cart.remove_cart()
        return redirect('cart:order_detail', order.id)


@require_POST
@csrf_exempt
def update_cart_item_quantity(request):
    unique_id = request.POST.get('unique_id')
    action = request.POST.get('action')
    cart = Cart(request)

    if action == 'increase':
        cart.update_quantity(unique_id, 1)
    elif action == 'decrease':
        cart.update_quantity(unique_id, -1)

    cart_total = cart.total()
    item = cart.cart[unique_id]
    item_total = int(item['quantity']) * int(item['price'])
    return JsonResponse({
        'quantity': item['quantity'],
        'item_total': item_total,
        'cart_total': cart_total,
    })

class CartDeleteView(View):
    def get(self, request, id, *args, **kwargs):
        cart = Cart(request)
        cart.delete(id)
        return redirect("cart:cart_detail")



