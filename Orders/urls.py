from django.urls import path, include
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    # paypal urls
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('payment_unsuccessful/', views.payment_unsuccessful, name='payment_unsuccessful'),
    # order details
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
]
