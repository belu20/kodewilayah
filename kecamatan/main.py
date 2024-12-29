from setting import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Setup opsi Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')  # Menjalankan browser di background tanpa tampilan UI
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Inisialisasi WebDriver
def start_driver():
    options = Options()
    options.add_argument("--headless")  # Untuk menjalankan browser tanpa GUI
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def check_page_for_data(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table tbody'))
        )
        # Mengambil tabel dari halaman
        rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
        
        # Jika tidak ada baris yang ditemukan, anggap halaman kosong
        if len(rows) == 0:
            print(f"URL {url} tidak memiliki data. Melewatkan.")
            return False
        return True
    except Exception as e:
        print(f"Terjadi kesalahan saat mengakses {url}: {e}")
        return False

# Fungsi untuk mengakses dan mengambil data
def scrape_data(url, driver):
    if not check_page_for_data(driver, url):
        return []

    wilayah_list = []
    try:
        # Menunggu dan mencari elemen yang relevan setelah memastikan halaman dimuat
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table tbody tr'))
        )

        # Mengambil tabel setelah memastikan halaman dimuat
        rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')  # Menyesuaikan selector tabel

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # for x in rows:
        #     nama_provinsi = x.find_element(By.XPATH, "td").text
        #     print(nama_provinsi)
        # Looping melalui baris dalam tabel dan ambil data
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, 'td')

            if len(columns) >= 2:  # Pastikan ada kolom yang cukup
                wilayah = {
                    'kode_kecamatan': columns[0].text.strip(),  # Kolom pertama: kode
                    'nama_kecamatan': columns[1].text.strip(),  # Kolom kedua: nama
                    'datetime': current_time  # Waktu crawling
                }
                wilayah_list.append(wilayah)
        return wilayah_list
    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil data dari {url}: {e}")
        return []

# Fungsi untuk men-scrape seluruh data
def scrape_all_data():
    driver = start_driver()

    for i in list(range(11, 21)) + list(range(31, 36)) + list(range(51, 53)) + list(range(61, 92)):  # Mulai dari 11 hingga 92
        for j in range(1, 89):  # Mengubah angka setelah titik dari 01 hingga 99
            url = f"https://kodewilayah.id/{i:02d}.{j:02d}"  # Format angka dengan 2 digit
            wilayah_data = scrape_data(url, driver)
            
            if wilayah_data:
                try:
                    # Asumsikan Anda sudah memiliki koneksi ke database MongoDB (misalnya, collection)
                    collection.insert_many(wilayah_data)
                    print(f"Berhasil memasukkan data dari {url}")
                except Exception as e:
                    print(f"Terjadi kesalahan saat memasukkan data dari {url}: {e}")

    driver.quit()  # Menutup driver setelah selesai

# Eksekusi scraping
scrape_all_data()