from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)
from django.views.generic import View, ListView, DetailView ,TemplateView, CreateView
from .models import *
import json
from .uitils import Invoice
from .forms import Shipping_add, PaymentFrom, CouponForm, RefundRequestForm, NewItemForm, ReviewForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages


import stripe
stripe.api_key = "___________"
from django.template.loader import get_template
from xhtml2pdf import pisa
from twilio.rest import Client
# Create your views here.



class Itemview(ListView):
    model = Item
    template_name = 'ecom/body.html'
    ordering = '-id'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['catagory'] = Catagory.objects.all()
        return context
        

class Product(DetailView):
    model = Item
    template_name = 'ecom/product_details.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        context['all_review'] = Review.objects.filter(product=self.get_object())
        if self.request.user.is_authenticated:
            try:
                orderitem = CartItem.objects.get(user=self.request.user,item=self.get_object(), orderd= False)
                context['quantity'] = orderitem.quantity
            except:
                context['quantity'] = 0
        if self.request.user.is_authenticated is False:
            try:
                data = json.loads(self.request.COOKIES['cart'])
                for i in data:
                    if i == self.get_object().slug:
                        context['quantity'] = data[i]['quantity']                        
            except:
                context['quantity'] = 0
    
        return context


    def post(self, *args, **kwargs):
        form = ReviewForm(self.request.POST or None)
        if form.is_valid():
            review = Review()
            review.author = self.request.user.profile
            review.product = self.get_object()
            review.body = self.request.POST.get('body')
            review.star = self.request.POST.get('score')
            review.save()
            # print(self.request.POST)
            # print(self.request.POST.get('form'))
            # print(self.request.POST.get('score'))
        messages.success(self.request,'Yor review submited')
        return JsonResponse({'body':review.body,'author':str(review.author)},safe=False)

def cartview(request):
      
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        item_list = cart.order.all()
    else:
        try:
            data = json.loads(request.COOKIES['cart'])
        except:
            data = {}
        final_price = 0
        item_list = []
        for i in data:
            try:
                item = Item.objects.get(slug = i)
                if Item.objects.get(slug=i).dis_price:
                    final_price += data[i]['quantity'] * item.dis_price
                    item_list.append({
                    'item':{
                        'main_image':item.main_image,
                        'name':item.name,
                        'price':item.price,
                        'quantity':data[i]['quantity'],
                        'slug':item.slug,
                        'dis_price':item.dis_price,
                        },
                    'quantity':data[i]['quantity'],
                    'get_item_disc_price': item.dis_price * data[i]['quantity'],
                    'get_saved': (item.price * data[i]['quantity'])-(item.dis_price * data[i]['quantity']),
                    })
                else:
                    final_price += data[i]['quantity'] * item.price
                    item_list.append({
                    'item':{
                        'main_image':item.main_image,
                        'name':item.name,
                        'price':item.price,
                        'slug':item.slug,
                        },
                    'quantity':data[i]['quantity'],
                    'get_item_price': data[i]['quantity'] * item.price,
                    })
            except:
                pass  
        cart = {'final_price': final_price }
    return render(request,'ecom/card.html',{'item_list':item_list, 'cart':cart})


class CheckoutView(LoginRequiredMixin, TemplateView):  
    
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['form'] = Shipping_add()
            context['p_form'] = PaymentFrom()
            context['coup_form'] = CouponForm()
            context['default_add'] = Profile.objects.get(user =self.request.user)
            context['cart'] = Cart.objects.get(user=self.request.user)
            if Profile.objects.get(user= self.request.user).defult_address is None:
                context['Address'] = True 
            if Cart.objects.get(user= self.request.user).shipping_add is None:
                context['extraadd'] = True
            return render(self.request, 'ecom/checkout.html',context)


    def post(self, request ,**kwargs):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        if not cart.order.all():
            messages.info(request,'You have no item')
            redirect('home')
        form = Shipping_add(request.POST or None )
        p_form = PaymentFrom(request.POST or None )
        coup_form = CouponForm(request.POST or None )
        if 'shipping_details' in request.POST:
            address = ShippingAddress()
            address.user = request.user
            address.country = request.POST.get('country')
            address.district = request.POST.get('district')
            address.thana = request.POST.get('thana')
            address.address = request.POST.get('address')
            address.holding_address = request.POST.get('holding_address')
            address.zipcode = request.POST.get('zip_code')
            if ShippingAddress.objects.filter(user=request.user,default=True).exists():
                address.default = False
            else:
                address.default = True    
            address.save()
            if address.default == False:
                cart.shipping_add = ShippingAddress.objects.get(id= address.id)
                cart.save()
            if Profile.objects.get(user= request.user).defult_address is None: 
                profile = Profile.objects.get(user= request.user)
                profile.defult_address = ShippingAddress.objects.get(id= address.id)
                profile.save()
            return redirect('checkout')
        
        if 'payment' in request.POST:

            cart = get_object_or_404(Cart,user= request.user)
            address = cart.shipping_add

            if cart.order.all():  
                if request.POST['payment_option'] == 'S':
                    if address is None:
                        cart.shipping_add = ShippingAddress.objects.get(user=request.user, default=True)
                        cart.save()
                    return redirect('stripe')
                elif request.POST['payment_option'] == 'P':
                    if address is None:
                        cart.shipping_add = ShippingAddress.objects.get(user=request.user, default=True)
                        cart.save()
                    return redirect('paypal')
                    return HttpResponse('You are now in Paypal page.')
            else:
                messages.info(request,'Courently your cart is empty pls add some product in your cart!!!')
                return redirect('home')                
        
        if 'coupon' in request.POST:
            if coup_form.is_valid():
                code = coup_form.cleaned_data.get('code') 
                if Coupon.objects.filter(code= code).exists():
                    validation = Coupon.objects.get(code= code)
                    cart = get_object_or_404(Cart,user= request.user)
                    cart.coupon = validation
                    cart.save()
                    messages.success(request,'Your coupon is activated')
                    return redirect(request.META.get('HTTP_REFERER'))                 
                messages.warning(request,'Your code is not valid')
                return redirect(request.META.get('HTTP_REFERER'))


