import streamlit as st
import random
import os
import base64
from PIL import Image
from utils.ui_components import apply_custom_css

apply_custom_css()

kimsin = st.session_state.current_user

st.title("🃏 Anı Eşleştirme")
st.write("Kartların arkasındaki fotoğrafları (anıları) eşleştirin!")

st.markdown("""
<style>
@media (max-width: 768px) {
    div[data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
        flex-wrap: wrap !important;
    }
    div[data-testid="column"] {
        width: 23% !important;
        flex: 1 1 23% !important;
        min-width: 23% !important;
        padding: 0.1rem !important;
    }
}
div[data-testid="stImage"] img {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# Görüntü klasörü
IMG_DIR = "assets/images"

def get_images():
    if not os.path.exists(IMG_DIR):
        return []
    valid_extensions = {".jpg", ".jpeg", ".png"}
    images = [f for f in os.listdir(IMG_DIR) if os.path.splitext(f)[1].lower() in valid_extensions]
    return images

images = get_images()

if len(images) < 8:
    st.warning(f"Oyun için en az 8 fotoğraf gerekiyor. Lütfen '{IMG_DIR}' klasörüne fotoğraf ekleyin.")
    st.stop()

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def init_game():
    st.session_state.cards = random.sample(images, 8) * 2
    random.shuffle(st.session_state.cards)
    st.session_state.revealed = [False] * 16
    st.session_state.matched = [False] * 16
    st.session_state.first_pick = None
    st.session_state.second_pick = None

if 'cards' not in st.session_state:
    init_game()

from PIL import ImageOps

cols = st.columns(4)

def card_click(idx):
    if st.session_state.matched[idx] or st.session_state.revealed[idx]:
        return
    
    if st.session_state.first_pick is None:
        st.session_state.first_pick = idx
        st.session_state.revealed[idx] = True
    elif st.session_state.second_pick is None:
        st.session_state.second_pick = idx
        st.session_state.revealed[idx] = True

# Kartları çiz
for i in range(16):
    col = cols[i % 4]
    with col:
        if st.session_state.revealed[i] or st.session_state.matched[i]:
            img_path = os.path.join(IMG_DIR, st.session_state.cards[i])
            try:
                img = Image.open(img_path)
                # Görselleri kare olarak kırp ve küçült ki her yere sığsın
                img = ImageOps.fit(img, (150, 150), Image.Resampling.LANCZOS)
                st.image(img, use_container_width=True)
            except Exception:
                st.write("Resim hatası")
        else:
            if st.button("❓", key=f"card_{i}", use_container_width=True):
                card_click(i)
                st.rerun()

# Kontrol Mekanizması
if st.session_state.first_pick is not None and st.session_state.second_pick is not None:
    f_idx = st.session_state.first_pick
    s_idx = st.session_state.second_pick
    
    if st.session_state.cards[f_idx] == st.session_state.cards[s_idx]:
        st.success("Eşleşme başarılı!")
        st.session_state.matched[f_idx] = True
        st.session_state.matched[s_idx] = True
    else:
        st.error("Eşleşmedi!")
        st.session_state.revealed[f_idx] = False
        st.session_state.revealed[s_idx] = False
        
    st.session_state.first_pick = None
    st.session_state.second_pick = None
    st.rerun()

st.markdown("---")
if kimsin == "Mert":
    if st.button("🔄 Yeniden Başlat / Sıfırla", use_container_width=True):
        init_game()
        st.rerun()
