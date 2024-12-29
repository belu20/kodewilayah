import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import re
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
from concurrent.futures import ThreadPoolExecutor
# Memanggil fungsi untuk menghubungkan ke MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Anda bisa mengganti URI jika diperlukan

db = client['crawler_wilayah']
collection = db['kecamatan']