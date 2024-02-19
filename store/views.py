from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ReviewForm
from .models import Product, Category, ReviewRating, ProductGallery
from Cart.models import Cart, CartItem
from Cart.views import _cart_id
from Orders.models import OrderProduct
# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.values('pk', 'image', 'name', 'price').filter(category=categories, is_active=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.values('pk', 'image', 'name', 'price').filter(is_active=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        "products": paged_products,
        "product_count": product_count
    }
    return render(request, "store/store.html", context)


def home(request, category_slug=None):
    products = Product.objects.filter(is_active=True)
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product)
    return render(request, "store/products.html", {'products': products, 'reviews': reviews})


def home_store(request, category_slug=None):
    products = Product.objects.values('pk', 'image', 'name', 'price').filter(is_active=True)
    return render(request, "store/store.html", {'products': products})
                

def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    except Exception as e:
        raise e

    try:
        if request.user.is_authenticated:
            order_product = OrderProduct.objects.filter(user=request.user, product_id=product).exists()
        else:
            order_product = OrderProduct.objects.filter(product_id=product).exists()
    except OrderProduct.DoesNotExist:
        order_product = None

    reviews = ReviewRating.objects.filter(product_id=product)

    # the product gallery

    product_gallery = ProductGallery.objects.filter(product_id=pk)

    return render(request, 'store/product-detail.html', {'product': product,
                                                         'in_cart': in_cart,
                                                         'order_product': order_product,
                                                         'reviews': reviews,
                                                         'product_gallery': product_gallery})


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
    context = {
        'products': products,
    }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                return redirect(url)






