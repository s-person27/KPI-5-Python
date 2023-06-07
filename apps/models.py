from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    SEX_CHOISE = [
        (1, 'Man'),
        (2,  'Woman')
    ]

    sex=models.PositiveIntegerField(verbose_name="sex", choices=SEX_CHOISE, blank=True, default=1)
    birth_date = models.DateField(verbose_name="birthday" , null=True, blank=True)



    email=models.EmailField(verbose_name="email", unique=True, error_messages={
            "unique": _("A user  with that email already exists."),
        },)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    description = models.TextField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_order =  models.DateTimeField(auto_now_add=True)
    complete =models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems =self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item  in orderitems])
        return total

    @property
    def shipping(self):
        shipping =False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False :
                shipping = True
        return  shipping


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price *self.quantity
        return total






    # def __str__(self):
    #     return f'{self.email, self.username, self.}'


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User,  on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=12, null=True)

    def __str__(self):
        return self.address
