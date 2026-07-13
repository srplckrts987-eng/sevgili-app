import streamlit as st
import streamlit.components.v1 as components
from utils.ui_components import apply_custom_css

apply_custom_css()

st.title("🔲 Kutu Kapmaca (Gerçek Zamanlı)")
st.write("Sıfır gecikmeli, gerçek zamanlı Kutu Kapmaca! Bir kutuyu kapattığınızda **tekrar oynama hakkı** kazanırsınız.")

kimsin = st.session_state.current_user

# Firebase JS SDK tabanlı, sıfır gecikmeli oyun motoru
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        font-family: 'Inter', sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
        background: transparent;
        margin: 0;
        padding: 20px;
    }}
    .scoreboard {{
        display: flex;
        justify-content: space-between;
        width: 300px;
        margin-bottom: 20px;
        font-size: 1.2em;
        font-weight: bold;
    }}
    .turn-indicator {{
        margin-bottom: 20px;
        font-size: 1.5em;
        font-weight: bold;
        color: #333;
    }}
    .game-board {{
        position: relative;
        width: 320px;
        height: 320px;
        background-color: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        padding: 20px;
    }}
    .dot {{
        position: absolute;
        width: 12px;
        height: 12px;
        background-color: #333;
        border-radius: 50%;
        transform: translate(-50%, -50%);
        z-index: 3;
    }}
    .h-line {{
        position: absolute;
        height: 12px;
        width: 75px;
        background-color: transparent;
        cursor: pointer;
        transform: translateY(-50%);
        z-index: 2;
        transition: background-color 0.2s;
    }}
    .h-line:hover {{ background-color: rgba(255, 75, 75, 0.3) !important; }}
    .v-line {{
        position: absolute;
        width: 12px;
        height: 75px;
        background-color: transparent;
        cursor: pointer;
        transform: translateX(-50%);
        z-index: 2;
        transition: background-color 0.2s;
    }}
    .v-line:hover {{ background-color: rgba(255, 75, 75, 0.3) !important; }}
    
    .line-drawn {{ background-color: #333 !important; cursor: default; }}
    
    .box {{
        position: absolute;
        width: 75px;
        height: 75px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2em;
        font-weight: bold;
        z-index: 1;
        transition: all 0.3s;
    }}
    .box.Mert {{ background-color: rgba(0, 123, 255, 0.2); color: #007bff; }}
    .box.Rümeysa {{ background-color: rgba(255, 105, 180, 0.2); color: #ff69b4; }}
    
    .reset-btn {{
        margin-top: 20px;
        padding: 10px 20px;
        background-color: #ff4b4b;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 1.2em;
        cursor: pointer;
        font-weight: bold;
    }}
</style>
</head>
<body>

<div class="turn-indicator" id="turnIndicator">Yükleniyor...</div>
<div class="scoreboard">
    <div id="scoreMert">Mert: 0</div>
    <div id="scoreRumeysa">Rümeysa: 0</div>
</div>

<div class="game-board" id="board"></div>

<button class="reset-btn" id="resetBtn" style="display:none;" onclick="resetGame()">YENİDEN BAŞLAT / SIFIRLA</button>

<script type="module">
import {{ initializeApp }} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import {{ getDatabase, ref, onValue, set, get }} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-database.js";

const firebaseConfig = {{
  databaseURL: "https://sevgiliwepsite-default-rtdb.europe-west1.firebasedatabase.app"
}};
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);
const gameRef = ref(db, 'dots_and_boxes_v3');

const currentUser = "{kimsin}";
const GRID = 4; // 4x4 kutu = 5x5 nokta
const SPACING = 75; // Noktalar arası mesafe px

let gameState = null;

function initBoard() {{
    const board = document.getElementById("board");
    board.innerHTML = '';
    
    // Noktaları çiz
    for(let r=0; r<=GRID; r++) {{
        for(let c=0; c<=GRID; c++) {{
            let dot = document.createElement("div");
            dot.className = "dot";
            dot.style.top = (r * SPACING + 20) + "px";
            dot.style.left = (c * SPACING + 20) + "px";
            board.appendChild(dot);
        }}
    }}
    
    // Yatay Çizgiler
    for(let r=0; r<=GRID; r++) {{
        for(let c=0; c<GRID; c++) {{
            let line = document.createElement("div");
            line.className = "h-line";
            line.id = `h_${{r}}_${{c}}`;
            line.style.top = (r * SPACING + 20) + "px";
            line.style.left = (c * SPACING + 20 + 6) + "px";
            line.onclick = () => drawLine(line.id);
            board.appendChild(line);
        }}
    }}
    
    // Dikey Çizgiler
    for(let r=0; r<GRID; r++) {{
        for(let c=0; c<=GRID; c++) {{
            let line = document.createElement("div");
            line.className = "v-line";
            line.id = `v_${{r}}_${{c}}`;
            line.style.top = (r * SPACING + 20 + 6) + "px";
            line.style.left = (c * SPACING + 20) + "px";
            line.onclick = () => drawLine(line.id);
            board.appendChild(line);
        }}
    }}
    
    // Kutular
    for(let r=0; r<GRID; r++) {{
        for(let c=0; c<GRID; c++) {{
            let box = document.createElement("div");
            box.className = "box";
            box.id = `b_${{r}}_${{c}}`;
            box.style.top = (r * SPACING + 20) + "px";
            box.style.left = (c * SPACING + 20) + "px";
            board.appendChild(box);
        }}
    }}
}}

// Dinleme
onValue(gameRef, (snapshot) => {{
    let data = snapshot.val();
    if (!data) {{
        resetGame(); // İlk defa açılıyorsa sıfırla
        return;
    }}
    gameState = data;
    renderState();
}});

function renderState() {{
    document.getElementById("turnIndicator").innerText = "Sıra: " + gameState.turn;
    if (gameState.turn === currentUser) {{
        document.getElementById("turnIndicator").style.color = "#ff4b4b";
    }} else {{
        document.getElementById("turnIndicator").style.color = "#333";
    }}
    
    document.getElementById("scoreMert").innerText = "Mert: " + (gameState.scores?.Mert || 0);
    document.getElementById("scoreRumeysa").innerText = "Rümeysa: " + (gameState.scores?.Rümeysa || 0);
    
    // Çizgileri güncelle
    for(let r=0; r<=GRID; r++) {{
        for(let c=0; c<GRID; c++) {{
            let id = `h_${{r}}_${{c}}`;
            let el = document.getElementById(id);
            if (gameState.lines && gameState.lines[id]) el.classList.add("line-drawn");
            else el.classList.remove("line-drawn");
        }}
    }}
    for(let r=0; r<GRID; r++) {{
        for(let c=0; c<=GRID; c++) {{
            let id = `v_${{r}}_${{c}}`;
            let el = document.getElementById(id);
            if (gameState.lines && gameState.lines[id]) el.classList.add("line-drawn");
            else el.classList.remove("line-drawn");
        }}
    }}
    
    // Kutuları güncelle
    let boxCount = 0;
    for(let r=0; r<GRID; r++) {{
        for(let c=0; c<GRID; c++) {{
            let id = `b_${{r}}_${{c}}`;
            let el = document.getElementById(id);
            el.className = "box"; // reset
            el.innerText = "";
            if (gameState.boxes && gameState.boxes[id]) {{
                let owner = gameState.boxes[id];
                el.classList.add(owner);
                el.innerText = owner === "Mert" ? "M" : "R";
                boxCount++;
            }}
        }}
    }}
    
    // Oyun bitişi
    if (boxCount === GRID * GRID) {{
        if(currentUser === "Mert") document.getElementById("resetBtn").style.display = "block";
        let mertS = gameState.scores?.Mert || 0;
        let rumS = gameState.scores?.Rümeysa || 0;
        if (mertS > rumS) document.getElementById("turnIndicator").innerText = "🏆 Mert Kazandı!";
        else if (rumS > mertS) document.getElementById("turnIndicator").innerText = "🏆 Rümeysa Kazandı!";
        else document.getElementById("turnIndicator").innerText = "Oyun Berabere!";
    }} else {{
        if(currentUser === "Mert") document.getElementById("resetBtn").style.display = "block"; // Her zaman gösterilebilir
    }}
}}

window.drawLine = function(id) {{
    if (!gameState) return;
    if (gameState.turn !== currentUser) {{
        alert("Sıra sende değil!");
        return;
    }}
    if (gameState.lines && gameState.lines[id]) return; // Zaten çizilmiş
    
    // Çizgiyi ekle
    if (!gameState.lines) gameState.lines = {{}};
    gameState.lines[id] = true;
    
    // Kutu kontrolü
    let newBoxes = 0;
    if (!gameState.boxes) gameState.boxes = {{}};
    if (!gameState.scores) gameState.scores = {{"Mert": 0, "Rümeysa": 0}};
    
    for(let r=0; r<GRID; r++) {{
        for(let c=0; c<GRID; c++) {{
            let bId = `b_${{r}}_${{c}}`;
            if (!gameState.boxes[bId]) {{
                let top = gameState.lines[`h_${{r}}_${{c}}`];
                let bot = gameState.lines[`h_${{r+1}}_${{c}}`];
                let left = gameState.lines[`v_${{r}}_${{c}}`];
                let right = gameState.lines[`v_${{r}}_${{c+1}}`];
                
                if (top && bot && left && right) {{
                    gameState.boxes[bId] = currentUser;
                    gameState.scores[currentUser]++;
                    newBoxes++;
                }}
            }}
        }}
    }}
    
    // Kutu kapanmadıysa sırayı değiştir
    if (newBoxes === 0) {{
        gameState.turn = (gameState.turn === "Mert") ? "Rümeysa" : "Mert";
    }}
    
    set(gameRef, gameState);
}};

window.resetGame = function() {{
    const DEFAULT_STATE = {{
        turn: "Mert",
        lines: {{}},
        boxes: {{}},
        scores: {{"Mert": 0, "Rümeysa": 0}}
    }};
    set(gameRef, DEFAULT_STATE);
    document.getElementById("resetBtn").style.display = "none";
}};

initBoard();

</script>
</body>
</html>
"""

components.html(html_code, height=600)
