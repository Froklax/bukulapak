# Bukulapak
Number 1 online bookstore in Pacil!!!

### Deployment
Live web app : [Bukulapak](http://bertrand-gwynfory-bukulapak.pbp.cs.ui.ac.id/)

### Fast Links
- [Tugas 3](#tugas-3)
- [Tugas 2](#tugas-2)

## Tugas 3

### Jelaskan mengapa kita memerlukan _data delivery_ dalam pengimplementasian sebuah platform?

_Data delivery_ penting dalam pengimplementasian sebuah platform karena sebagian besar aplikasi modern mengandalkan pertukaran data antara berbagai komponen dalam platform. _Data delivery_ memastikan bahwa data dapat dipertukar dengan aman, cepat, dan akurat antara client dan server. Tanpa data delivery, aplikasi tidak dapat berfungsi secara optimal karena data yang diperlukan tidak dapat diakses atau disampaikan dengan tepat waktu.

### Mana yang lebih baik antara XML dan JSON? Mengapa JSON lebih populer dibandingkan XML?

Menurut saya sendiri, JSON lebih baik dibandingkan XML. JSON juga lebih populer dan lebih sering digunakan dibandingkan XML karena berbagai alasan berikut:

- **Lebih Ringkas:** 
  JSON menggunakan struktur yang lebih sederhana dibandingkan XML, karena JSON tidak menggunakan tag pembuka dan penutup yang panjang seperti XML. Ini membuat JSON lebih efisien dalam hal ukuran data dan kecepatan parsing, yang sangat berguna untuk aplikasi dengan kebutuhan real-time.

- **Lebih mudah dibaca oleh manusia dan diproses mesin:** 
  JSON lebih mudah dipahami oleh _developer_ dan lebih cepat diproses oleh mesin, karena memiliki struktur yang lebih sederhana dibandingkan XML.

- **Integrasi langsung dalam JavaScript:** 
  JSON secara alami terintegrasi dengan JavaScript karena formatnya berasal langsung dari struktur objek JavaScript, sehingga sangat mudah diimplementasikan dalam aplikasi web yang menggunakan JavaScript di sisi client.

### Jelaskan fungsi dari method `is_valid()` pada form Django dan mengapa kita membutuhkan method tersebut?

Method `is_valid()` pada form Django digunakan untuk memeriksa apakah data yang dikirim melalui form memenuhi aturan validasi yang telah ditentukan pada form. Jika data yang diisi dalam form valid, method ini akan mengembalikan nilai `True` dan menyimpan data yang sudah divalidasi di atribut `cleaned_data` dari form. Jika data tidak valid, method ini akan mengembalikan nilai `False` dan mengeluarkan error yang bisa diakses melalui atribut `form.errors`.

Tanpa method `is_valid()`, data yang tidak benar atau tidak sesuai aturan validasi yang ditentukan bisa masuk ke sistem yang dapat menyebabkan error dan mengancam keamanan aplikasi.

### Mengapa kita membutuhkan `csrf_token` saat membuat form di Django? Apa yang dapat terjadi jika kita tidak menambahkan `csrf_token` pada form Django? Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?

`csrf_token` adalah token keamanan yang disisipkan oleh Django pada setiap form yang mengirimkan data melalui metode POST. Ketika user menjelajahi _website_, Django menghasilkan `csrf_token` unik untuk setiap sesi. Token ini termasuk dalam form yang dikirim oleh user dan diperiksa oleh server untuk memverifikasi bahwa permintaan tersebut berasal dari user yang terautentikasi dan bukan dari sumber jahat.

Django secara default memeriksa keberadaan `csrf_token` pada setiap permintaan POST. Jika token ini tidak ada atau tidak valid, server akan mengembalikan error 403 (Forbidden), yang berarti permintaan tersebut ditolak.

Jika `csrf_token` tidak digunakan, penyerang dapat membuat halaman palsu yang berisi form tersembunyi atau script yang mengirimkan permintaan POST ke server atas nama pengguna yang sedang login.

### Langkah Implementasi Checklist

1. **Membuat input `form` untuk menambahkan objek model pada app sebelumnya.**
   - Saya pertama membuat sebuah class BookForm di file forms.py yang merupakan subclass dari ModelForm di Django. Class ini digunakan untuk menghasilkan form berdasarkan model Product.

   ```python
      from django.forms import ModelForm
      from main.models import Product

      class BookForm(ModelForm):
         class Meta:
            model = Product
            fields = ["name", "price", "description", "quantity"]
   ```
   
   - Kemudian, saya membuat sebuah fungsi `create_book_entry` dalam file `views.py` untuk menangani pembuatan form baru. Fungsi ini menerima request dari pengguna dan membuat instance dari `BookForm`, dengan data POST jika ada.

   ```python
      def create_book_entry(request):
         form = BookForm(request.POST or None)

         if form.is_valid() and request.method == "POST":
            form.save()
            return redirect('main:show_main')

         context = {'form': form}
         return render(request, "create_book_entry.html", context)
   ```

   - Selanjutnya, saya membuat template HTML bernama `create_book_entry.html` untuk menampilkan form.

   ```HTML
      {% extends 'base.html' %} 
      {% block content %}
      <div class="form-container">
         <h1 class="form-title">Add New Book</h1>

         <form method="POST">
               {% csrf_token %}
               <table>
                  {{ form.as_table }}
                  <tr>
                     <td></td>
                     <td class="button-container-form">
                           <input type="submit" value="Add Book" class="add-button" />
                     </td>
                  </tr>
               </table>
         </form>
      </div>

      {% endblock %}
   ```

   - Terakhir, saya menambahkan path URL di file `urls.py` untuk mengakses fungsi form.

   ```python
      from django.urls import path
      from main.views import show_main, create_book_entry

      app_name = 'main'

      urlpatterns = [
         path('', show_main, name='show_main'),
         path('create-book-entry', create_book_entry, name='create_book_entry'),
      ]
   ```

2. **Menambahkan 4 fungsi views baru untuk melihat objek yang sudah ditambahkan dalam format XML, JSON, XML by ID, dan JSON by ID.**

   - Memambahkan fungsi view untuk XML pada `views.py`.

   ```python
      def show_xml(request):
         data = Product.objects.all()
         return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
   ```

   - Memambahkan fungsi view untuk JSON pada `views.py`.

   ```python
      def show_json(request):
         data = Product.objects.all()
         return HttpResponse(serializers.serialize("json", data), content_type="application/json")
   ```

   - Memambahkan fungsi view untuk XML by ID pada `views.py`.

   ```python
      def show_xml_by_id(request, id):
         data = Product.objects.filter(pk=id)
         return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
   ```

   - Menambahkan fungsi view untuk JSON by ID pada `views.py`.

   ```python
      def show_json_by_id(request, id):
         data = Product.objects.filter(pk=id)
         return HttpResponse(serializers.serialize("json", data), content_type="application/json")
   ```

   - Terakhir, saya menambahkan path url di `urls.py` untuk mengakses 4 fungsi tersebut. 

   ```python
      from django.urls import path
      from main.views import show_main, create_book_entry, show_xml, show_json, show_xml_by_id, show_json_by_id

      app_name = 'main'

      urlpatterns = [
         path('', show_main, name='show_main'),
         path('create-book-entry', create_book_entry, name='create_book_entry'),
         path('xml/', show_xml, name='show_xml'),
         path('json/', show_json, name='show_json'),
         path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
         path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
      ]
   ```
3. **Mengubah README.md.**

   - Terakhir, saya mengubah `README.md` yang sebelumnya telah saya buat untuk menambahkan jawaban dari pertanyaan-pertanyaan yang diberikan pada Tugas 3.

### Screenshot Hasil Akses Keempat URL Pada Postman
**XML**
![XML](./images/xml.png)

**XML BY ID**
![XML BY ID](./images/xmlbyid.png)

**JSON**
![JSON](./images/json.png)

**JSON BY ID**
![JSON BY ID](./images/jsonbyid.png)


## Tugas 2

### Langkah Implementasi Checklist

1. **Membuat Direktori Proyek.**
   - Saya mulai dengan membuat sebuah direktori untuk proyek saya dengan perintah `mkdir bukulapak` di terminal. Saya membuat virtual environment di dalam direktori proyek dengan perintah `python -m venv env`. Setelah itu, saya mengaktifkan virtual environment dengan perintah source env/bin/activate di terminal. Dengan ini, saya dapat menginstall paket Python dalam lingkungan terisolasi tanpa mempengaruhi sistem Python global.

2. **Mempersiapkan _Dependencies_.**
   - Saya membuat file bernama requirements.txt yang di dalamnya berisi semua _dependencies_ yang diperlukan. Setelah menyimpan file requirements.txt, saya menginstal semua _dependencies_ yang terdaftar di dalamnya dengan perintah `pip install -r requirements.txt`. Ini akan menginstal semua _dependencies_ yang diperlukan ke dalam virtual environment yang aktif.

3. **Membuat Proyek Django Baru.** 
   - Saya kemudian membuat proyek Django baru dengan menjalankan perintah `django-admin startproject bukulapak`. di direktori proyek. Perintah ini akan menginisialisasi proyek Django baru dengan nama bukulapak di direktori saat ini dan membuat struktur direktori dasar untuk proyek Django.

4. **Membuat Aplikasi Dengan Nama `main`.**
   - Setelah proyek Django berhasil dibuat, saya menambahkan aplikasi baru dengan nama `main` di dalam proyek tersebut dengan menjalankan perintah `python manage.py startapp main`. Aplikasi ini akan berisi fitur spesifik yang akan dikembangkan lebih lanjut.

5. **Melakukan Routing Pada Proyek Agar Dapat Menjalankan Aplikasi `main`.**
   - Untuk memastikan aplikasi `main` dapat diakses, saya melakukan routing di berkas `urls.py` yang ada di direktori proyek `bukulapak/urls.py`. Saya menambahkan rute yang mengarahkan permintaan ke aplikasi "main" dengan menambahkan baris kode berikut:
   
   
   ```python
    from django.contrib import admin
    from django.urls import path
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('main.urls')),
    ]
    ```

6. **Membuat Model Pada Aplikasi `main` Dengan Nama `Product`.**
   - Kemudian saya membuat model `Product` di `models.py` yang memiliki atribut `name`, `price`, `description`, dan `quantity`.


   ```python
    from django.db import models

    class Product(models.Model):
        name = models.CharField(max_length=255)
        price = models.IntegerField()
        description = models.TextField()
        quantity = models.IntegerField()

        @property
        def is_product_available(self):
            return self.quantity > 0
   ```

7. **Membuat Sebuah Fungsi Pada `views.py` Untuk Dikembalikan ke Dalam Sebuah Template HTML Yang Menampilkan Nama Aplikasi Serta Nama dan Kelas Saya.**
   - Saya membuat template main.html di dalam direktori `templates` aplikasi `main` untuk menampilkan data dari model Product berserta nama dan kelas saya. Kemudian saya menambahkan fungsi show_main di berkas main/views.py untuk merender template HTML yang sudah saya buat. Template menampilkan informasi seperti nama aplikasi, data produk, dan nama beserta dengan kelas saya.


   ```python
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
   ```

8. **Membuat Sebuah Routing Pada `urls.py` Aplikasi `main` Untuk Memetakan Fungsi Yang Telah Dibuat Pada `views.py`.**
   - Di dalam berkas `urls.py` pada aplikasi `main`, saya menambahkan rute untuk memetakan URL ke fungsi yang telah saya buat di `views.py` dengan kode dibawah:


   ```python
    from django.urls import path
    from main.views import show_main

    app_name = 'main'

    urlpatterns = [
        path('', show_main, name='show_main'),
    ]
   ```

9. **Melakukan Deployment ke PWS.**
   - Setelah semuanya selesai, saya melakukan deployment aplikasi saya ke Pacil Web Service atau PWS sehingga nantinya dapat diakses melalui Internet.

10. **Membuat README.md.**
    - Terakhir, saya membuat sebuah file `README.md` yang berisi tautan menuju aplikasi PWS yang sudah di-_deploy_, serta jawaban dari pertanyaan-pertanyaan yang diberikan.

### Bagan Berisi Request Client ke Web Aplikasi Berbasis Django Beserta Responnya

![Bagan](./images/bagan.png)

Alur permintaan di aplikasi Django dimulai ketika `Client` mengirimkan request ke server Django. Pertama-tama, urls.py menentukan fungsi mana di views.py yang harus menangani request tersebut. Setelah permintaan diarahkan ke fungsi yang tepat di views.py, fungsi ini akan memproses data dan, jika diperlukan, bekerja dengan models.py untuk `read` atau `write` data di database. Setelah pemrosesan selesai, views.py akan menggunakan template HTML yang ada di folder templates untuk merender tampilan akhir. Hasil dari render ini kemudian dikirim kembali ke `Client` sebagai respons HTTP dari server Django.

### Fungsi Git Dalam Pengembangan Perangkat Lunak

Git adalah _version control system_ yang sangat penting dalam pengembangan perangkat lunak. Dengan menggunakan git, _developer_ dapat melacak perubahan yang terjadi pada proyek, berkolaborasi dengan _developer_ lain, dan mengelola proyek secara efisien melalui berbagai fitur yang ditawarkan. Beberapa fitur git adalah sebagai berikut:

- **Version Control:** 
  Git mencatat setiap perubahan pada kode, memungkinkan _developer_ untuk mengakses versi sebelumnya kapan saja, yang sangat membantu dalam mengatur perubahan.

- **Kolaborasi:** 
  Dengan fitur _branching_, beberapa _developer_ dapat bekerja pada proyek yang sama tanpa mengganggu satu sama lain, dan kemudian   menggabungkan hasilnya melalui proses merging.

- **Distribusi:** 
  _Developer_ dapat bekerja secara lokal tanpa koneksi internet dan melakukan sinkronisasi dengan repositori pusat saat sudah tersedia akses, menjadikan Git alat yang fleksibel dalam berbagai situasi.

### Kenapa Django Dijadikan Permulaan Pengembangan Perangkat Lunak?

Django dijadikan permulaan perangkat lunak karena bisa dibilang lebih _beginner-friendly_. Django mengikuti konsep MVT (Model-View_Template) yang memisahkan data, tampilan, _templating_, dan _routing_ aplikasi, sehingga membantu pemula memahami struktur aplikasi web dengan lebih mudah. Django menangani banyak kerepotan dalam pengembangan web, sehingga pemula dapat fokus pada pembuatan aplikasi tanpa perlu menciptakan ulang hal-hal yang sudah ada. Selain hal ini,Django juga memiliki ekosistem yang lengkap dan komunitas besar yang mendukung pemula dalam mempelajari Django. 

### Mengapa model pada Django disebut sebagai _Object-Relational Mapping_ (ORM)?

Model pada Django disebut sebagai _Object-Relational Mapping_ (ORM) karena memungkinkan _developer_ untuk berinteraksi dengan database relasional menggunakan objek Python. Dengan menggunakan model Django, _developer_ dapat mengatur database melalui objek Python, tanpa harus menulis _query_ SQL secara langsung. ORM memetakan tabel-tabel di database ke dalam objek Python, sehingga pengelolaan data menjadi lebih mudah dan efisien.