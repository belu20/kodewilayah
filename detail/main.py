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

        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, 'td')
            
            if len(columns) >= 2:  # Pastikan ada kolom yang cukup
                wilayah = {
                    'kode_kabupaten': columns[0].text.strip(),  # Kolom pertama: Nama wilayah
                    'nama_kabupaten': columns[1].text.strip(),  # Kolom kedua: Kode wilayah
                    'datetime':current_datetime
                    # Tambahkan kolom lain sesuai dengan data yang Anda inginkan
                }
                wilayah_list.append(wilayah)
        return wilayah_list
        

    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil data dari {url}: {e}")
        return []

# Loop untuk mengakses URL dari kodewilayah.id/11 hingga kodewilayah.id/92
for i in range(11, 93):
    url = f"https://kodewilayah.id/{i}"
    wilayah_data = scrape_data(url)

    if wilayah_data :
        try:
            collection.insert_many(wilayah_data)
            print("Berhasil memasukan data")
        except Exception as e:
            print(f"terjadi kesalahan : {e}")
    
    # Tampilkan hasilnya jika ada data yang ditemukan
    # if wilayah_data:
    #     print(f"Data dari {url}:")
    #     for data in wilayah_data:
    #         print(data)

# Tutup browser setelah selesai
driver.quit()