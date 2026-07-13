import streamlit as st
import random
from utils.db_helper import get_data, put_data
from streamlit_autorefresh import st_autorefresh

st.title("🚢 Amiral Battı")
st.write("Klasik Amiral Battı oyunu. Gemilerinizi (1 adet 3'lük, 2 adet 2'lik) rastgele yerleştirip ateş edin!")

kimsin = st.session_state.current_user

# Otomatik yenileme
st_autorefresh(interval=3000, limit=None, key="battleship_refresh")

DEFAULT_STATE = {
    "turn": "Mert",
    "boards": {
        "Mert": {"ships": {}, "shots": {}}, # ships: {"0_0": True}, shots: {"0_0": "hit"/"miss"}
        "Rümeysa": {"ships": {}, "shots": {}}
    },
    "ready": {"Mert": False, "Rümeysa": False},
    "winner": None
}

state = get_data("battleship")
if not state:
    put_data("battleship", DEFAULT_STATE)
    state = DEFAULT_STATE

GRID_SIZE = 6

def generate_random_ships():
    # 6x6 tahtaya rastgele 1 adet 3 birimlik, 2 adet 2 birimlik gemi yerleştir
    ships = {}
    
    def place_ship(length):
        placed = False
        while not placed:
            horiz = random.choice([True, False])
            r = random.randint(0, GRID_SIZE - 1)
            c = random.randint(0, GRID_SIZE - 1)
            
            coords = []
            for i in range(length):
                if horiz: coords.append((r, c+i))
                else: coords.append((r+i, c))
                
            valid = True
            for cr, cc in coords:
                if cr >= GRID_SIZE or cc >= GRID_SIZE or f"{cr}_{cc}" in ships:
                    valid = False
            if valid:
                for cr, cc in coords:
                    ships[f"{cr}_{cc}"] = True
                placed = True
                
    place_ship(3)
    place_ship(2)
    place_ship(2)
    return ships

col_info, col_btn = st.columns(2)

with col_info:
    if state.get("winner"):
        st.success(f"🏆 Kazanan: {state.get('winner')}")
    elif state.get("ready", {}).get("Mert") and state.get("ready", {}).get("Rümeysa"):
        st.info(f"Sıra Kimde: **{state['turn']}**")
    else:
        st.warning("Oyuncuların gemileri yerleştirmesi bekleniyor...")

with col_btn:
    if kimsin == "Mert":
        if st.button("🔄 Oyunu Sıfırla", use_container_width=True):
            put_data("battleship", DEFAULT_STATE)
            st.rerun()

st.markdown("---")

if not state.get("ready", {}).get(kimsin):
    st.write("Henüz gemilerini yerleştirmedin. Rastgele yerleştirmek için tıkla:")
    if st.button("Gemileri Yerleştir ve Hazır Ol!", type="primary"):
        state["boards"][kimsin]["ships"] = generate_random_ships()
        state["ready"][kimsin] = True
        put_data("battleship", state)
        st.rerun()

if state.get("ready", {}).get("Mert") and state.get("ready", {}).get("Rümeysa") and not state.get("winner"):
    enemy = "Rümeysa" if kimsin == "Mert" else "Mert"
    
    # Firebase empty dict fix
    if "shots" not in state["boards"][enemy]: state["boards"][enemy]["shots"] = {}
    if "ships" not in state["boards"][enemy]: state["boards"][enemy]["ships"] = {}
    if "shots" not in state["boards"][kimsin]: state["boards"][kimsin]["shots"] = {}
    if "ships" not in state["boards"][kimsin]: state["boards"][kimsin]["ships"] = {}

    st.write(f"🎯 **{enemy}'nın Sahası (Ateş Et)**")
    
    # Düşman tahtası (Tıklanabilir butonlar)
    cols = st.columns(GRID_SIZE)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            idx = f"{r}_{c}"
            shot_status = state["boards"][enemy]["shots"].get(idx)
            
            label = "🌊"
            disabled = False
            
            if shot_status == "hit":
                label = "💥"
                disabled = True
            elif shot_status == "miss":
                label = "❌"
                disabled = True
                
            with cols[c]:
                if st.button(label, key=f"shot_{r}_{c}", disabled=disabled, use_container_width=True):
                    if state["turn"] == kimsin:
                        if idx in state["boards"][enemy]["ships"]:
                            state["boards"][enemy]["shots"][idx] = "hit"
                            # Kazanma kontrolü (Toplam 7 parça var)
                            hits = sum(1 for v in state["boards"][enemy]["shots"].values() if v == "hit")
                            if hits == 7:
                                state["winner"] = kimsin
                            # Vuran bir daha oynar
                        else:
                            state["boards"][enemy]["shots"][idx] = "miss"
                            state["turn"] = enemy # Sıra geçer
                        put_data("battleship", state)
                        st.rerun()
                    else:
                        st.toast("Sıra sende değil!")

    st.markdown("---")
    st.write("🛡️ **Kendi Sahan (Gemilerin)**")
    # Kendi tahtan (Sadece izleme)
    my_cols = st.columns(GRID_SIZE)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            idx = f"{r}_{c}"
            is_ship = idx in state["boards"][kimsin]["ships"]
            enemy_shot = state["boards"][kimsin]["shots"].get(idx)
            
            display = "🟦"
            if is_ship: display = "🚢"
            if enemy_shot == "hit": display = "💥"
            elif enemy_shot == "miss": display = "❌"
            
            with my_cols[c]:
                st.markdown(f"<div style='text-align:center; font-size:2em;'>{display}</div>", unsafe_allow_html=True)

