from django.db import models
from account.models import User


class Article(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="author", verbose_name="نویسنده")
    title = models.CharField(max_length=60,verbose_name= "موضوع")
    content = models.TextField(verbose_name="متن مقاله")
    image = models.ImageField(upload_to="article",null=True,blank=True, verbose_name="تصویر مقاله")
    created_at =  models.DateField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "مقالات"
        verbose_name = "مقاله"


    def __str__(self):
        return f"{self.title}-{self.content[:30]}"





