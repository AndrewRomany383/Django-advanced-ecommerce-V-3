from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>', views.product_detail, name='detail'),
    path('store/', views.home_store, name='store'),
    path('<slug:category_slug>', views.store, name='product_by_category'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>', views.submit_review, name='submit_review'),
]


