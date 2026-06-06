# 🎭 Hareketli Kitap!

Bu proje, bilgisayarlı görü ve yapay zeka teknikleri kullanılarak geliştirilmiş interaktif bir sanal kontrol sistemidir. Akıllı telefon kamerası üzerinden alınan gerçek zamanlı el hareketleri (gestures) ile ekrandaki dijital nesnelerin konumları değiştirilmekte, arayüzdeki ışık seviyesi kontrol edilmekte ve spesifik el hareketleriyle arka plan ses efektleri tetiklenmektedir.

## 🚀 Özellikler

* **Gerçek Zamanlı El Takibi:** MediaPipe Hand Landmark modeli ile 21 farklı eklem noktasının gecikmesiz tespiti.
* **Akıllı Kamera Entegrasyonu:** Camo Studio aracılığıyla telefon kamerasının yüksek çözünürlüklü IP/Sanal kamera olarak kullanılması.
* **Dinamik Görüntü Etkileşimi:** El hareketlerinin x ve y koordinatlarına göre ekrandaki nesnelerin sürüklenmesi.
* **Işık/Parlaklık Kontrolü:** Parmaklar arasındaki mesafeye duyarlı, anlık değişen ışık seviyesi yönetimi.
* **İşitsel Geri Bildirim:** Belirli el hareketlerinin birer tetikleyici (trigger) olarak kullanılıp arka plan ses dosyalarını oynatması.

## ⚙️ Kurulum ve Gereksinimler

Projenin yerel makinenizde çalışabilmesi için aşağıdaki adımları izleyin:

1. Anaconda Prompt Terminali üzerinden gerekli kütüphanelerin yüklenmesi: cv2, mediapipe, numpy.
```bash 
uv pip install opencv-python mediapipe numpy
```
2. Hazır "Proje" dosyasını indirin.
3. Eğer Camo Studio harici bir uygulama kullanacaksanız, cv2.VideoCapture() parametresini güncelleyin.
4. Kullanım için terminale yazın:
```bash
python kukla_projesi.py 
```

## Proje Resimleri

<img width="1536" height="1024" alt="model" src="https://github.com/user-attachments/assets/54c7a56e-1d47-4477-a7d2-b9958ed54e36" />
<img width="1536" height="1024" alt="gemi" src="https://github.com/user-attachments/assets/d26bbaa8-7334-4080-ade9-0a3e7574bf02" />
<img width="1536" height="1024" alt="gun_batimi" src="https://github.com/user-attachments/assets/0f37fe4b-e232-4524-ba6a-ae6f7bb7bc9b" />


## MSaidKr

