import streamlit as st

def check_login(username, password):
    if username == "Mert" and password == "456":
        return True
    elif username == "Rümeysa" and password == "123":
        return True
    return False

st.markdown("<h1 style='text-align: center; margin-top: 50px;'>Hoş Geldiniz 🤍</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Uygulamaya erişmek için lütfen giriş yapın.</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    kullanici_adi = st.selectbox("Kimsin?", ["Mert", "Rümeysa"])
    sifre = st.text_input("Şifre:", type="password")
    
    if st.button("Giriş Yap", use_container_width=True, type="primary"):
        if check_login(kullanici_adi, sifre):
            st.session_state.logged_in = True
            st.session_state.current_user = kullanici_adi
            st.query_params["user"] = kullanici_adi
            st.rerun()
        else:
            st.error("Hatalı şifre! Lütfen tekrar dene.")
