import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
from utils.ui_components import render_metric_card, render_timeline_item, apply_custom_css
from utils.db_helper import get_data, put_data
from streamlit_autorefresh import st_autorefresh

apply_custom_css()

kimsin = st.session_state.current_user

# Otomatik yenileme (Dua bildirimleri için 10 saniyede bir)
st_autorefresh(interval=10000, limit=None, key="dashboard_refresh")

st.title(f"Hoş Geldin, {kimsin} 🤍")
st.markdown("---")

st.header("⏳ Kavuşmaya Kalan Zaman")

# Koyu Mod uyumlu saniyeli JavaScript Geri Sayım Sayacı
countdown_html = """
<div id="countdown" style="font-family: 'Inter', sans-serif; text-align: center; background-color: var(--secondary-background-color); padding: 20px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px;">
    <h2 style="margin: 0; color: #ff4b4b; font-size: 2.5em; font-weight: bold;" id="timer">Yükleniyor...</h2>
    <p style="margin: 5px 0 0 0; color: var(--text-color); font-size: 1.1em;">14 Eylül 2026</p>
</div>
<script>
    var countDownDate = new Date("Sep 14, 2026 00:00:00").getTime();
    var x = setInterval(function() {
        var now = new Date().getTime();
        var distance = countDownDate - now;
        
        if (distance < 0) {
            clearInterval(x);
            document.getElementById("timer").innerHTML = "KAVUŞTUNUZ! 🎉";
            return;
        }

        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        document.getElementById("timer").innerHTML = days + " Gün " + hours + " Saat " + minutes + " Dakika " + seconds + " Saniye ";
    }, 1000);
</script>
"""
components.html(countdown_html, height=150)


# Doğum Günleri (Bu yıl için hesaplama)
col1, col2 = st.columns(2)
current_year = datetime.now().year
mert_dogum = datetime(current_year, 12, 12)
if mert_dogum < datetime.now(): mert_dogum = datetime(current_year + 1, 12, 12)
mert_gun_kaldi = (mert_dogum - datetime.now()).days

rumeysa_dogum = datetime(current_year, 6, 25)
if rumeysa_dogum < datetime.now(): rumeysa_dogum = datetime(current_year + 1, 6, 25)
rumeysa_gun_kaldi = (rumeysa_dogum - datetime.now()).days

with col1:
    render_metric_card("Mert'in Doğum Gününe", f"{mert_gun_kaldi} Gün", "12 Aralık")
with col2:
    render_metric_card("Rümeysa'nın Doğum Gününe", f"{rumeysa_gun_kaldi} Gün", "25 Haziran")

st.markdown("---")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.header("🕰️ Zaman Tüneli")
    render_timeline_item("28 Mart 2026", "Vera'da ilk buluşma ☕")
    render_timeline_item("14 Nisan 2026", "Sevgili olma tarihi ❤️")
    render_timeline_item("14 Mayıs 2026", "Sevgililiğin 1. Ayı 🎉")

with col_right:
    st.header("🤲 Bana Dua Et")
    karsi_taraf = "Rümeysa" if kimsin == "Mert" else "Mert"
    st.write(f"{karsi_taraf} sana dua etsin istiyorsan aşağıdaki butona tıkla.")
    
    if st.button(f"{karsi_taraf}'ya Dua İsteği Gönder 🤍", use_container_width=True):
        # Firebase'e dua isteği yaz
        dua_istegi = {
            "from": kimsin,
            "to": karsi_taraf,
            "timestamp": datetime.now().isoformat(),
            "seen": False
        }
        put_data(f"dua_istegi_{karsi_taraf}", dua_istegi)
        st.success("Dua isteğin gönderildi! 🕊️")

    # Dua isteği kontrolü
    gelen_istek = get_data(f"dua_istegi_{kimsin}")
    if gelen_istek and not gelen_istek.get("seen"):
        gonderen = gelen_istek.get("from")
        st.info(f"✨ **{gonderen} şu an senden dua bekliyor 🤍**")
        if st.button("Dua Ettim & Bildirimi Kapat", use_container_width=True):
            gelen_istek["seen"] = True
            put_data(f"dua_istegi_{kimsin}", gelen_istek)
            st.rerun()
