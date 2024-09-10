from django.shortcuts import render

def show_main(request):
    context = {
        'name' : 'Buku 1',
        'price': '50.000',
        'description': 'A very interesting read!',
        'quantity': '2',
    }

    return render(request, "main.html", context)
