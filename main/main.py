from setting import *
# Setup opsi Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')  # Menjalankan browser di background tanpa tampilan UI
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Menginisialisasi WebDriver menggunakan webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Akses halaman yang ingin di-crawl
url = "https://kodewilayah.id/"
driver.get(url)

# Tunggu beberapa saat untuk memastikan halaman sepenuhnya dimuat
time.sleep(5)  # Anda bisa menggunakan WebDriverWait untuk menunggu elemen tertentu

# Mengambil data dari elemen <li>
wilayah_list = []
try:
    # Misalnya, kita ingin mengambil data dari <ul> atau <ol> yang berisi <li>
    items = driver.find_elements(By.XPATH, '//*[@id="app"]/div[2]/div[1]/ul/li') # Sesuaikan dengan selector <ul> dan <li> yang sesuai


    for x in items:
        data = x.find_element(By.XPATH, "a").text
        # Split data berdasarkan spasi, ambil angka sebagai kode_wilayah dan sisa sebagai nama_wilayah
        split_data = data.split(" ", 1)  # Split hanya sekali di spasi pertama
        kode_provinsi = split_data[0]
        nama_provinsi = split_data[1] if len(split_data) > 1 else ""  # Pastikan nama wilayah ada

        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Tambahkan ke dalam list wilayah_list
        wilayah_list.append({"kode_provinsi": kode_provinsi, "provinsi": nama_provinsi, "datetime":current_datetime})

except Exception as e:
    print(f"Terjadi kesalahan: {e}")

# Menampilkan hasil
# print(wilayah_list)

if wilayah_list:
    try:
        collection.insert_many(wilayah_list)  # Memasukkan data ke koleksi MongoDB
        print(f"Berhasil memasukkan {len(wilayah_list)} data ke MongoDB.")
    except Exception as e:
        print(f"Terjadi kesalahan saat memasukkan data ke MongoDB: {e}")
else:
    print("Tidak ada data untuk dimasukkan ke MongoDB.")
