from django.forms import ModelForm
from main.models import Product
from django.utils.html import strip_tags

class BookForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "quantity"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        return strip_tags(name)

    def clean_description(self):
        description = self.cleaned_data["description"]
        return strip_tags(description)