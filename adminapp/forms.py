from .models import Product,ColdCoffee
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Submit


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        labels = {"category":"Select Category"}
class CoffeePaymentForm(forms.ModelForm):
    class Meta:
        model = ColdCoffee
        fields = "__all__"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "name",
            "amount",
            Submit('submit','Buy',css_class="button white btn-block btn-primary")
        )