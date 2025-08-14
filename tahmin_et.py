import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

MODEL_PATH = 'alev_gozcusu_model.h5'
IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256
KARAR_ESIGI = 0.85 

print("Yapay zekâ modeli yükleniyor...")
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model başarıyla yüklendi.")
except Exception as e:
    print(f"Model yüklenirken hata oluştu: {e}")
    exit()

def tahmin_et(image_path):
    try:
        img = image.load_img(image_path, target_size=(IMAGE_HEIGHT, IMAGE_WIDTH))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        prediction_non_fire = model.predict(img_array)[0][0]
        ihtimal_fire = 1 - prediction_non_fire

        print(f"Modelin Ham Yangın Skoru: {ihtimal_fire:.2%}")

        if ihtimal_fire > KARAR_ESIGI:
            print(f"SONUÇ: YANGIN TESPİT EDİLDİ! (Karar Eşiği > %{KARAR_ESIGI:.0%})")
            return "YANGIN"
        else:
            print(f"SONUÇ: YANGIN TESPİT EDİLMEDİ. (Karar Eşiği <= %{KARAR_ESIGI:.0%})")
            return "NORMAL"
            
    except FileNotFoundError:
        print(f"Hata: '{image_path}' adında bir dosya bulunamadı.")
        return None
    except Exception as e:
        print(f"Tahmin sırasında bir hata oluştu: {e}")
        return None

if __name__ == "__main__":
    print("\n--- TEST 1: Yangınlı Görüntü ---")
    tahmin_et('test_yangin.jpg')

    print("\n--- TEST 2: Normal Görüntü ---")
    tahmin_et('test_normal.jpg')