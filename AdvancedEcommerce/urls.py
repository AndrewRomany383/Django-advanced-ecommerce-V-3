"""
URL configuration for AdvancedEcommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from AdvancedEcommerce import settings
from Accounts import views
urlpatterns = [
    path('9O]WT_)IpjXm$~nCUx#RW@S6__ULJj/', admin.site.urls),
    path('', include('store.urls')),
    path('cart/', include('Cart.urls')),
    path('accounts/', include('Accounts.urls')),
    path('orders/', include('Orders.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
