import streamlit as st
import streamlit.components.v1 as components
import json
from utils.api_helper import get_prayer_times, get_daily_content
from utils.ui_components import apply_custom_css
import datetime

apply_custom_css()

st.title("🕌 İbadet ve Maneviyat")

# Şehir Seçimi (Kıble ve Vakit için)
sehir = st.selectbox("Konum Seçiniz", ["Tokat", "Kilis"])

# Kıble açıları (Yaklaşık)
kible_acilari = {
    "Tokat": 158,
    "Kilis": 167
}

vakitler = get_prayer_times(city=sehir)

col1, col2 = st.columns([1, 1])

with col1:
    st.header("⏳ Vakit Sayacı")
    if vakitler:
        # Vakitleri saniyeli sayaca göndermek için JS'ye inject edelim
        vakitler_json = json.dumps(vakitler)
        
        sayac_html = f"""
        <div style="text-align:center; padding:20px; background:#f8f9fa; border-radius:10px;">
            <h3 id="nextVakitName" style="color:#555; margin:0;">Hesaplanıyor...</h3>
            <h1 id="vakitTimer" style="color:#ff4b4b; font-size:3em; margin:10px 0;">00:00:00</h1>
            <p id="kerahatUyari" style="color:red; font-weight:bold; display:none;">⚠️ Şu an Kerahat Vaktindesiniz!</p>
        </div>
        <script>
            const vakitler = {vakitler_json};
            const orderedNames = ["İmsak", "Güneş", "Öğle", "İkindi", "Akşam", "Yatsı"];
            
            function updateTimer() {{
                const now = new Date();
                let nextName = "";
                let nextTime = null;
                
                for(let name of orderedNames) {{
                    let parts = vakitler[name].split(":");
                    let t = new Date();
                    t.setHours(parseInt(parts[0]), parseInt(parts[1]), 0, 0);
                    
                    if(t > now) {{
                        nextName = name;
                        nextTime = t;
                        break;
                    }}
                }}
                
                if(!nextTime) {{
                    nextName = "İmsak (Yarın)";
                    let parts = vakitler["İmsak"].split(":");
                    nextTime = new Date();
                    nextTime.setDate(nextTime.getDate() + 1);
                    nextTime.setHours(parseInt(parts[0]), parseInt(parts[1]), 0, 0);
                }}
                
                let diff = nextTime - now;
                let h = Math.floor(diff / 3600000);
                let m = Math.floor((diff % 3600000) / 60000);
                let s = Math.floor((diff % 60000) / 1000);
                
                document.getElementById("nextVakitName").innerText = "Sıradaki Vakit: " + nextName;
                document.getElementById("vakitTimer").innerText = 
                    h.toString().padStart(2, '0') + ":" + 
                    m.toString().padStart(2, '0') + ":" + 
                    s.toString().padStart(2, '0');
                
                let kerahat = false;
                if (nextName === "Güneş" && diff < 45 * 60000) kerahat = true; 
                if (nextName === "Akşam" && diff < 45 * 60000) kerahat = true; 
                
                document.getElementById("kerahatUyari").style.display = kerahat ? "block" : "none";
            }}
            setInterval(updateTimer, 1000);
            updateTimer();
        </script>
        """
        components.html(sayac_html, height=200)

with col2:
    st.header("🧭 Kıble Yönü")
    aci = kible_acilari[sehir]
    st.info(f"**{sehir}** için kıble açısı Kuzey'den itibaren saat yönünde **{aci}°**'dir.")
    st.markdown(f"""
    <div style="display:flex; justify-content:center; align-items:center; height:150px;">
        <div style="width:100px; height:100px; border-radius:50%; border:3px solid #ccc; position:relative; display:flex; justify-content:center; align-items:center;">
            <div style="position:absolute; top:-25px; font-weight:bold; color:#555;">KUZEY</div>
            <div style="font-size:3em; transform: rotate({aci}deg);">⬆️</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("---")

col_z, col_i = st.columns([1, 1])

with col_z:
    st.header("📿 Zikirmatik")
    
    zikir_html = """
    <div style="text-align:center; padding:20px; background:#fff; border-radius:15px; box-shadow:0 5px 15px rgba(0,0,0,0.1);">
        <select id="zikirType" style="padding:10px; font-size:1.1em; margin-bottom:20px; border-radius:5px; width:100%;">
            <option value="Sübhanallah">Sübhanallah (33)</option>
            <option value="Elhamdülillah">Elhamdülillah (33)</option>
            <option value="Allahu Ekber">Allahu Ekber (33)</option>
            <option value="La ilahe illallah">La ilahe illallah (Serbest)</option>
        </select>
        <div id="countDisplay" style="font-size:5em; font-weight:bold; color:#ff4b4b; margin:20px 0;">0</div>
        <button onclick="increment()" style="width:150px; height:150px; border-radius:50%; background:#28a745; color:white; font-size:2em; border:none; box-shadow:0 10px 20px rgba(40,167,69,0.4); cursor:pointer;">Bas</button>
        <br><br>
        <button onclick="resetZikir()" style="padding:10px 20px; background:#6c757d; color:white; border:none; border-radius:5px; cursor:pointer;">Sıfırla</button>
    </div>
    <script>
        let count = 0;
        function increment() {
            count++;
            document.getElementById("countDisplay").innerText = count;
            
            let type = document.getElementById("zikirType").value;
            let target = 33;
            if (type === "La ilahe illallah") target = 100;
            
            if (count % target === 0) {
                if (navigator.vibrate) navigator.vibrate([200, 100, 200]); 
                document.getElementById("countDisplay").style.color = "#28a745";
                setTimeout(() => { document.getElementById("countDisplay").style.color = "#ff4b4b"; }, 500);
            } else {
                if (navigator.vibrate) navigator.vibrate(50);
            }
        }
        function resetZikir() {
            count = 0;
            document.getElementById("countDisplay").innerText = count;
        }
    </script>
    """
    components.html(zikir_html, height=450)

with col_i:
    st.header("📖 Günün İçerikleri")
    icerik = get_daily_content()
    st.success(f"**Günün Ayeti:**\n\n{icerik['ayet']}")
    st.info(f"**Günün Hadisi:**\n\n{icerik['hadis']}")
    
    with st.expander("✨ Esmaü'l-Hüsna (Allah'ın 99 İsmi)"):
        st.markdown("""
        1. **Allah:** Kendinden başka ilah bulunmayan.
        2. **Er-Rahman:** Dünyada bütün mahlukata merhamet eden.
        3. **Er-Rahim:** Ahirette müminlere merhamet eden.
        4. **El-Melik:** Mülkün, kâinatın sahibi.
        5. **El-Kuddüs:** Her türlü eksiklikten uzak.
        6. **Es-Selam:** Kullarını selamete çıkaran.
        *(Bu bölüm günlük okumalarınız için örnek olarak listelenmiştir. Tamamı eklenebilir)*
        """)
