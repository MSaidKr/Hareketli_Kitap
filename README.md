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

1. Anaconda Prompt Terminali üzerinden gerekli kütüphanelerin yüklenmesi: cv2, mediapipe, numpy, math, time, os.
'''bash
uv pip install opencv-python mediapipe numpy
3. Hazır "Proje" dosyasını indirin.
4. Eğer Camo Studio harici bir uygulama kullanacaksanız, cv2.VideoCapture() parametresini güncelleyin.
5. Kullanım için terminale: python kukla_projesi.py yazın.

## MSaidKr

