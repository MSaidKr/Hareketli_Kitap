import cv2
import mediapipe as mp
import numpy as np
import math
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# =====================================================================
# 1. SES SİSTEMİ BAŞLATMA 
# =====================================================================
pygame.mixer.init()

# =====================================================================
# 2. GÖRSELLERİN YÜKLENMESİ VE HAZIRLIK
# =====================================================================
SAHNE_W, SAHNE_H = 850, 480

try:
    ada_img = cv2.imread('model.png', cv2.IMREAD_UNCHANGED)
    gemi_img = cv2.imread('gemi.png', cv2.IMREAD_UNCHANGED)
    
    bg_gun_batimi = cv2.resize(cv2.imread('gun_batimi.png'), (SAHNE_W, SAHNE_H))
    bg_gece = cv2.resize(cv2.imread('gece.png'), (SAHNE_W, SAHNE_H))
    bg_sabah = cv2.resize(cv2.imread('sabah.png'), (SAHNE_W, SAHNE_H))
except Exception as e:
    print("Hata: Görseller yüklenemedi! Dosya isimlerini kontrol et.")
    exit()

ada_img = cv2.resize(ada_img, (400, 250))
gemi_img = cv2.resize(gemi_img, (150, 100))

arka_planlar = [bg_gun_batimi, bg_gece, bg_gun_batimi, bg_sabah]
aktif_bg_index = 0

# =====================================================================
# 3. ZAMANLAYICILAR VE GÜVENLİ BİNDİRME
# =====================================================================
son_bg_degisme_zamani = 0

def resme_resim_ekle_guvenli(arka_plan, eklenecek_resim, x, y):
    bg_h, bg_w = arka_plan.shape[:2]
    img_h, img_w = eklenecek_resim.shape[:2]
    x1, x2 = max(0, int(x)), min(bg_w, int(x + img_w))
    y1, y2 = max(0, int(y)), min(bg_h, int(y + img_h))
    if x1 >= x2 or y1 >= y2: return
    crop_x1, crop_y1 = x1 - int(x), y1 - int(y)
    crop_x2, crop_y2 = crop_x1 + (x2 - x1), crop_y1 + (y2 - y1)
    parca = eklenecek_resim[crop_y1:crop_y2, crop_x1:crop_x2]
    bgr = parca[:, :, :3]
    alpha = parca[:, :, 3] / 255.0
    for c in range(3):
        arka_plan[y1:y2, x1:x2, c] = (alpha * bgr[:, :, c] + (1.0 - alpha) * arka_plan[y1:y2, x1:x2, c])

# =====================================================================
# 4. KAMERA VE YAPAY ZEKA AYARLARI
# =====================================================================
KAMERA_ADRESI = 0 
cap = cv2.VideoCapture(KAMERA_ADRESI)
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=mp.tasks.vision.RunningMode.VIDEO, num_hands=1
)
landmarker = HandLandmarker.create_from_options(options)
frame_timestamp_ms = 0

gemi_x = SAHNE_W // 2
print("Guncellenmis Sihirli Ada Basladi!")

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    frame_timestamp_ms += 1
    detection_result = landmarker.detect_for_video(mp_image, frame_timestamp_ms)

    suan = time.time()
    parlaklik_carpani = 1.0  

    if detection_result.hand_landmarks:
        landmarks = detection_result.hand_landmarks[0]
        
        x4, y4 = landmarks[4].x * w, landmarks[4].y * h    # Başparmak
        x8, y8 = landmarks[8].x * w, landmarks[8].y * h    # İşaret Parmağı
        x12, y12 = landmarks[12].x * w, landmarks[12].y * h # Orta Parmak
        x16, y16 = landmarks[16].x * w, landmarks[16].y * h # Yüzük Parmağı
        x20, y20 = landmarks[20].x * w, landmarks[20].y * h # Serçe Parmağı

        y13 = landmarks[13].y * h # Yüzük parmak kökü
        y17 = landmarks[17].y * h # Serçe parmak kökü

        # -----------------------------------------------------------------
        # GÜNCELLEME 1: İŞARET PARMAĞI = Gemi (Hızlandırıldı & Sınırları Genişletildi)
        # -----------------------------------------------------------------
        # Kameranın orta kısmındaki ufak hareketler gemiyi uçtan uca götürecek
        gemi_x = int(np.interp(x8, [w * 0.15, w * 0.85], [-50, SAHNE_W - 100]))

        # -----------------------------------------------------------------
        # GÜNCELLEME 2: YÜZÜK PARMAĞI = Arka Plan (Tema Değişimi)
        # -----------------------------------------------------------------
        if y16 < y13: # Yüzük parmağı havadaysa
            if (suan - son_bg_degisme_zamani) > 1.5:
                aktif_bg_index = (aktif_bg_index + 1) % len(arka_planlar)
                son_bg_degisme_zamani = suan

        # -----------------------------------------------------------------
        # GÜNCELLEME 3: ORTA PARMAK = Parlaklık (Başparmak ile Mesafe)
        # -----------------------------------------------------------------
        orta_mesafe = math.hypot(x12 - x4, y12 - y4)
        parlaklik_carpani = np.interp(orta_mesafe, [20, 150], [0.2, 1.0])

        # -----------------------------------------------------------------
        # GÜNCELLEME 4: SERÇE PARMAĞI = Ses Kapat/Aç Modu
        # -----------------------------------------------------------------
        if y20 < y17: # Serçe parmağı havadaysa
            if not pygame.mixer.music.get_busy(): # Müzik çalmıyorsa başlat (Döngüye al)
                try:
                    pygame.mixer.music.load('marti.mp3')
                    pygame.mixer.music.play(-1) # -1 sayesinde parmak havadayken sürekli çalar
                except:
                    pass
        else: # Serçe parmağı kapalıysa
            pygame.mixer.music.stop() # Anında müziği keser

    # =====================================================================
    # SAHNE OLUŞTURMA VE KATMANLAMA
    # =====================================================================
    sahne = arka_planlar[aktif_bg_index].copy()
    sahne = cv2.convertScaleAbs(sahne, alpha=parlaklik_carpani, beta=0)

    gemi_y = SAHNE_H - 220
    resme_resim_ekle_guvenli(sahne, gemi_img, gemi_x, gemi_y)

    ada_x = (SAHNE_W - 400) // 2
    ada_y = SAHNE_H - 250
    resme_resim_ekle_guvenli(sahne, ada_img, ada_x, ada_y)

    cv2.putText(sahne, "Isaret: Gemi | Orta: Isik | Yuzuk: Tema | Serce: Ses", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    cv2.imshow("Kamera", frame)
    cv2.imshow("Etkilesimli Sihirli Ada", sahne)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
