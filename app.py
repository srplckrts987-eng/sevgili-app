import streamlit as st

if 'logged_in' not in st.session_state:
    if "user" in st.query_params and st.query_params["user"] in ["Mert", "Rümeysa"]:
        st.session_state.logged_in = True
        st.session_state.current_user = st.query_params["user"]
    else:
        st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Sayfa yapılandırması ana dosyada yapılır
st.set_page_config(
    page_title="Mert & Rümeysa",
    page_icon="🤍",
    layout="wide",
    initial_sidebar_state="auto"
)

# Koyu Mod için CSS düzeltmeleri (Eğer açık modda kalmış elementler varsa)
st.markdown("""
<style>
    /* Ortak CSS */
    .stButton>button {
        border-radius: 8px;
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    # Giriş yapmayanlara sadece Login sayfasını göster
    pg = st.navigation([st.Page("views/login.py", title="Giriş", icon="🔒")])
    pg.run()
else:
    # Giriş yapanlara menüyü göster
    pages = {
        "🏠 Ana Menü": [
            st.Page("views/dashboard.py", title="Ana Ekran", icon="🏠"),
            st.Page("views/maneviyat.py", title="İbadet ve Maneviyat", icon="🕌")
        ],
        "🎮 Oyunlar Merkezi": [
            st.Page("views/games/kutu_kapmaca.py", title="Kutu Kapmaca", icon="🔲"),
            st.Page("views/games/xox.py", title="XOX (Tic Tac Toe)", icon="❌"),
            st.Page("views/games/hokey.py", title="Masa Hokeyi", icon="🏒"),
            st.Page("views/games/amiral_batti.py", title="Amiral Battı", icon="🚢"),
            st.Page("views/games/kelime_avi.py", title="Kelime Avı", icon="🔤"),
            st.Page("views/games/pacman.py", title="Pacman", icon="👻"),
            st.Page("views/games/yilan.py", title="Yılan Oyunu", icon="🐍"),
            st.Page("views/games/hafiza.py", title="Anı Eşleştirme", icon="🃏"),
            st.Page("views/games/math.py", title="Günün İşlemi", icon="🧮")
        ]
    }
    pg = st.navigation(pages)
    pg.run()
