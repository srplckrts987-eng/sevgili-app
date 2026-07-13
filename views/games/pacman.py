import streamlit as st
import streamlit.components.v1 as components

st.title("👻 Basit Pacman")
st.write("Sarı noktaları topla, hayaletten (Kırmızı) kaç! (Skorunuz kaydedilir)")

kimsin = st.session_state.current_user

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ background: #222; color: white; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; }}
    #grid {{ display: grid; grid-template-columns: repeat(15, 20px); grid-template-rows: repeat(15, 20px); gap: 2px; background: #111; padding: 10px; border-radius: 5px; }}
    .cell {{ width: 20px; height: 20px; background: #111; display:flex; align-items:center; justify-content:center; }}
    .wall {{ background: #0000ff; border-radius: 2px; }}
    .dot {{ width: 6px; height: 6px; background: yellow; border-radius: 50%; }}
    .pacman {{ width: 16px; height: 16px; background: yellow; border-radius: 50%; }}
    .ghost {{ width: 16px; height: 16px; background: red; border-radius: 50%; }}
    .controls {{ display: grid; grid-template-columns: 50px 50px 50px; gap: 5px; margin-top: 20px; }}
    .btn {{ width: 50px; height: 50px; font-size: 1.5em; background: #444; color: white; border: none; border-radius: 10px; cursor: pointer; }}
    .leaderboard {{ width: 300px; background: #333; padding: 10px; border-radius: 10px; margin-bottom: 20px; font-size: 1.2em; }}
    .leaderboard .title {{ font-weight: bold; color: #ff4b4b; text-align: center; margin-bottom: 10px; }}
    .score-row {{ display: flex; justify-content: space-between; padding: 5px 10px; background: #222; margin-bottom: 5px; border-radius: 5px; }}
</style>
</head>
<body>

<div class="leaderboard">
    <div class="title">🏆 EN İYİ SKORLAR</div>
    <div id="lb-content">Yükleniyor...</div>
</div>
<h2 style="margin-bottom: 5px;">Skor: <span id="score">0</span></h2>
<p id="gameOver" style="color:red; display:none; font-weight:bold;">OYUN BİTTİ!</p>
<div id="grid"></div>

<!-- Mobil destek için butonlar -->
<div class="controls">
    <div></div><button class="btn" onclick="setDir(0, -1)">⬆️</button><div></div>
    <button class="btn" onclick="setDir(-1, 0)">⬅️</button><button class="btn" onclick="setDir(0, 1)">⬇️</button><button class="btn" onclick="setDir(1, 0)">➡️</button>
</div>
<!-- RESET_BTN -->

<script type="module">
import {{ initializeApp }} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import {{ getDatabase, ref, onValue, set, get }} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-database.js";

const firebaseConfig = {{
    databaseURL: "https://sevgiliwepsite-default-rtdb.europe-west1.firebasedatabase.app"
}};
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);
const scoreRef = ref(db, 'pacman_highscores');
const currentUser = "{kimsin}";

let myHighScore = 0;

onValue(scoreRef, (snapshot) => {{
    let data = snapshot.val() || {{}};
    let scores = [];
    if(data["Mert"] !== undefined) scores.push({{name: "Mert", s: data["Mert"]}});
    if(data["Rümeysa"] !== undefined) scores.push({{name: "Rümeysa", s: data["Rümeysa"]}});
    
    scores.sort((a, b) => b.s - a.s);
    
    let lbHtml = "";
    let rank = 1;
    for(let item of scores) {{
        let medal = rank === 1 ? "🥇" : "🥈";
        lbHtml += `<div class="score-row"><span>${{medal}} ${{item.name}}</span><span>${{item.s}}</span></div>`;
        if(item.name === currentUser) myHighScore = item.s;
        rank++;
    }}
    if(scores.length === 0) lbHtml = "<div style='text-align:center;'>Henüz skor yok</div>";
    document.getElementById("lb-content").innerHTML = lbHtml;
}});

const w = 15; const h = 15;
const map_template = [
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
    1,2,2,2,2,2,2,1,2,2,2,2,2,2,1,
    1,2,1,1,1,1,2,1,2,1,1,1,1,2,1,
    1,2,1,2,2,2,2,2,2,2,2,2,1,2,1,
    1,2,1,2,1,1,2,1,2,1,1,2,1,2,1,
    1,2,2,2,1,2,2,1,2,2,1,2,2,2,1,
    1,1,1,2,1,2,1,1,1,2,1,2,1,1,1,
    1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,
    1,1,1,2,1,2,1,1,1,2,1,2,1,1,1,
    1,2,2,2,1,2,2,1,2,2,1,2,2,2,1,
    1,2,1,2,1,1,2,1,2,1,1,2,1,2,1,
    1,2,1,2,2,2,2,2,2,2,2,2,1,2,1,
    1,2,1,1,1,1,2,1,2,1,1,1,1,2,1,
    1,2,2,2,2,2,2,1,2,2,2,2,2,2,1,
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
];
let map = [...map_template];
let pac = {{x: 7, y: 7}};
let dx = 0; let dy = 0;
let ghost = {{x: 1, y: 1}};
let score = 0;
let gameInterval;
let ghostInterval;

window.resetGame = function() {{
    map = [...map_template];
    pac = {{x: 7, y: 7}};
    ghost = {{x: 1, y: 1}};
    dx = 0; dy = 0; score = 0;
    document.getElementById("gameOver").style.display = "none";
    clearInterval(gameInterval); clearInterval(ghostInterval);
    gameInterval = setInterval(update, 200);
    ghostInterval = setInterval(moveGhost, 400);
    draw();
}}

function draw() {{
    let g = document.getElementById("grid");
    g.innerHTML = "";
    for(let y=0; y<h; y++) {{
        for(let x=0; x<w; x++) {{
            let cell = document.createElement("div");
            cell.className = "cell";
            let val = map[y*w + x];
            if(val === 1) cell.classList.add("wall");
            else if(val === 2) {{
                let dot = document.createElement("div");
                dot.className = "dot";
                cell.appendChild(dot);
            }}
            
            if(pac.x === x && pac.y === y) {{
                let p = document.createElement("div");
                p.className = "pacman";
                cell.appendChild(p);
            }}
            if(ghost.x === x && ghost.y === y) {{
                let gh = document.createElement("div");
                gh.className = "ghost";
                cell.appendChild(gh);
            }}
            g.appendChild(cell);
        }}
    }}
    document.getElementById("score").innerText = score;
}}

window.setDir = function(nx, ny) {{ dx = nx; dy = ny; }}

document.addEventListener("keydown", (e) => {{
    let key = e.key.toLowerCase();
    if(key === "arrowup" || key === "w") setDir(0, -1);
    if(key === "arrowdown" || key === "s") setDir(0, 1);
    if(key === "arrowleft" || key === "a") setDir(-1, 0);
    if(key === "arrowright" || key === "d") setDir(1, 0);
}});

// Swipe support for mobile
let tX = 0; let tY = 0;
let gridEl = document.getElementById("grid");
gridEl.addEventListener('touchstart', e => {{ tX = e.changedTouches[0].screenX; tY = e.changedTouches[0].screenY; }}, {{passive: false}});
gridEl.addEventListener('touchmove', e => {{ e.preventDefault(); }}, {{passive: false}});
gridEl.addEventListener('touchend', e => {{
    let ex = e.changedTouches[0].screenX; let ey = e.changedTouches[0].screenY;
    let diffX = ex - tX; let diffY = ey - tY;
    if(Math.abs(diffX) > Math.abs(diffY)) {{ if(diffX > 30) setDir(1, 0); else if(diffX < -30) setDir(-1, 0); }}
    else {{ if(diffY > 30) setDir(0, 1); else if(diffY < -30) setDir(0, -1); }}
}}, {{passive: false}});

function update() {{
    let nx = pac.x + dx; let ny = pac.y + dy;
    if(map[ny*w + nx] !== 1) {{
        pac.x = nx; pac.y = ny;
        if(map[ny*w + nx] === 2) {{
            map[ny*w + nx] = 0;
            score += 10;
        }}
    }}
    checkDeath();
    draw();
}}

function moveGhost() {{
    let dirs = [[0,-1],[0,1],[-1,0],[1,0]];
    // Simple logic: move towards pacman if possible
    let bestDist = 9999;
    let bestDir = [0,0];
    for(let d of dirs) {{
        let nx = ghost.x + d[0]; let ny = ghost.y + d[1];
        if(map[ny*w + nx] !== 1) {{
            let dist = Math.abs(nx - pac.x) + Math.abs(ny - pac.y);
            if(dist < bestDist) {{ bestDist = dist; bestDir = d; }}
        }}
    }}
    ghost.x += bestDir[0]; ghost.y += bestDir[1];
    checkDeath();
    draw();
}}

function checkDeath() {{
    if(pac.x === ghost.x && pac.y === ghost.y) {{
        if (score > myHighScore) {{
            set(ref(db, 'pacman_highscores/' + currentUser), score);
        }}
        clearInterval(gameInterval);
        clearInterval(ghostInterval);
        document.getElementById("gameOver").style.display = "block";
    }}
}}

gameInterval = setInterval(update, 200);
ghostInterval = setInterval(moveGhost, 400);

draw();
</script>
</body>
</html>
"""
reset_html = '<button class="btn" style="width:200px; margin-top:20px; background:#ff4b4b; font-size:1.2em;" onclick="resetGame()">🔄 YENİDEN BAŞLAT</button>' if kimsin == "Mert" else ""
html_code = html_code.replace("<!-- RESET_BTN -->", reset_html)

components.html(html_code, height=800)
