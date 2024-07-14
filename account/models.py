from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError("Users must have an phone address")
        user = self.model(phone=self.normalize_email(phone),)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(phone,password=password,)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="آدرس ایمیل", max_length=255,null=True,blank=True,unique=True,)
    fullname = models.CharField(max_length=50, verbose_name='نام کامل ')
    phone = models.CharField(max_length=12, unique=True,verbose_name='شماره تلفن')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Otp(models.Model):
    token = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    expiration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.phone


class City(models.Model):
    name = models.CharField(max_length=40,verbose_name="نام استان")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "استان ها"
        verbose_name = "استان"



class UserAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='addresses',verbose_name="کاربر")
    fullname = models.CharField(max_length=80,verbose_name='نام و نام خانوادگی')
    address = models.CharField(max_length=300, verbose_name='آدرس')
    email = models.EmailField(null=True, blank=True, verbose_name='ایمیل')
    postal_code = models.CharField(max_length=10,verbose_name='کد پستی')
    phone = models.CharField(max_length=12, verbose_name='تلفن')
    city = models.ForeignKey(City,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="استان")

    def __str__(self):
        return f'{self.user.fullname}-{self.user.phone}'

    class Meta:
        verbose_name_plural = 'آدرس کاربران'
        verbose_name = 'آدرس'


