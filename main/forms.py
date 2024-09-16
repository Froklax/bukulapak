from django.forms import ModelForm
from main.models import Product

class BookForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "quantity"]