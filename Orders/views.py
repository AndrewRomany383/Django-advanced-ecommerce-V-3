from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

from store.models import Product
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from Cart.models import CartItem
import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# Create your views here.


@login_required(login_url='login')
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total = (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (10 * total) / 100
    grand_total = total + tax
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.country = form.cleaned_data['country']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.pk)
            data.order_number = order_number
            data.is_ordered = True
            data.save()
            order = Order.objects.get(user=current_user, is_ordered=True, order_number=order_number, id=data.pk)
            host = request.get_host()
            paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': Order.objects.get(user=request.user, is_ordered=True, id=data.pk).order_total,
                'item_name': 'Order {}'.format(Order.objects.get(user=request.user, is_ordered=True, id=data.pk).order_number),
                'invoice': Order.objects.get(user=request.user, is_ordered=True, id=data.pk).order_total,
                'currency_code': 'USD',
                'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
                'return_url': 'http://{}{}'.format(host, reverse('order_complete')),
                'cancel_return': 'http://{}{}'.format(host, reverse('payment_unsuccessful')),
            }
            form = PayPalPaymentsForm(initial=paypal_dict)
            payment = Payment(user=current_user,
                              payment_id=order_number,
                              payment_method='PayPal',
                              amount_paid=grand_total,
                              status=False)
            payment.save()
            order.payment = payment
            order.save()
            # move the cart items to OrderProduct table
            for item in cart_items:
                order_product = OrderProduct()
                order_product.order_id = order.id
                order_product.payment = payment
                order_product.user_id = current_user.id
                order_product.product_id = item.product_id
                order_product.quantity = item.quantity
                order_product.product_price = item.product.price
                order_product.ordered = True
                order_product.save()
                # reduce the quantity of the sold products
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()
            # clear the cart
            # send order received email to customer
            mail_subject = 'Your order has been received'
            message = render_to_string('Orders/order_received_email.html', {
                'user': current_user,
                'order': order,
            })
            to_email = current_user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'form': form
            }
            return render(request, 'Orders/place-order2.html', context)
        else:
            return HttpResponse(f'<h1>{form.errors}</h1>')
    else:
        return redirect('checkout')


"""def payments(request):
    body = json.loads(request.body)
    print(body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    return render(request, 'Orders/place-order2.html')"""


"""def payments(request):
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': Order.objects.get(user=request.user, is_ordered=False).order_total,
        'item_name': 'Order {}'.format(Order.objects.get(user=request.user, is_ordered=False).order_number),
        'invoice': Order.objects.get(user=request.user, is_ordered=False).order_total,
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_successful')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_unsuccessful')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
        'form': form
    }
    return render(request, 'Orders/place-order2.html', context)"""


def payment_unsuccessful(request):
    return HttpResponse('<h1>Payment unsuccessful</h1>')


@login_required(login_url='login')
def order_complete(request):
    try:
        order = Order.objects.latest('is_ordered', 'id')
        ordered_products = OrderProduct.objects.filter(order_id=order.id, ordered=True, user=request.user)
        subtotel = 0
        for i in ordered_products:
            subtotel += i.product_price * i.quantity
        context = {
            'order': order,
            'ordered_products': ordered_products,
            'subtotel': subtotel
        }
        cart_item = CartItem.objects.filter(user=request.user)
        cart_item.delete()
        return render(request, 'Orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('store')


def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    sub_total = 0
    for i in order_detail:
        sub_total += i.product_price * i.quantity
    context = {
        'order_detail': order_detail,
        'order': order,
        'sub_total': sub_total
    }
    return render(request, 'Orders/order_detail.html', context)
