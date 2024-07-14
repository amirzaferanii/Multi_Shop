from django.shortcuts import get_object_or_404
from product.models import Category
from article.models import Article
from django.conf import settings


def recent_articles(request):
    recent_articles = Article.objects.order_by('-created_at')[:3]
    return {'recent_articles': recent_articles}


CART_SESSION_ID = 'cart'

def cart_item_count(request):
    cart = request.session.get(CART_SESSION_ID, {})
    cart_length = len(cart)
    return {'cart_item_count': cart_length}




