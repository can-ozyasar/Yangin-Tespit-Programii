import requests

API_KEY = "d9fdb1897a881ae706357b458b97a6c3"

SOURCE = "VIIRS_SNPP_NRT"

COUNTRY = "TUR"  # Türkiye için ISO 3166-1 alpha-2 kodu

DAYS = "1"

url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{API_KEY}/{SOURCE}/{COUNTRY}/{DAYS}"

print("NASA FIRMS sunucusuna bağlanıyor ... ")
print(f"İstek gönderilen URL: {url}")

try:
    response = requests.get(url)
    if response.status_code == 200:
        print("\nBağlantı Başarılı! Veri alınıyor ... ")
        fire_data_text = response. text
        print("\n --- ALINAN HAM YANGIN VERİSİ --- ")
        print(fire_data_text)

        with open("ham_yangin_verisi.csv", "w", encoding="utf-8") as file: file.write(fire_data_text)

        print("\nVeri ham_yangin_verisi.csv dosyasına başarıyla kaydedildi!")

    else:
        print(f"\n Hata! Durum kodu: {response.status_code}")
        print("Sunucunun cevabi :", response.text)

except Exception as e:
    print(f"Program çalışırken bir hata oluştu: {e}")