def add_to_cart(request): 

    select = Item.objects.get(slug= request.POST['productId'])
    
    if request.POST['action'] == 'add':
        if CartItem.objects.filter(user=request.user, item= select, orderd= False).exists():
            item = CartItem.objects.get(user=request.user, item= select, orderd= False)
            cart, created = Cart.objects.get_or_create(user= request.user)
            cart.order.add(item)
        else:
            cartitem = CartItem.objects.create(user=request.user,
                        item= select,quantity=1, orderd= False)
            cart, created = Cart.objects.get_or_create(user= request.user)
            cart.order.add(cartitem)
    
    if request.POST['action'] == 'inc':
        product, created = CartItem.objects.get_or_create(user=request.user, item= select, orderd= False)
        product.quantity +=1
        product.save()
        messages.success(request,'Your item quantity succefully increase')    

    if request.POST['action'] == 'dec':
        product = get_object_or_404(CartItem,user=request.user, item=select, orderd= False)
        if product.quantity > 1:
            product.quantity -= 1
            product.save()
            messages.success(request,'Your item quantity successfull decrease')
        elif product.quantity == 1:
            product.delete()
 
    return JsonResponse('We are using js',safe=False)

def remove_from_cart(request,slug):
    select = Item.objects.get(slug= slug)
    trash_item = get_object_or_404(CartItem,user=request.user, item=select, orderd= False)
    trash_item.delete()
    messages.success(request,'Your item is remove from cart')
    return redirect(request.META.get('HTTP_REFERER'))




class StripeView(TemplateView):
    template_name = 'ecom/payment.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context[''] = ''
        return context

    def post(self, *args, **kwargs):
        amount = Cart.objects.get(user=self.request.user)
        tk= int(amount.final_price())
        token = self.request.POST.get('stripeToken')
        save = self.request.POST.get('save')
        profile = Profile.objects.get(user= self.request.user)
        if save:
            cu_id= stripe.Customer.create(
                source=token
            )
            profile.stripe_customer = cu_id['id']
            profile.save()

        try:
            pay_id =stripe.Charge.create(
                amount=tk,
                currency="usd",
                source=token,
               
            )

            cart =Cart.objects.get(user=self.request.user)
            cart_item = cart.order.all()
            
            archive = Finalorder()            
            archive.user = self.request.user
            archive.invoice_num = Invoice('Mycompany',self.request.user.id)
            archive.ammount = cart.final_price()
            archive.tnsx_id = pay_id['id']
            archive.payment_method = 'Stripe'
            archive.shipping_add = cart.shipping_add
            archive.save()
            archive.product.add(*cart.order.all())

          
            archive.save()    
            cart.shipping_add = None
            cart.coupon = None
            cart.save()
            cart_item.update(orderd=True)
            for item in cart_item:
                item.save()
            cart.order.clear()
            account_sid = 'ACa25070639e5537516c9310af7d0b6e26'
            auth_token = 'ec9489a6b85da9e53d82ec59bf64f0ee'
            client = Client(account_sid, auth_token)

            message = client.messages .create(
                    body= f"Hey '{archive.user}',thansk for your order.'{archive.invoice_num}' it is your order number. ",
                     from_='+12185000163',
                     to='+37062465647 '
                 )


            template_path = 'ecom/order_pdf.html'
            context = {'order': archive}
            response = HttpResponse(content_type='application/pdf')

            response['Content-Disposition'] = 'filename= "Order-Details.pdf"'
            template = get_template(template_path)
            html = template.render(context)

            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response)
            # if error then show some funy view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response


        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught

            messages.warning(self.request,f'{e.error.message}')
            return redirect('home')
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request,f'{e.error.message}')
            return redirect('home')
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.warning(self.request,f'{e.error.message}')
            return redirect('home')
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request,f'{e.error.message}')
            return redirect('home')
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request,f'{e.error.message}')
            return redirect('home')
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(self.request,f'{e.error.message}')
            return redirect('home')
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.warning(self.request,f'{e.error.message}')
            return redirect('home')

