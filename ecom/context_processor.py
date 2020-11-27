from ecom.models import Cart
from django.shortcuts import get_object_or_404

import json

def item_count(request):

    if request.user.is_authenticated:
        cart,_ = Cart.objects.get_or_create(user = request.user)
        item_num = cart.order.all().count()

    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
            
        item_num = len(cart)
    return { 'item_num':item_num }