from setting import *

# Setup opsi Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')  # Menjalankan browser di background tanpa tampilan UI
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Menginisialisasi WebDriver menggunakan webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def scrape_data(url):
    driver.get(url)
    time.sleep(5)  # Tunggu beberapa saat untuk memastikan halaman sepenuhnya dimuat

    wilayah_list = []
    try:
        # Mengambil data dari halaman
        rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')  # Menyesuaikan selector tabel

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, 'td')
            
            if len(columns) >= 2:  # Pastikan ada kolom yang cukup
                wilayah = {
                    'kode_desa': columns[0].text.strip(),  # Kolom pertama: kode
                    'nama_desa': columns[1].text.strip(),  # Kolom kedua: nama
                    'datetime':current_time # Waktu crawling 

                    # Tambahkan kolom lain sesuai dengan data yang Anda inginkan
                }
                wilayah_list.append(wilayah)
        return wilayah_list
    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil data dari {url}: {e}")
        return []

# Loop untuk mengakses URL dari kodewilayah.id/11.01 hingga kodewilayah.id/92.92
for i in range(11, 93):  # Mulai dari 11 hingga 92
    for j in range(1, 100):  # Mengubah angka setelah titik dari 01 hingga 99
        for x in list(range(1000, 1084)) + list(range(2000, 2117)):

            url = f"https://kodewilayah.id/{i:02d}.{j:02d}.{x:04d}"  # Format angka dengan 2 digit
            wilayah_data = scrape_data(url)

            if wilayah_data:
                try:
                    collection.insert_many(wilayah_data)
                    print(f"Berhasil memasukkan data dari {url}")
                except Exception as e:
                    print(f"Terjadi kesalahan saat memasukkan data dari {url}: {e}")
    
# Tutup browser setelah selesai
driver.quit()
