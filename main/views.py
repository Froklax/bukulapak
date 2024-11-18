import datetime
from django.shortcuts import render, redirect, reverse
from main.forms import BookForm
from main.models import Product
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
import json

@login_required(login_url='/login')
def show_main(request):
    context = { 
        'nama_user': request.user.username,
        'nama_aplikasi' : 'Bukulapak',
        'person' : 'Bertrand Gwynfory Iskandar',
        'npm' : '2306152121',
        'class' : 'PBP C',
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)

def create_book_entry(request):
    form = BookForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        book_entry= form.save(commit=False)
        book_entry.user = request.user
        book_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_book_entry.html", context)

@csrf_exempt
@require_POST
def add_book_entry_ajax(request):
    name = strip_tags(request.POST.get("name"))
    price = request.POST.get("price")
    description = strip_tags(request.POST.get("description"))
    quantity = request.POST.get("quantity")
    user = request.user
    
    errors = {}

    if not name:
        errors['name'] = "Name field cannot be blank."
    if not description:
        errors['description'] = "Description field cannot be blank."
    if not price or not price.isdigit() or int(price) <= 0:
        errors['price'] = "Price not valid."
    if not quantity or not quantity.isdigit() or int(quantity) <= 0:
        errors['quantity'] = "Price not valid."


    if errors:
        return JsonResponse(errors, status=400)
        
    new_book = Product(
        name=name, price=price,
        description=description, quantity=quantity,
        user=user
    )
    new_book.save()

    return HttpResponse(b"CREATED", status=201)

def edit_book(request, id):
    # Get book berdasarkan id
    book = Product.objects.get(pk = id)

    # Set book entry sebagai instance dari form
    form = BookForm(request.POST or None, instance=book)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_book.html", context)

def delete_book(request, id):
    # Get book berdasarkan id
    book = Product.objects.get(pk = id)
    # Hapus book
    book.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('main:show_main'))

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
      else:
        messages.error(request, "Invalid username or password. Please try again.")

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def show_xml(request):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def create_book_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_book = Product.objects.create(
            user=request.user,
            name=data["name"],
            price=int(data["price"]),
            description=data["description"],
            quantity=int(data["quantity"]),
        )

        new_book.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)