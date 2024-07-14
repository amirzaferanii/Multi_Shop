from django.db import models
from account.models import User
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders',verbose_name='کاربر')
    total_price = models.IntegerField(default=0,verbose_name="کل خرید")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ سفارش')
    is_paid = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')

    def __str__(self):
        return self.user.phone


    class Meta:
        verbose_name_plural = "سفارشات"
        verbose_name = "سفارش"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE , related_name='items',verbose_name='سفارش')
    product = models.ForeignKey(Product , on_delete=models.CASCADE, related_name='items', verbose_name='محصول')
    size = models.CharField(max_length=12,verbose_name='سایز')
    color = models.CharField(max_length=12, verbose_name='رنگ')
    quantity = models.SmallIntegerField(verbose_name='تعداد')
    price = models.PositiveIntegerField(verbose_name='قیمت')



    class Meta:
        verbose_name_plural = "نوع سفارش"




