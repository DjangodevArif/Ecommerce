from django.db import models
from django.contrib.auth.models import User

from django_countries.fields import CountryField


from django.core.exceptions import ValidationError
# Create your models here.

class Catagory(models.Model):
    cata = models.CharField(max_length=100)

    def __str__(self):
        return self.cata


def user_img_path(instance,filename):
    return 'Item_pics/{0}/{1}'.format(instance.name, filename)

def extra_img_path(instance,filename):
    return 'Item_pics/{0}/{1}'.format(instance.item_link.name, filename)


from PIL import Image
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    price = models.FloatField()
    dis_price = models.FloatField(null=True,blank=True)
    main_image = models.ImageField(default='default.jpg',upload_to =user_img_path)
    cata = models.ForeignKey(Catagory, on_delete=models.SET_NULL,null=True, blank=True)
    slug = models.SlugField(unique=True,blank=True, null=True)
    

    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.main_image.path)
        if img.height > 300 or img.width > 300:
            output_size =(300,300)
            img.thumbnail(output_size)
            img.save(self.main_image.path)


from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import *

@receiver(post_save, sender= Item)
def post_save_create_slug(sender,instance,**kwargs):
    if instance.slug is None:
        new_name = slugify(instance.name)
        new_cat = slugify(instance.cata)
        instance.slug = f'{new_name}-{new_cat}-{instance.id}'
        instance.save()


class ImageItem(models.Model):
    item_link = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to =extra_img_path)


class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    orderd = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} & {self.item.name} -x{self.quantity}'
    
    def get_item_price(self):
        return self.quantity * self.item.price

    def get_item_disc_price(self):
        return self.quantity * self.item.dis_price

    def get_saved(self):
        return self.get_item_price() - self.get_item_disc_price()

    def total_price(self):
        if self.item.dis_price:
            return self.item.dis_price * self.quantity
        else:
            return self.item.price * self.quantity

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    order = models.ManyToManyField(CartItem, blank=True)
    coupon = models.ForeignKey('Coupon',on_delete=models.SET_NULL,blank=True, null=True)
    shipping_add = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, null=True , blank=True)
    
    def __str__(self):
        return self.user.username

    def final_price(self):
        price = 0
        for item in self.order.all():
            price += item.total_price()
        if self.coupon:
            price -= self.coupon.amount
        return price


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    defult_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code = models.CharField(max_length=20)
    amount = models.FloatField()

    def __str__(self):
        return f'{str(self.amount)} & {self.code}'

    class Meta:
        verbose_name = 'Discount code'
# --------

class Finalorder(models.Model):

    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    product = models.ManyToManyField(CartItem) 
    invoice_num = models.CharField(max_length=30)
    shipping_add = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, null=True)
    ammount = models.FloatField()
    order_date = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    refund_request = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50)
    tnsx_id = models.CharField(max_length=50)

    def __str__(self):
        return self.invoice_num

class RefundRequest(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice = models.CharField(max_length=30)
    message = models.TextField(max_length=200)
    granted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} & {self.invoice}'
    
class ShippingAddress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = CountryField(blank=True)
    district = models.CharField(max_length=100)
    thana = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    holding_address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=40)
    default = models.BooleanField(default=False,verbose_name='Do you want to set default')


# Review model
class Review(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product =  models.OneToOneField(Item, on_delete=models.CASCADE)
    body = models.CharField(max_length=250)
    date = models.DateField(auto_now_add=True)
    star = models.IntegerField(default=0)



