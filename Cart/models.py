from django.db import models
from store.models import Product
from Accounts.models import Account


# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=300, unique=True, null=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, related_name='product_cart_item', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='cart', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product}'
