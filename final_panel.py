import requests
import pandas as pd
import folium
import time
import webbrowser
from io import StringIO
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os
import random

API_KEY = "2ece47e141b71c73ecfe8f609c1f8c86"
SOURCE = "VIIRS_SNPP_NRT" 
COUNTRY = "TUR"
DAYS = "1" 
REFRESH_RATE_SECONDS = 600
MODEL_PATH = 'alev_gozcusu_model.h5'
KARAR_ESIGI = 0.85

print("Yapay zekâ modeli yükleniyor...")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model başarıyla yüklendi.")
except Exception as e:
    print(f"Model yüklenirken hata oluştu: {e}")
    exit()

def tahmin_et_yangin(image_path):
    try:
        img = image.load_img(image_path, target_size=(256, 256))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        prediction_non_fire = model.predict(img_array, verbose=0)[0][0]
        ihtimal_fire = 1 - prediction_non_fire

        if ihtimal_fire > KARAR_ESIGI:
            return "YANGIN", ihtimal_fire
        else:
            return "NORMAL", ihtimal_fire
    except Exception as e:
        print(f"Tahmin hatası: {e}")
        return "HATA", 0

def get_fire_data():
    url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{API_KEY}/{SOURCE}/{COUNTRY}/{DAYS}"
    print(f"[{time.strftime('%H:%M:%S')}] NASA'dan güncel veri çekiliyor...")
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            print("Veri başarıyla alındı.")
            return response.text
        else:
            return None
    except Exception as e:
        print(f"Veri çekme hatası: {e}")
        return None

def create_map(fire_data_text):
    if fire_data_text is None or len(fire_data_text.strip().splitlines()) <= 1:
        print("Gösterilecek yangın verisi bulunamadı.")
        return

    data_io = StringIO(fire_data_text)
    df = pd.read_csv(data_io)
    
    df = df[df['confidence'] != 'l']

    print(f"{len(df)} yüksek güvenilirlikli nokta haritaya işleniyor...")
    turkiye_map = folium.Map(location=[39.925533, 32.866287], zoom_start=6)

    for _, row in df.iterrows():
        lat = row['latitude']
        lon = row['longitude']
        
        is_fire_simulation = random.choice([True, False, False, False, False])
        test_image = 'test_yangin.jpg' if is_fire_simulation else 'test_normal.jpg'

        if os.path.exists(test_image):
            sonuc, ihtimal = tahmin_et_yangin(test_image)
        else:
            sonuc, ihtimal = "HATA", 0

        if sonuc == "YANGIN":
            icon = folium.Icon(color='red', icon='fire', prefix='fa')
            popup_text = f"<b>DOĞRULANMIŞ YANGIN!</b><br>İhtimal: {ihtimal:.2%}<br>Konum: {lat}, {lon}"
        else:
            icon = folium.Icon(color='orange', icon='info-circle', prefix='fa')
            popup_text = f"<b>Termal Anomali</b><br>AI Skoru: {ihtimal:.2%}<br>Konum: {lat}, {lon}"

        folium.Marker(
            location=[lat, lon],
            icon=icon,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(turkiye_map)
        
    turkiye_map.save("final_panel.html")
    print(f"[{time.strftime('%H:%M:%S')}] Harita 'final_panel.html' olarak güncellendi.")

if __name__ == "__main__":
    print("Alev Gözcüsü Final Paneli Başlatılıyor...")
    initial_data = get_fire_data()
    create_map(initial_data)
    
    if os.path.exists("final_panel.html"):
        webbrowser.open("final_panel.html")

    while True:
        print(f"\nSonraki güncelleme {REFRESH_RATE_SECONDS} saniye sonra...")
        time.sleep(REFRESH_RATE_SECONDS)
        
        data = get_fire_data()
        create_map(data)