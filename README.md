# Bukulapak
Number 1 online bookstore in Pacil!!!

### Deployment
Live web app : [Bukulapak](http://bertrand-gwynfory-bukulapak.pbp.cs.ui.ac.id/)

### Fast Links
- [Tugas 6](#tugas-6)
- [Tugas 5](#tugas-5)
- [Tugas 4](#tugas-4)
- [Tugas 3](#tugas-3)
- [Tugas 2](#tugas-2)

## Tugas 6

### Jelaskan manfaat dari penggunaan JavaScript dalam pengembangan aplikasi web!

JavaScript memberikan banyak manfaat dalam pengembangan aplikasi web. Dengan JavaScript, kita bisa membuat aplikasi yang lebih interaktif dan _responsive_, memungkinkan _user_ berinteraksi dengan halaman web tanpa perlu me-refresh seluruh halaman. Kemampuan JavaScript untuk memanipulasi DOM secara dinamis memungkinkan kita mengubah konten dan tampilan halaman secara _real-time_. Selain itu, JavaScript memungkinkan validasi form di sisi _client_ yang dapat meningkatkan kecepatan respons dan mengurangi beban server. Melalui AJAX, JavaScript juga memudahkan komunikasi _asynchronous_ dengan server, sehingga kita bisa memperbarui data tanpa mengganggu pengalaman _user_. JavaScript juga menjadi dasar untuk pengembangan Single Page Applications (SPA) yang memberikan pengalaman seperti aplikasi desktop dalam browser web. JavaScript juga bersifat lintas platform yang memungkinkan aplikasi web kita berjalan di berbagai browser dan perangkat.

### Jelaskan fungsi dari penggunaan `await` ketika kita menggunakan `fetch()`! Apa yang akan terjadi jika kita tidak menggunakan `await`?

`await` digunakan untuk menunggu hasil dari operasi _asynchronous_ sebelum melanjutkan eksekusi kode berikutnya. Ketika kita menggunakan `fetch()`, kita menggunakannya dengan `await` untuk menunggu _response_ dari server sebelum melanjutkan. Jika kita tidak menggunakan await, kode berikutnya akan dieksekusi sebelum `fetch()` selesai yang dapat menyebabkan terdapat data yang tidak lengkap dan membuat sebuah kesalahan. 

### Mengapa kita perlu menggunakan _decorator_ `csrf_exempt` pada _view_ yang akan digunakan untuk AJAX `POST`?

`csrf_exempt` digunakan untuk "_exempt_" atau mengecualikan perlindungan CSRF (Cross-Site Request Forgery) pada _view_ yang digunakan untuk AJAX `POST`. Ini dilakukan karena AJAX `POST` request biasanya tidak menyertakan `csrf_token` secara otomatis, dimana server akan menolak request tersebut karena tidak ada `csrf_token`. Dengan menggunakan `csrf_exempt`, ini memungkinkan request AJAX `POST` diterima tanpa verifikasi CSRF. 

###  Pada tutorial PBP minggu ini, pembersihan data input pengguna dilakukan di belakang (_backend_) juga. Mengapa hal tersebut tidak dilakukan di _frontend_ saja?

Pembersihan data input pengguna dilakukan di _backend_ dan tidak pada _frontend_ saja untuk memastikan keamanan  data yang diterima oleh server. Meskipun pembersihan data di _frontend_ dapat membantu meningkatkan pengalaman pengguna dengan memberikan _feedback_ langsung, hal ini tidak cukup untuk melindungi aplikasi dari serangan berbahaya. _User_ yang jahat dapat memanipulasi data sebelum dikirim ke server, sehingga validasi dan pembersihan di _frontend_ saja tidak dapat diandalkan. Dengan melakukan pembersihan data di _backend_, kita dapat memastikan bahwa semua data yang masuk telah melalui proses validasi yang ketat dan konsisten untuk melindungi aplikasi dari serangan seperti SQL injection dan XSS (Cross-Site Scripting), yang bisa saja tidak terdeteksi oleh validasi _frontend_. Selain itu, pembersihan data di _backend_ juga memastikan bahwa data yang disimpan dan diproses oleh aplikasi selalu dalam format yang benar dan aman.

### Langkah Implementasi Checklist

1. **Implementasi AJAX GET**

- Pertama, saya mengubah fungsi `show_json` dan `show_xml` agar memfilter data buku berdasarkan _user_ yang sudah _logged-in_.

```python
   def show_xml(request):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

   def show_json(request):
      data = Product.objects.filter(user=request.user)
      return HttpResponse(serializers.serialize("json", data), content_type="application/json")
```

- Selanjutnya, saya membuat fungsi JavaScript baru pada `main.html` bernama `getBookEntries` untuk melakukan _request_ AJAX `GET`. Fungsi ini menggunakan API `fetch()` untuk mengirim _request_ URL  yang sesuai dengan funsi `show_json`.

```JAVASCRIPT
   async function getBookEntries(){
      return fetch("{% url 'main:show_json' %}").then((res) => res.json())
   }
```

- Terakhir, saya menambahkan `div` dengan `id="book_entry_cards"` dan membuat fungsi JavaScript bernama `refreshBookEntries` pada `main.html`. Fungsi ini menggunakan `await getBookEntries()` untuk mendapatkan data buku terbaru secara _asynchronous_. Fungsi ini juga memiliki string html yang memuat `card` buku yang menampilkan data berdasarkan hasil dari AJAX `GET` yaitu `fetch` yang dilakukan oleh `getBookEntries`. Fungsi ini juga memperbarui elemen `book_entry_cards` dengan kelas CSS dan konten HTML yang dibuat.

```HTML
   <div id="book_entry_cards"></div>
```

```JAVASCRIPT
   async function refreshBookEntries() {
    document.getElementById("book_entry_cards").innerHTML = "";
    document.getElementById("book_entry_cards").className = "";
    const bookEntries = await getBookEntries();
    let htmlString = "";
    let classNameString = "";

    if (bookEntries.length === 0) {
        classNameString = "flex flex-col items-center justify-center min-h-[24rem] p-6";
        htmlString = `
            <div class="flex flex-col items-center justify-center min-h-[24rem] p-6">
                <img src="{% static 'image/sedih-banget.png' %}" alt="Sad face" class="w-32 h-32 mb-4"/>
                <p class="text-center text-white mt-4">Belum ada data buku pada Bukulapak.</p>
            </div>
        `;
    }
    else {
        classNameString = "columns-1 sm:columns-2 lg:columns-3 gap-6 space-y-6 w-full"
        bookEntries.forEach((item) => {
            const name = DOMPurify.sanitize(item.fields.name);
            const description = DOMPurify.sanitize(item.fields.description);
            htmlString += `
            <div class="manrope relative break-inside-avoid">
                <div class="relative top-5 bg-gradient-to-r from-purple-300 via-indigo-400 to-violet-700 shadow-lg rounded-lg mb-6 break-inside-avoid flex flex-col border-2 border-indigo-300 transform hover:scale-105 transition-transform duration-300">
                    <div class="bg-gradient-to-r from-purple-400 to-violet-800 text-black p-4 rounded-t-lg border-b-2 border-indigo-300">
                        <h3 class="font-bold text-xl mb-2">${item.fields.name}</h3>
                        <p class="text-black">Rp. ${item.fields.price}</p>
                    </div>
                    <div class="p-4">
                        <p class="font-semibold text-lg mb-2">Description</p>
                        <p class="text-black">${item.fields.description}</p>
                        <div class="mt-4">
                            <p class="text-black font-semibold mb-2">Stock</p>
                            <div class="relative pt-1">
                                <div class="flex mb-2 items-center justify-between">
                                    <div>
                                        <span class="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-indigo-600 bg-indigo-200">
                                            ${item.fields.quantity}
                                        </span>
                                    </div>
                                </div>
                                <div class="overflow-hidden h-2 mb-4 text-xs flex rounded bg-indigo-200">
                                    <div style="width: ${item.fields.quantity > 10 ? 100 : item.fields.quantity * 10}%;" class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-indigo-500"></div>
                                </div>
                            </div>
                        </div>
                        <div class="flex justify-center space-x-4 mt-4">
                            <a href="/edit-book/${item.pk}" class="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 px-4 rounded-full transition duration-300 shadow-md">
                                <i class="fas fa-edit"></i> Edit
                            </a>
                            <a href="/delete/${item.pk}" class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-full transition duration-300 shadow-md">
                                <i class="fas fa-trash-alt"></i> Delete
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            `;
        });
    }
    document.getElementById("book_entry_cards").className = classNameString;
    document.getElementById("book_entry_cards").innerHTML = htmlString;
}
```

2. **Implementasi AJAX `POST`**

- 

3. **Mengubah README.md.**

- Terakhir, saya mengubah `README.md` yang sebelumnya telah saya buat untuk menambahkan jawaban dari pertanyaan-pertanyaan yang diberikan pada Tugas 6.

## Tugas 5

### Jika terdapat beberapa CSS selector untuk suatu elemen HTML, jelaskan urutan prioritas pengambilan CSS selector tersebut!

Terdapat urutan prioritas (specificity) yang akan menentukan CSS selector yang akan digunakan jika terdapat banyak CSS selector yang digunakan pada suatu elemen HTML yang sama. Urutan prioritasnya adalah sebagai berikut:

1. **Inline Styles**: Style yang dimasukkan langsung ke dalam elemen HTML menggunakan atribut `style`.

2. **Id Selector**:  Selector yang menggunakan atribut `id` elemen, ditulis dengan tanda `#`.

3. **Class Selector**: Selector yang menggunakan atribut `class` elemen, ditulis dengan tanda `.`.

4. **Tag Selector**: Selector dengan prioritas terendah, langsung menggunakan tag HTML seperti `body`, `p`, dan `h1`.

5. **Browser Default**: Styles yang diterapkan oleh browser sebagai default.

### Mengapa responsive design menjadi konsep yang penting dalam pengembangan aplikasi web? Berikan contoh aplikasi yang sudah dan belum menerapkan responsive design!

Responsive design adalah konsep penting dalam pengembangan aplikasi web karena memungkinkan tampilan dan fungsi situs web menyesuaikan dengan berbagai ukuran layar dan perangkat yang diggunakan oleh _user_. Responsive design penting untuk memastikan pengalaman `user` yang konsisten dan optimal di berbagai ukuran layar berbeda seperti di desktop, tablet, dan _handphone_.

### Contoh Aplikasi yang Sudah Menerapkan Repsonsive Design:
- **Google**: Fitur untuk _searching_ tetap responsif di berbagai perangkat berbeda.
- **Twitter**: Menyediakan berbagai tampilan dan fungsionalitas yang menyesuaikan dengan perangkat yang digunakan.

### Contoh Aplikasi yang Belum Menerapkan Responsive Design:

- **Pacil Web Service**: Tidak ada support untuk perangkat _mobile_, sehingga tidak bisa melihat informasi proyek-proyek di PWS jika menggunakan perangkat _mobile_.

### Jelaskan perbedaan antara margin, border, dan padding, serta cara untuk mengimplementasikan ketiga hal tersebut!

- **Margin**: Ruang di luar elemen, antara elemen dengan elemen lainnya. Fungsinya untuk mengatur jarak antara suatu elemen dengan elemen lainnya.

- **Border**: Batasan yang mengelilingi elemen. Dapat digunakan untuk mengatur ruang antara margin dan padding, serta membuat sebuah border mengelilingi elemen seperti yang kita ketahui.

- **Padding**: Ruang di dalam elemen, antara konten dalam elemen border elemen tersebut. Padding digunakan untuk memberi jarak antara konten dan ujung elemen.

**Cara Implementasi:**
```CSS
   .container {
      margin: 5px;   /* Memberi jarak 5px antara .container dengan elemen lain*/
      border: 5px solid; /* Membuat border setebal 5px dan juga menambahkan ruang 5px antara margin dan padding*/
      padding: 5px;  /* Memberi jarak 5px antara konten dalam elemen dengan ujung elemen*/
   }
```

### Jelaskan konsep flex box dan grid layout beserta kegunaannya!

Flex box adalah model _layout_ satu dimensi untuk menyusun secara vertikal atau horizontal. Elemen ini akan "_flex_" yaitu akan membesar atau mengecil tergantung aturan yang didefinisikan. Flex box memungkinkan elemen di dalam _container_ untuk diatur secara otomatis tergantung dengan ukuran _viewport_, yang memudahkan kita untuk membuat _layout_ yang fleksibel dan responsif. 

Grid adalah model _layout_ dua dimensi yang memungkinkan kita untuk membuat _design_ yang lebih kompleks dengan baris dan kolom. Grid memungkinkan kita untuk menyusun item secara baris dan kolom. _Grid layout_ bagus dalam membagi halaman menjadi beberapa area utama, seperti header, konten utama, dan footer atau menentukan hubungan dalam hal ukuran, posisi, dan ruang yang diambil antara bagian.

### Langkah Implementasi Checklist

1. **Implementasikan fungsi untuk menghapus dan mengedit product.**

- Pertama, saya menambahkan fungsi baru bernama `edit_book` pada `views.py` yang akan digunakan untuk mengedit buku yang sudah ada sebelumnya.

```python
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
```

- Selanjutnya, saya juga membuat fungsi baru bernama  `delete_book` pada `views.py` yang akan digunakan untuk menghapus buku yang sudah ada sebelumnya.

```python
   def delete_book(request, id):
      # Get book berdasarkan id
      book = Product.objects.get(pk = id)
      # Hapus book
      book.delete()
      # Kembali ke halaman awal
      return HttpResponseRedirect(reverse('main:show_main'))
   ```

- Langkah terakhir, saya mengimport fungsi `edit_book` dan `delete_book` yang sudah saya buat sebelumnya dan menambahkan path url untuk mengakses fungsi-fungsi yang di-import tersebut pada `urls.py`.

```python
   from django.urls import path
   from main.views import show_main, create_book_entry, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user, edit_book, delete_book

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
   ]
```

2. **Kustomisasi desain pada template HTML menggunakan Tailwind**

- Pertama, saya menambahkan tag `<meta name="viewport">` untuk responsive terhadap perangkat mobile beserta dengan script Tailwind pada file `base.html`. Saya juga menambahkan _icons_ dari _font awesome_ dan font Manrope untuk membuat tampilan lebih menarik. 

```HTML
   <meta name="viewport" content="width=device-width, initial-scale=1">
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
   <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap">
   <script src="https://cdn.tailwindcss.com"></script>
```

- Kemudian, saya membuat sebuah file css baru bernama `global.css` untuk mengubah beberapa tampilan pada aplikasi saya.

```CSS
   .form-style form input, form textarea, form select {
      width: 100%;
      padding: 0.5rem;
      border: 2px solid #bcbcbc;
      border-radius: 0.375rem;
   }
   .form-style form input:focus, form textarea:focus, form select:focus {
      outline: none;
      border-color: #674ea7;
      box-shadow: 0 0 0 3px #674ea7;
   }
   @keyframes shine {
      0% { background-position: -200% 0; }
      100% { background-position: 200% 0; }
   }
   .animate-shine {
      background: linear-gradient(120deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.3));
      background-size: 200% 100%;
      animation: shine 3s infinite;
   }

   .manrope {
      font-family: 'Manrope', Tahoma, sans-serif;
   }
```

- Saya juga menambahkan `middleware` WhiteNoise pada `settings.py` agar _static files_ dapat diakses saat di deployment.

```python
   STATIC_URL = '/static/'
   if DEBUG:
      STATICFILES_DIRS = [
         BASE_DIR / 'static' # merujuk ke /static root project pada mode development
      ]
   else:
      STATIC_ROOT = BASE_DIR / 'static' # merujuk ke /static root project pada mode production
```

- Selanjutnya, saya mengubah tampilan pada `login.html`, `register.html`, dan `create_book_entry.html` menjadi lebih menarik menggunakan Tailwind.

Tampilan login.html:

```HTML
   {% extends 'base.html' %}

   {% block meta %}
   <title>Login to Bukulapak</title>
   {% endblock meta %}

   {% block content %}
   <div class="manrope min-h-screen flex items-center justify-center w-screen bg-blue-950 py-12 px-4 sm:px-6 lg:px-8">
      <div class="container mb-20 bg-violet-900 max-w-md w-full space-y-8 p-12 rounded-lg shadow-lg">
         <div>
            <h2 class="mt-6 text-center text-3xl font-extrabold text-white">
               Login to Bukulapak
            </h2>
         </div>
         <form class="mt-8 space-y-6" method="POST" action="">
            {% csrf_token %}
            <input type="hidden" name="remember" value="true">
            <div class="rounded-md shadow-sm -space-y-px">
               <div class="mb-4">
                  <label for="username" class="sr-only">Username</label>
                  <input id="username" name="username" type="text" required class="appearance-none rounded-full relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Username">
               </div>
               <div>
                  <label for="password" class="sr-only">Password</label>
                  <input id="password" name="password" type="password" required class="appearance-none rounded-full relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="Password">
               </div>
            </div>
         
            <div>
               <button type="submit" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-full text-white bg-blue-600 hover:bg-blue-950 hover:opacity-80 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-300 ease-in-out">
                  Sign in
               </button>
            </div>
         </form>    

         {% if messages %}
         <div class="mt-4">
            {% for message in messages %}
            {% if message.tags == "success" %}
                  <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
                     <span class="block sm:inline">{{ message }}</span>
                  </div>
            {% elif message.tags == "error" %}
                  <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                     <span class="block sm:inline">{{ message }}</span>
                  </div>
            {% else %}
                  <div class="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded relative" role="alert">
                     <span class="block sm:inline">{{ message }}</span>
                  </div>
            {% endif %}
            {% endfor %}
         </div>
         {% endif %}

         <div class="text-center mt-4">
            <p class="text-lg text-white">
               Don't have an account yet?
               <a href="{% url 'main:register' %}" class="font-medium text-indigo-200 hover:text-indigo-300">
                  Register Now
               </a>
            </p>
         </div>
      </div>
   </div>
   {% endblock content %}
```

Tampilan `register.html`:

```HTML
   {% extends 'base.html' %}

   {% block meta %}
   <title>Register</title>
   {% endblock meta %}

   {% block content %}
   <div class="manrope min-h-screen flex items-center justify-center bg-blue-950 py-12 px-4 sm:px-6 lg:px-8">
      <div class="container mb-20 bg-violet-900 rounded-lg max-w-lg w-full p-12 space-y-8 form-style">
         <div>
            <h2 class="mt-3 text-center text-3xl font-extrabold text-white">
               Create your account
            </h2>
         </div>
         <form class="mt-8 space-y-6" method="POST">
            {% csrf_token %}
            <input type="hidden" name="remember" value="true">
            <div class="rounded-lg shadow-sm -space-y-px">
               {% for field in form %}
                  <div class="{% if not forloop.first %}mt-4{% endif %}">
                     <label for="{{ field.id_for_label }}" class="mb-4 text-white font-extrabold text-base">
                        {{ field.label }}
                     </label>
                     <div class="relative mt-1 mb-3">
                        {{ field }}
                        <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                           {% if field.errors %}
                              <svg class="h-5 w-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                              </svg>
                           {% endif %}
                        </div>
                     </div>
                     {% if field.errors %}
                        {% for error in field.errors %}
                           <p class="mt-1 text-sm text-red-600">{{ error }}</p>
                        {% endfor %}
                     {% endif %}
                  </div>
               {% endfor %}
            </div>

            <div>
               <button type="submit" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-full text-white bg-blue-600 hover:bg-blue-950 hover:opacity-80 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-300 ease-in-out">
                  Register
               </button>
            </div>
         </form>

         {% if messages %}
         <div class="mt-4">
            {% for message in messages %}
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <span class="block sm:inline">{{ message }}</span>
            </div>
            {% endfor %}
         </div>
         {% endif %}

         <div class="text-center mt-4">
            <p class="text-lg text-white">
               Already have an account?
               <a href="{% url 'main:login' %}" class="font-medium text-indigo-200 hover:text-indigo-300">
                  Login here
               </a>
            </p>
         </div>
      </div>
   </div>
   {% endblock content %}
```

Tampilan `create_book_entry.html`:

```HTML
   {% extends 'base.html' %}
   {% load static %}
   {% block meta %}
   <title>Add Book</title>
   {% endblock meta %}

   {% block content %}
   {% include 'navbar.html' %}

   <div class="manrope flex flex-col min-h-screen bg-blue-950">
      <div class="container mx-auto px-4 py-8 mt-16 max-w-xl">
         <h1 class="text-3xl font-bold text-center mb-8 text-white">Add New Book</h1>
      
         <div class="bg-violet-900    shadow-md rounded-lg p-6 form-style">
            <form method="POST" class="space-y-6">
               {% csrf_token %}
               {% for field in form %}
                  <div class="flex flex-col">
                     <label for="{{ field.id_for_label }}" class="mb-2 font-semibold text-white">
                        {{ field.label }}
                     </label>
                     <div class="w-full">
                        {{ field }}
                     </div>
                     {% if field.help_text %}
                        <p class="mt-1 text-sm text-gray-500">{{ field.help_text }}</p>
                     {% endif %}
                     {% for error in field.errors %}
                        <p class="mt-1 text-sm text-red-600">{{ error }}</p>
                     {% endfor %}
                  </div>
               {% endfor %}
               <div class="flex justify-center mt-6">
                  <button type="submit" class="text-white font-semibold px-6 py-3 rounded-full bg-blue-600 hover:bg-blue-950 hover:opacity-80 transition duration-300 ease-in-out w-full">
                     Add New Book
                  </button>
               </div>
            </form>
         </div>
      </div>
   </div>

   {% endblock %}
```

- Selanjutnya, saya kustomisasi halaman daftar produk, yaitu halaman utama `main.html` menjadi lebih menarik dan responsif.

```HTML
   {% extends 'base.html' %}
   {% load static %}

   {% block meta %}
   <title>Bukulapak</title>
   {% endblock meta %}
   {% block content %}
   {% include 'navbar.html' %}
   <div class="manrope overflow-x-hidden px-4 md:px-8 pb-8 pt-24 min-h-screen bg-blue-950 flex flex-col">
      <div class="p-2 mb-6 relative">
         <div class="text-white text-2xl font-bold mb-6 ml-5">Created By</div>
         <div class="relative grid grid-cols-1 z-30 md:grid-cols-3 gap-8">
            {% include "card_info.html" with title='Name' value=person %}
            {% include "card_info.html" with title='NPM' value=npm %}
            {% include "card_info.html" with title='Class' value=class %}
         </div>
         <div class="w-full px-6 absolute top-[44px] left-0 z-20 hidden md:flex mt-14">
            <div class="w-full min-h-4 bg-indigo-700">
            </div>
         </div>
      </div>
      <div class="px-3 mb-4">
         <div class="flex rounded-md items-center bg-indigo-600 py-2 px-4 w-fit">
            <h1 class="text-white text-center">Last Login: {{last_login}}</h1>
         </div>
      </div>
      <div class="flex justify-between items-center mb-6 mt-20">
         <h2 class="text-2xl font-bold text-white ml-5">Available Books</h2>
         <a href="{% url 'main:create_book_entry' %}" class="bg-blue-600 hover:bg-blue-700 hover:opacity-80 text-white font-bold py-2 px-4 rounded-full transition duration-300 ease-in-out transform hover:scale-105">
            <i class="fas fa-plus mr-2"></i>Add New Book
         </a>
      </div>
      
      <div class="container mx-auto bg-violet-900 rounded-xl w-full max-w-full p-20">
         {% if not books %}
         <div class="flex flex-col items-center justify-center min-h-[24rem] p-6">
            <img src="{% static 'image/sedih-banget.png' %}" alt="Sad face" class="w-32 h-32 mb-4"/>
            <p class="text-center text-white mt-4">Belum ada data buku pada Bukulapak.</p>
         </div>
         {% else %}
         <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 w-full">
            {% for book_entry in books %}
            {% include 'card_book.html' with book_entry=book_entry %}
            {% endfor %}
         </div>
         {% endif %}
      </div>
   </div>
   {% endblock content %}
```

- Jika tidak ada buku yang terdaftar, saya menampilkan gambar dan pesan bahwa tidak ada buku yang terdaftar dengan bagian kode dibawah ini:

```HTML
   {% if not books %}
   <div class="flex flex-col items-center justify-center min-h-[24rem] p-6">
         <img src="{% static 'image/sedih-banget.png' %}" alt="Sad face" class="w-32 h-32 mb-4"/>
         <p class="text-center text-white mt-4">Belum ada data buku pada Bukulapak.</p>
   </div>
```
- Jika terdapat buku yang terdaftar, maka saya menampikannya menggunakan card yang sudah saya buat pada `card_book.html` seperti berikut:
```HTML
   <div class="manrope relative break-inside-avoid">
      <div class="relative top-5 bg-gradient-to-r from-purple-300 via-indigo-400 to-violet-700 shadow-lg rounded-lg mb-6 break-inside-avoid flex flex-col border-2 border-indigo-300 transform hover:scale-105 transition-transform duration-300">
         <div class="bg-gradient-to-r from-purple-400 to-violet-800 text-black p-4 rounded-t-lg border-b-2 border-indigo-300">
            <h3 class="font-bold text-xl mb-2">{{book_entry.name}}</h3>
            <p class="text-black">Rp. {{book_entry.price}}</p>
         </div>
         <div class="p-4">
            <p class="font-semibold text-lg mb-2">Description</p>
            <p class="text-black">{{book_entry.description}}</p> 
            <div class="mt-4">
               <p class="text-black font-semibold mb-2">Stock</p>
               <div class="relative pt-1">
                  <div class="flex mb-2 items-center justify-between">
                     <div>
                     <span class="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-indigo-600 bg-indigo-200">
                        {{book_entry.quantity}}
                     </span>
                     </div>
                  </div>
                  <div class="overflow-hidden h-2 mb-4 text-xs flex rounded bg-indigo-200">
                     <div style="width:{% if book_entry.quantity > 10 %}100%{% else %}{{ book_entry.quantity }}0%{% endif %}" class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-indigo-500"></div>
                  </div>
               </div>
            </div>
            <div class="flex justify-center space-x-4 mt-4">
               <a href="{% url 'main:edit_book' book_entry.pk %}" class="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 px-4 rounded-full transition duration-300 shadow-md">
                  <i class="fas fa-edit"></i> Edit
               </a>
               <a href="{% url 'main:delete_book' book_entry.pk %}" class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-full transition duration-300 shadow-md">
                  <i class="fas fa-trash-alt"></i> Delete
               </a>
            </div>
         </div>
      </div>
   </div>
```
- dan pada `main.html` sebagai berikut:

```HTML
   {% else %}
   <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 w-full">
      {% for book_entry in books %}
         {% include 'card_book.html' with book_entry=book_entry %}
      {% endfor %}
   </div>
   {% endif %}
```

- Saya juga menambahkan button untuk mengedit dan menghapus buku pada _card_ pada bagian ini di `card_book.html`:

```HTML
   <div class="flex justify-center space-x-4 mt-4">
      <a href="{% url 'main:edit_book' book_entry.pk %}" class="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 px-4 rounded-full transition duration-300 shadow-md">
         <i class="fas fa-edit"></i> Edit
      </a>
      <a href="{% url 'main:delete_book' book_entry.pk %}" class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-full transition duration-300 shadow-md">
         <i class="fas fa-trash-alt"></i> Delete
      </a>
   </div>
```

- Terakhir, saya membuat sebuah navigation bar yang responsif terhadap ukuran device. Navigation bar berisi logo Bukulapak, _navigation links_, nama _user_ yang sedang logged in, dan tombol logout. Navigation bar ini akan ditampilkan pada `main.html`, `create_book_entry.html`, dan `edit_book.html`.

```HTML
   <nav class="bg-violet-900 shadow-lg fixed top-0 left-0 z-40 w-screen">
      <div class="w-full px-4 sm:px-6 lg:px-8">
         <div class="flex items-center justify-between h-16">
            <!-- Logo Bukulapak -->
            <div class="flex-shrink-0">
               <h1 class="manrope text-2xl font-bold text-white">Bukulapak</h1>
            </div>
            
            <!-- Navigasi tengah -->
            <div class="hidden md:flex justify-center flex-grow ml-20">
               <nav class="manrope nav-links flex space-x-4">
                  <a href="{% url 'main:show_main' %}" class="text-white text-lg hover:bg-blue-950 px-3 py-2 rounded-md transition duration-300 hover:scale-110">Home</a>
                  <a href="#" class="text-white text-lg hover:bg-blue-950 px-3 py-2 rounded-md transition duration-300 hover:scale-105">Products</a>
                  <a href="#" class="text-white text-lg hover:bg-blue-950 px-3 py-2 rounded-md transition duration-300 hover:scale-105">Categories</a>
                  <a href="#" class="text-white text-lg hover:bg-blue-950 px-3 py-2 rounded-md transition duration-300 hover:scale-105">Cart</a>
               </nav>
            </div>

            <!-- User info dan logout -->
            <div class="hidden md:flex items-center">
               {% if user.is_authenticated %}
                  <div class="flex items-center gap-2">
                     <i class="fas fa-user text-white"></i>
                     <span class="manrope text-white mr-4 text-lg">{{ user.username }}</span>
                  </div>
                  <a href="{% url 'main:logout' %}" class="manrope bg-blue-600 hover:bg-blue-950 hover:opacity-80 text-white font-bold py-2 px-4 rounded-full transition duration-300 hover:scale-105">
                     <i class="fas fa-sign-out-alt mr-2"></i>
                     Logout
                  </a>
               {% else %}
                  <a href="{% url 'main:login' %}" class="text-center bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition duration-300 mr-2">
                     Login
                  </a>
                  <a href="{% url 'main:register' %}" class="text-center bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded transition duration-300">
                     Register
                  </a>
               {% endif %}
            </div>
            <div class="md:hidden flex items-center">
               <button class="mobile-menu-button">
                  <svg class="w-6 h-6 text-white" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" stroke="currentColor">
                     <path d="M4 6h16M4 12h16M4 18h16"></path>
                  </svg>
               </button>
            </div>
         </div>
      </div>
      <!-- Mobile menu -->
      <div class="manrope mobile-menu hidden md:hidden px-4 w-full md:max-w-full">
         <div class="pt-2 pb-3 space-y-1 mx-auto">
            <a href="{% url 'main:show_main' %}" class="block text-white text-lg hover:bg-blue-950 px-3 py-2 rounded-md transition duration-300">Home</a>
            <a href="#" class="block text-white text-lg hover:bg-blue-950 px-3 py-2 rounded-md transition duration-300">Products</a>
            <a href="#" class="block text-white text-lg hover:bg-blue-950 px-3 py-2 rounded-md transition duration-300">Categories</a>
            <a href="#" class="block text-white text-lg hover:bg-blue-950 px-3 py-2 rounded-md transition duration-300">Cart</a>
            {% if user.is_authenticated %}
               <div class="flex items-center gap-2 px-3 py-2">
                  <i class="fas fa-user text-white"></i>
                  <span class="text-white text-base font-medium">{{ user.username }}</span>
               </div>
               <a href="{% url 'main:logout' %}" class="block text-center bg-blue-600 hover:bg-blue-950 hover:opacity-80 text-white font-bold py-2 px-4 rounded transition duration-300">
                  Logout
               </a>
            {% else %}
               <a href="{% url 'main:login' %}" class="block text-center bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition duration-300 mb-2">
                  Login
               </a>
               <a href="{% url 'main:register' %}" class="block text-center bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded transition duration-300">
                  Register
               </a>
            {% endif %}
         </div>
      </div>

      <script>
         const btn = document.querySelector("button.mobile-menu-button");
         const menu = document.querySelector(".mobile-menu");

         btn.addEventListener("click", () => {
            menu.classList.toggle("hidden");
         });
      </script>
   </nav>
```

3. **Mengubah README.md.**

- Terakhir, saya mengubah `README.md` yang sebelumnya telah saya buat untuk menambahkan jawaban dari pertanyaan-pertanyaan yang diberikan pada Tugas 5.

## Tugas 4

### Apa perbedaan antara `HttpResponseRedirect()` dan `redirect()`

`HttpResponseRedirect()` dan `redirect()` sebenarnya mempunyai return value yang sama yaitu keduanya akan mengembalikan sebuah `HttpResponseRedirect` yang mengarahkan user ke URL yang ditentukan. Perbedaannya berada pada parameter yang diperbolehkan, `HttpResponseRedirect()` hanya menerima sebuah URL sebagai parameter dalam methodnya, sedangkan `redirect()` memperbolehkan URL, objek model, atau view sebagai parameter dalam method. Oleh karena itu, `redirect()` bisa dibilang lebih fleksibel daripada HttpResponseRedirect().

### Cara kerja penghubungan model Product dengan `User`!

`User` adalah model bawaan dari Django yang memiliki field bawaan username, password, email, first_name, dan last_name.  Model `User` digunakan oleh sistem _authentication_ dan _authorization_ Django untuk mengelola login, logout, dan izin pengguna. Untuk menghubungkan model `Product` dengan `User`, kita bisa menggunakan `ForeignKey` yang akan mendefinisikan _many-to-one relationship_. Dalam model `Product` yang sudah dibuat, `ForeignKey` digunakan untuk menghubungkan setiap `Product` dengan satu `User`. Setiap `Product` akan terkait dengan satu `User`, tetapi satu `User` bisa memiliki banyak `Product`. 

```python
   from django.db import models
   from django.contrib.auth.models import User
   import uuid

   class Product(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
      name = models.CharField(max_length=255)
      price = models.IntegerField()
      description = models.TextField()
      quantity = models.IntegerField()
```

### Apa perbedaan antara _authentication_ dan _authorization_, apakah yang dilakukan saat pengguna login? Jelaskan bagaimana Django mengimplementasikan kedua konsep tersebut.

_Authentication_ adalah proses verifikasi identitas user. Saat pengguna login, mereka memasukkan kredensial seperti username dan password yang kemudian diverifikasi oleh sistem untuk memastikan bahwa mereka adalah pengguna yang valid. Tujuan utama dari _authentication_ adalah untuk memastikan bahwa pengguna yang mencoba mengakses sistem adalah benar-benar orang yang mereka nyatakan.

_Authorization_ adalah proses menentukan hak akses pengguna setelah mereka berhasil _authenticated_. Setelah pengguna login dan identitas pengguna diverifikasi, _authorization_ menentukan apa yang dapat dilakukan atau diakses oleh pengguna tersebut dalam sistem. Seorang pengguna dengan _role_ _admin_ mungkin memiliki akses penuh ke semua sistem, sementara pengguna dengan _role_ _user_ biasa hanya memiliki akses terbatas.

Untuk _authentication_, Django menyediakan model `User` yang menyimpan informasi pengguna, serta _form_ dan _view_ bawaan seperti `UserCreationForm` dan `AuthenticationForm` yang merupakan bagian dari _module_ `django.contrib.auth`  untuk menangani registrasi dan login pengguna. Saat pengguna login, Django menggunakan _middleware_ untuk menghubungkan pengguna yang terautentikasi dengan setiap _request_. Proses ini memastikan bahwa hanya pengguna yang valid yang dapat mengakses sistem.

Untuk authorization, Django menggunakan sistem authorization bawaaan django yang merupakan bagian dari _module_ `django.contrib.auth`. Sistem ini memungkinkan _developer_ memberikan hak akses tertentu kepada pengguna menggunakan _decorators_ seperti `@permission_required`, `@login_required` atau sebuah _method_ seperti `user.has_perm()`. Setelah pengguna berhasil diautentikasi, Django menentukan hak akses berdasarkan _permission_ yang telah ditetapkan.

### Bagaimana Django mengingat pengguna yang telah login? Jelaskan kegunaan lain dari cookies dan apakah semua cookies aman digunakan?

Django menggunakan _sessions_ dan _cookies_ untuk mengingat pengguna yang telah login. Saat pengguna login, Django membuat _session_ baru dan menyimpan ID _session_ di _cookie_ browser pengguna. Ketika pengguna membuat _request_ baru, _cookie_ ini dikirim ke server yang memungkinkan Django untuk mengidentifikasi pengguna yang sedang login.

**Kegunaan Lain Cookies**:
- _Cookies_ dapat digunakan untuk menyimpan preferensi dari pengguna .
- Melacak data sementara yang berguna tanpa mengharuskan pengguna untuk login.
- `csrf_token` disimpan dalam _cookie_, yang membantu verifikasi _form_ mana yang berasal dari pengguna asli.

Tidak semua _cookie_ dapat dikatakan aman. _Cookies_ yang tidak dikirim melalui saluran yang aman seperti tanpa menggunakan HTTPS dapat dicuri oleh penyerang yang memungkinkan _session hijacking_ dimana penyerang menyamar sebagai pengguna dengan menggunakan _session_ ID pengguna tersebut. _Cookies_ yang tidak dilindungi bisa rentan terharap _Cross-Site Scripting (XSS)_ dimana _script_ jahat dapat mengakses _cookie_ dan masuk ke sistem.

### Langkah Implementasi Checklist

1. **Mengimplementasikan fungsi registrasi, login, dan logout.**

- Pertama saya mengimport `UserCreationForm` dan `messages` pada bagian paling atas `views.py` dan menambahkan fungsi baru bernama `register`.

```python
   from django.contrib.auth.forms import UserCreationForm
   from django.contrib import messages

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
```

- Kemudian saya membuat file HTML baru bernama `register.html` pada direktori `main/templates` dengan isi sebagai berikut:

```HTML
   {% extends 'base.html' %}

   {% block meta %}
   <title>Register</title>
   {% endblock meta %}

   {% block content %}

   <div class="register">
   <h1 class="form-title">Register Form</h1>

   <form method="POST">
      {% csrf_token %}
      <table>
         {{ form.as_table }}
         <tr>
         <td></td>
         <td><input class="btn" type="submit" name="submit" value="Daftar" /></td>
         </tr>
      </table>
   </form>

   {% if messages %}
   <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
   </ul>
   {% endif %}
   </div>

   {% endblock content %}
```

- Selanjutnya saya mengimport `authenticate`, `login`, dan `AuthenticationForm` pada bagian paling atas `views.py` dan menambahkan fungsi baru bernama `login_user`.

```python
   from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
   from django.contrib.auth import authenticate, login

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
         form = AuthenticationForm(request)
      context = {'form': form}
      return render(request, 'login.html', context)
```

- Sama seperti untuk `register`, saya juga membuat file HTML baru bernama `login.html` pada direktori `main/templates` dengan isi sebagai berikut:

```HTML
   {% extends 'base.html' %}

   {% block meta %}
   <title>Login</title>
   {% endblock meta %}

   {% block content %}
   <div class="login">
   <h1 class="form-title">Login to Bukulapak</h1>

   <form method="POST" action="" class="login-form">
      {% csrf_token %}
      <table class="form-table">
         {{ form.as_table }}
         <tr>
         <td></td>
         <td class="login-btn"><input class="btn login_btn" type="submit" value="Login" /></td>
         </tr>
      </table>
   </form>

   {% if messages %}
   <ul>
      {% for message in messages %}
      <li>{{ message }}</li>
      {% endfor %}
   </ul>
   {% endif %} 
   <div class="register-section">
      Don't have an account yet? <a href="{% url 'main:register' %}" class="register-btn">Register Now</a>
   </div>
   </div>

   {% endblock content %}
```

- Untuk fungsi `logout`, sama seperti sebelumnya saya menambahkan import baru bernama `logout` pada bagian atas `views.py` dan menambahkan fungsi baru bernama `logout_user`.

```python
   def logout_user(request):
      logout(request)
      response = HttpResponseRedirect(reverse('main:login'))
      response.delete_cookie('last_login')
      return response
```

- Setelah saya membuat fungsi `logout_user`, saya menambahkan button untuk logout ke `main.html` sebagai berikut:

```HTML
   <a href="{% url 'main:logout' %}">
      <button>Logout</button>
   </a>
```

- Langkah terakhir, saya mengimport fungsi `register`, `login_user`, dan `logout_user` yang sudah saya buat sebelumnya menambahkan path url untuk mengakses fungsi-fungsi yang di-import tersebut pada `urls.py`.

```python
   from django.urls import path
   from main.views import show_main, create_book_entry, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user

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
   ]
```

2. **Membuat dua akun pengguna dengan masing-masing tiga dummy data menggunakan model yang telah dibuat pada aplikasi sebelumnya untuk setiap akun di lokal.**

- Saya membuat dua akun bernama cbkadal dan Bertrand pada lokal yang masing-masing berisi tiga dummy data menggunakan model yang telah dibuat sebelumnya (Purcell Kalkulus dan Rosen Matdis saya tetapkan sebagai produk default).

**Akun cbkadal:**

![cbkadal](./images/cbkadal-image.png)

**Akun Bertrand:**

![Bertrand](./images/Bertrand-image.png)

3. **Menghubungkan model `Product` dengan `User`.**

   Untuk menghubungkan model `Product` dengan `User`, saya menggunakan `ForeignKey` yang mendefinisikan _many-to-one relationship_. Saya menggunakan `ForeignKey` untuk menghubungkan setiap `Product` dengan satu `User` yang dimana `Product` akan terkait dengan satu `User`, tetapi satu `User` bisa memiliki banyak `Product`.

```python
   from django.db import models
   from django.contrib.auth.models import User
   import uuid

   class Product(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
      name = models.CharField(max_length=255)
      price = models.IntegerField()
      description = models.TextField()
      quantity = models.IntegerField()
```

4. **Menampilkan detail informasi pengguna yang sedang logged in seperti username dan menerapkan cookies seperti last login pada halaman utama aplikasi.**

- Saya menampilkan informasi pengguna yang sedang login pada halaman utama dengan menambahkan `request.user.username` pada `context` di fungsi `show_main()` pada `views.py`.

- Kemudian saya melakukan hal yang sama untuk menerapkan _cookies_ seperti last login pada halaman utama aplikasi, yaitu dengan menambahkan `'last_login': request.COOKIES['last_login']` pada `context` di `show_main()` yang akan menambahkan informasi _cookie_ _last_login_ pada response yang akan ditampilkan di halaman utama aplikasi.

```python
   context = { 
        'nama_user': request.user.username,
        'nama_aplikasi' : 'Bukulapak',
        'person' : 'Bertrand Gwynfory Iskandar',
        'npm' : '2306152121',
        'class' : 'PBP C',
        'books' : all_books,
        'last_login': request.COOKIES['last_login'],
    }
```

5. **Mengubah README.md.**

- Terakhir, saya mengubah `README.md` yang sebelumnya telah saya buat untuk menambahkan jawaban dari pertanyaan-pertanyaan yang diberikan pada Tugas 4.


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