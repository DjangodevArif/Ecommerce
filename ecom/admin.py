from django.contrib import admin
from .models import *


# Register your models here.

def make_order_delivered(ModelAdmin, request, queryset):
    queryset.update(delivered=True)
make_order_delivered.short_description = 'Update delivered'

class FinalorderAdmin(admin.ModelAdmin):
    list_display =[
        'user',
        'ammount',
        'order_date','delivered',
        'refund_request',
        'refunded','payment_method'
    ]
    list_filter =[
        'ammount','order_date',
        'delivered',
        'refund_request','refunded',
        'payment_method'

    ]
    list_display_links =[
        'user',
        'refund_request',
        'payment_method'
    ]
    search_fields =[
        'user__username', 'invoice_num',
    ]
    actions = [make_order_delivered]

admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Profile)
admin.site.register(CartItem)
admin.site.register(Catagory)
admin.site.register(Coupon)
admin.site.register(Finalorder,FinalorderAdmin)
admin.site.register(RefundRequest)
admin.site.register(ShippingAddress)
admin.site.register(ImageItem)
admin.site.register(Review)