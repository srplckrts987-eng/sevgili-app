import streamlit as st
import random
from datetime import datetime
from utils.db_helper import get_data, put_data
from utils.ui_components import apply_custom_css

apply_custom_css()

st.title("🧮 Günün İşlemi")
st.write("Verilen 6 sayıyı ve 4 işlemi (+, -, *, /) kullanarak Hedef Sayı'ya ulaşmaya çalışın!")

# Bugüne ait seed oluştur
today_str = datetime.now().strftime("%Y-%m-%d")
random.seed(today_str)

kucuk_sayilar = [random.randint(1, 10) for _ in range(4)]
buyuk_sayilar = [random.choice([25, 50, 75, 100]) for _ in range(2)]
sayilar = kucuk_sayilar + buyuk_sayilar
random.shuffle(sayilar)

hedef_sayi = random.randint(101, 999)

st.markdown("---")
st.markdown(f"<h2 style='text-align:center;'>🎯 Hedef: <span style='color:#ff4b4b;'>{hedef_sayi}</span></h2>", unsafe_allow_html=True)

st.write("**Kullanabileceğiniz Sayılar:**")
cols = st.columns(6)
for i, s in enumerate(sayilar):
    with cols[i]:
        st.markdown(f"<div style='background:#f0f2f6; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:1.5em;'>{s}</div>", unsafe_allow_html=True)

st.markdown("---")

kimsin = st.session_state.current_user

formül = st.text_input("Formülünüzü girin (Örn: (50 * 8) + 25):")

if st.button("Sonucu Kontrol Et", use_container_width=True):
    try:
        if any(c.isalpha() for c in formül):
            st.error("Lütfen sadece sayı ve matematiksel işaretler kullanın!")
        else:
            # Sadece izin verilen karakterler
            sonuc = eval(formül)
            if sonuc == hedef_sayi:
                st.balloons()
                st.success(f"Tebrikler {kimsin}! Hedefe tam ulaştın! Sonuç: {sonuc}")
                # Skor kaydetme
                gunun_skorlari = get_data(f"math_scores_{today_str}") or {}
                gunun_skorlari[kimsin] = "Tam İsabet!"
                put_data(f"math_scores_{today_str}", gunun_skorlari)
            else:
                fark = abs(hedef_sayi - sonuc)
                st.info(f"Sonucun: {sonuc}. Hedefe {fark} kaldı!")
    except Exception as e:
        st.error("Hatalı bir formül girdiniz. Lütfen parantezleri ve işlemleri kontrol edin.")

gunun_skorlari = get_data(f"math_scores_{today_str}")
if gunun_skorlari:
    st.write("---")
    st.write("🏆 **Günün Kazananları:**")
    for isim, durum in gunun_skorlari.items():
        st.write(f"- {isim}: {durum}")
