from django.contrib import admin
from django.urls import path
from .import views
from .views import (
    Itemview,Product, CheckoutView,StripeView, Refundview, Login_View,
    PaypalView, newitem
)
urlpatterns = [
    path('',Itemview.as_view(),name = 'home'),
    path('product/<slug>/',Product.as_view(), name = 'product'),
    path('card/',views.cartview, name = 'card'),
    path('checkout/',CheckoutView.as_view(), name = 'checkout'),
    path('add/',views.add_to_cart, name= 'add'),
    path('new_item', views.newitem, name= 'new'),
    path('remove/<slug>/',views.remove_from_cart, name= 'remove'),
    path('payment/stripe/',StripeView.as_view(), name = 'stripe'),
    path('payment/paypal/',PaypalView.as_view(), name= 'paypal' ),
    path('refund_request/',Refundview.as_view(), name= 'refund'),
    path('login/', Login_View.as_view(template_name ='ecom/login.html'), name = 'login')

]
