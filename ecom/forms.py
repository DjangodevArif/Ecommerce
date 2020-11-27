from django import forms

from .models import Coupon, RefundRequest, Item , Catagory

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class Shipping_add(forms.Form):

    
   
    country = CountryField(blank_label='(Select country)').formfield(widget=CountrySelectWidget(attrs={'class': 'form-control w-100 h-25'}))
    district = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control ','placeholder':'District'}))
    thana = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control ','placeholder':'Town/City'}))
    address = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control ','placeholder':'Address line 01'}))
    zip_code = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control ','placeholder':'zip'}))
    holding_address = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control ', 'placeholder':'Holding address' }))

class PaymentFrom(forms.Form):

    payment_method = [
        ('P','Paypal'),
        ('S','Stripe')
    ]
    address_ch = [
        ('Use_default','Use default for delivery........'),
        ('New_address','Use new addrss for delivery'),
    ]

    payment_option = forms.ChoiceField(widget=forms.RadioSelect,choices= payment_method)
    use_defult_address = forms.ChoiceField(widget=forms.RadioSelect, choices = address_ch)

class CouponForm(forms.ModelForm):

    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter coupon code'}))

    class Meta:
        model = Coupon
        fields = ['code']

class RefundRequestForm(forms.ModelForm):

    invoice = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Type your order invoice number'}))
    message = forms.CharField(widget= forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Why you request to refund...', 'rows':2}))

    class Meta:
        model = RefundRequest
        fields = ['invoice', 'message']

class NewItemForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':'Name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control form-control-lg','rows':1 ,'placeholder':'Discription'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control form-control-lg','placeholeder':'Price'}))
    dis_price = forms.DecimalField(required=False,widget=forms.NumberInput(attrs={'class':'form-control form-control-lg','placeholeder':'Discount-price'}))
    main_image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control form-control-lg','placeholeder':'Main-image'}))
    cata = forms.ModelChoiceField(queryset=Catagory.objects.all(),empty_label="(Nothing)",widget=forms.Select(attrs={'class':'form-control form-control-lg w-100 ','placeholder':'Catagory'}))
    class Meta:
        model = Item
        fields = ('name','description','price','dis_price','main_image','cata')


class ReviewForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control mb-10','placeholder':'Review', 'rows':2}))
