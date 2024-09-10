from django.shortcuts import render

def show_main(request):
    context = {
        'name' : 'Buku 1',
        'price': '50.000',
        'description': 'A very interesting read!',
        'quantity': '2',
        'nama_aplikasi' : 'Bukulapak',
        'person' : 'Bertrand Gwynfory Iskandar',
        'npm' : '2306152121',
        'class' : 'PBP C',
    }

    return render(request, "main.html", context)
