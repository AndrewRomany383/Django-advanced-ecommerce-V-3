from django.db import models
from django.urls import reverse
from Accounts.models import Account
from django.db.models import Avg, Count
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    is_active = models.BooleanField()

    class Meta:
        verbose_name_plural = 'Categories'
    
    
    def get_url(self):
        return reverse('product_by_category', kwargs={'category_slug':self.slug})
    
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='media')
    slug = models.CharField(max_length=150)
    is_active = models.BooleanField()
    category = models.ForeignKey(Category, related_name='Category', on_delete=models.CASCADE)
    price = models.IntegerField()
    stock = models.IntegerField(default=5)

    def __str__(self):
        return self.name

    def average_review(self):
        reviews = ReviewRating.objects.filter(product=self)
        if reviews.count() > 0:
            reviews = reviews.aggregate(average=Avg('rating'))
            return float(reviews['average'])
        else:
            return 0

    def count_review(self):
        reviews = ReviewRating.objects.filter(product=self)
        if reviews.count() > 0:
            reviews = reviews.aggregate(count=Count('id'))
            return int(reviews['count'])
        else:
            return 0


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media')

    def __str__(self):
        return self.product.name


class Attribute(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=50)
    attribute = models.ForeignKey(Attribute, related_name='Attribute', on_delete=models.CASCADE)
    def __str__(self):
        return self.value


class Inventory(models.Model):
    is_active = models.BooleanField()
    is_default = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    sku = models.CharField(max_length=20, unique=True)
    product = models.ManyToManyField(AttributeValue)
    def __str__(self):
        return self.product.name


class StockControl(models.Model):
    last_checked = models.DateTimeField(auto_now_add=True, editable=False)
    units = models.IntegerField(default=0)
    inventory = models.OneToOneField(Inventory, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Stock Control"


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.subject} by {self.user}'





































































