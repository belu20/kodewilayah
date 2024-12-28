import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import re
from datetime import datetime
# Memanggil fungsi untuk menghubungkan ke MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Anda bisa mengganti URI jika diperlukan

db = client['crawler_wilayah']
collection = db['desa']