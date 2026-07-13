import streamlit as st
import random
from utils.db_helper import get_data, put_data
from streamlit_autorefresh import st_autorefresh

st.title("🔤 Kelime Avı (Ortak Adam Asmaca)")
st.write("Biriniz kelime belirler, diğeriniz tahmin eder!")

kimsin = st.session_state.current_user

# Otomatik yenileme
st_autorefresh(interval=3000, limit=None, key="word_refresh")

DEFAULT_STATE = {
    "word": "",
    "creator": "",
    "guesses": [],
    "lives": 6,
    "winner": None # "Guesser" veya "Creator"
}

state = get_data("word_game")
if not state:
    put_data("word_game", DEFAULT_STATE)
    state = DEFAULT_STATE

col1, col2 = st.columns([2, 1])

with col2:
    if kimsin == "Mert":
        if st.button("🔄 Oyunu Sıfırla", use_container_width=True):
            put_data("word_game", DEFAULT_STATE)
            st.rerun()

with col1:
    if state["word"] == "":
        st.warning("Şu an aktif bir oyun yok.")
        st.write("Yeni bir kelime belirleyerek oyunu başlatın (Diğer kişi tahmin edecek).")
        yeni_kelime = st.text_input("Gizli Kelime (Sadece harfler):", type="password")
        if st.button("Oyunu Başlat"):
            if yeni_kelime.isalpha():
                state = {
                    "word": yeni_kelime.upper(),
                    "creator": kimsin,
                    "guesses": [],
                    "lives": 6,
                    "winner": None
                }
                put_data("word_game", state)
                st.rerun()
            else:
                st.error("Lütfen sadece harflerden oluşan bir kelime girin.")
    else:
        # Oyun aktif
        guesser = "Rümeysa" if state["creator"] == "Mert" else "Mert"
        
        st.info(f"Oluşturan: **{state['creator']}** | Tahmin Eden: **{guesser}**")
        
        display_word = ""
        won = True
        for char in state["word"]:
            if char in state["guesses"]:
                display_word += f" {char} "
            else:
                display_word += " _ "
                won = False
                
        st.markdown(f"<h1 style='text-align:center; letter-spacing: 5px;'>{display_word}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center; color:red;'>Kalan Can: {'❤️' * state['lives']}</h3>", unsafe_allow_html=True)
        
        if won and state["winner"] is None:
            state["winner"] = guesser
            put_data("word_game", state)
            st.rerun()
            
        if state["winner"]:
            st.success(f"Oyun Bitti! Kazanan: {state['winner']}")
            st.info(f"Gizli Kelime: **{state['word']}**")
        else:
            if kimsin == guesser:
                tahmin = st.text_input("Harf Tahmini:", max_chars=1).upper()
                if st.button("Tahmin Et"):
                    if tahmin and tahmin.isalpha():
                        if tahmin not in state["guesses"]:
                            state["guesses"].append(tahmin)
                            if tahmin not in state["word"]:
                                state["lives"] -= 1
                                if state["lives"] <= 0:
                                    state["winner"] = state["creator"]
                            put_data("word_game", state)
                            st.rerun()
                        else:
                            st.warning("Bu harfi zaten denedin!")
            else:
                st.write("Tahmin sırası karşı tarafta. Bekleyiniz...")