class Refundview(View):
    def get(self, *args, **kwargs):
        form =RefundRequestForm()
        context = { 'form':form }
        return render(self.request, 'ecom/refund.html', context)

    def post(self, request, *args, **kwargs):
        form = RefundRequestForm(request.POST or None)
        if form.is_valid():
            invoice = request.POST['invoice']
            if Finalorder.objects.filter(user=request.user, invoice_num= invoice).exists():

                varify = Finalorder.objects.get(invoice_num= invoice)
               
                form.instance.user = request.user
                form.save()
                varify.refund_request = True
                varify.save()
                messages.success(request,'Your request is successfully received')
                return redirect('home')
            messages.warning(request,'Your invoice number is not valid')
            return redirect(request.META.get('HTTP_REFERER'))


class Login_View(LoginView):
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        
        if self.request.COOKIES['cart'] == '':
            login(self.request, form.get_user())
        else:
            login(self.request, form.get_user())
            cart, created = Cart.objects.get_or_create(user= self.request.user)
            data = json.loads(self.request.COOKIES['cart'])
            for i in data:
                item = Item.objects.get(slug=i)
                if item not in cart.order.all():
                    cartitem,created = CartItem.objects.get_or_create(
                        user=self.request.user,
                        item=item,
                        orderd=False
                    )
                    cartitem.quantity = data[i]['quantity']
                    cartitem.save()
                    cart.order.add(cartitem)
                    cart.save()
                else:
                    cartitem = CartItem.objects.get(user=self.request.user,item= item)
                    cartitem.quantity = data[i]['quantity']
                    cartitem.save()
        response = redirect(self.get_success_url())
        response.delete_cookie('cart')
        return response


class PaypalView(TemplateView):

    template_name = 'ecom/paypal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['amount'] = Cart.objects.get(user= self.request.user).final_price()
        return context

    def post(self,request, *args, **kwargs):
        data = json.loads(json.dumps(request.POST))

        if data['details[status]'] == 'COMPLETED':
            cart =Cart.objects.get(user=self.request.user)
            cart_item = cart.order.all()
            
            archive = Finalorder()            
            archive.user = self.request.user
            archive.invoice_num = Invoice('Mycompany',self.request.user.id)
            archive.ammount = cart.final_price()
            archive.tnsx_id = data['details[id]']
            archive.payment_method = 'Paypal'
            archive.shipping_add = cart.shipping_add
            archive.save()
    
            archive.product.add(*cart.order.all())
            archive.save()
            cart.shipping_add = None
            cart.coupon = None
            cart.save()
            cart_item.update(orderd=True)
            for item in cart_item:
                item.save()
            cart.order.clear()
            account_sid = 'ACa25070639e5537516c9310af7d0b6e26'
            auth_token = 'ec9489a6b85da9e53d82ec59bf64f0ee'
            client = Client(account_sid, auth_token)

            message = client.messages .create(
                    body= f"Hey '{archive.user}',thansk for your order.'{archive.invoice_num}' it is your order number. ",
                     from_='+12185000163',
                    #  media_url=['https://giphy.com/gifs/krystlelina-mood-shopping-krystle-lina-WpJ2JrXXXm2iuT5UfJ'],
                     to='+12074241129'
                 )
            messages.success(self.request,'Your transaction is succefull')
            return redirect('home')
        else:
            messages.warning(self.request,'Something worng try again !!')
            return redirect(request.META.get('HTTP_REFERER'))
        messages.success(self.request,'Your transaction is succefull')
        return redirect('home')


def newitem(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            it = form.save(commit=False)
            extra = request.FILES.getlist('image[]')
            form.save()
            for field in extra:
                extra_image = ImageItem.objects.create(item_link=it, image=field)
        messages.success(request,'Your Item succefully addedd')
        return redirect('home')           
    else:
        form = NewItemForm(request.POST)
    return render(request, 'ecom/new_item.html',{'form':form})


