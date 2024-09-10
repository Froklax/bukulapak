# Bukulapak
Number 1 online bookstore in Pacil!!!

### Deployment
Live web app : [Bukulapak](http://bertrand-gwynfory-bukulapak.pbp.cs.ui.ac.id/)

## Pertanyaan dan Jawaban

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

![Bagan](/bagan.png)

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