from django.urls import path
from main.views import show_main, create_book_entry, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user, edit_book, delete_book, add_book_entry_ajax, create_book_flutter

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-book-entry', create_book_entry, name='create_book_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('edit-book/<uuid:id>', edit_book, name='edit_book'),
    path('delete/<uuid:id>', delete_book, name='delete_book'),
    path('create-ajax/', add_book_entry_ajax, name='add_book_entry_ajax'),
    path('create-flutter/', create_book_flutter, name='create_book_flutter'),
]

