from django.shortcuts import render, redirect
from main.forms import BookForm
from main.models import Product
from django.http import HttpResponse
from django.core import serializers

def show_main(request):
    books = Product.objects.all()

    fetch_books = [{'name': book.name, 'price': book.price, 'description': book.description, 'quantity': book.quantity} for book in books]

    default_books = [
        {
            'name' : 'Purcell Kalkulus',
            'price': '50000',
            'description': 'Buat lulus kalkulus!',
            'quantity': '2',
        },
        
        {
            'name' : 'Rosen Matdis',
            'price': '40000',
            'description': 'Buat lulus matdis!',
            'quantity': '2',
        }
    ]

    all_books = default_books + fetch_books

    context = { 
        'nama_aplikasi' : 'Bukulapak',
        'person' : 'Bertrand Gwynfory Iskandar',
        'npm' : '2306152121',
        'class' : 'PBP C',
        'books' : all_books
    }

    return render(request, "main.html", context)

def create_book_entry(request):
    form = BookForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_book_entry.html", context)

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")