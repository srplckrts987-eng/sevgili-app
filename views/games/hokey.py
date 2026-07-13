import streamlit as st
import streamlit.components.v1 as components

st.title("🏒 Masa Hokeyi")
st.write("Diskleri karşı tarafa yollayarak gol atmaya çalışın! (Aynı anda ekran başında oynamanız önerilir)")

kimsin = st.session_state.current_user

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: 'Inter', sans-serif; display: flex; flex-direction: column; align-items: center; user-select: none; }}
    #gameArea {{ position: relative; width: 300px; height: 500px; background-color: #e0f7fa; border: 4px solid #333; border-radius: 10px; overflow: hidden; touch-action: none; }}
    .goal {{ position: absolute; width: 100px; height: 10px; background-color: red; left: 100px; }}
    #goalTop {{ top: 0; }}
    #goalBottom {{ bottom: 0; }}
    .center-line {{ position: absolute; width: 100%; height: 4px; background-color: #ccc; top: 250px; left: 0; }}
    #puck {{ position: absolute; width: 20px; height: 20px; background-color: black; border-radius: 50%; transform: translate(-50%, -50%); }}
    .paddle {{ position: absolute; width: 40px; height: 40px; background-color: #ff4b4b; border-radius: 50%; transform: translate(-50%, -50%); z-index: 10; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
    #paddleMert {{ background-color: #007bff; }}
    #paddleRumeysa {{ background-color: #ff69b4; }}
    .score-board {{ display: flex; justify-content: space-between; width: 300px; font-size: 1.5em; font-weight: bold; margin-bottom: 10px; }}
</style>
</head>
<body>
<div class="score-board">
    <div id="scoreMert" style="color: #007bff;">Mert: 0</div>
    <div id="scoreRumeysa" style="color: #ff69b4;">Rüm: 0</div>
</div>
<div id="gameArea">
    <div class="goal" id="goalTop"></div>
    <div class="goal" id="goalBottom"></div>
    <div class="center-line"></div>
    <div id="puck" style="left: 150px; top: 250px;"></div>
    <div class="paddle" id="paddleMert" style="left: 150px; top: 400px;"></div>
    <div class="paddle" id="paddleRumeysa" style="left: 150px; top: 100px;"></div>
</div>
<p style="margin-top:10px; color:#555; text-align:center;">{kimsin} olarak oynuyorsunuz. Kırmızı alanlara diski (siyah) sokarak gol atın!</p>
<!-- RESET_BTN -->
<script type="module">
import {{ initializeApp }} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import {{ getDatabase, ref, onValue, set, update }} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-database.js";

const app = initializeApp({{ databaseURL: "https://sevgiliwepsite-default-rtdb.europe-west1.firebasedatabase.app" }});
const db = getDatabase(app);
const gameRef = ref(db, 'hockey_game');

const currentUser = "{kimsin}";
let state = {{ 
    puck: {{x: 150, y: 250, vx: 0, vy: 0}},
    pMert: {{x: 150, y: 400}},
    pRumeysa: {{x: 150, y: 100}},
    scores: {{Mert: 0, Rumeysa: 0}}
}};

let isMaster = currentUser === "Mert"; // Mert fizik motorunu çalıştırır
let lastTime = performance.now();

onValue(gameRef, (snapshot) => {{
    let data = snapshot.val();
    if(data) {{
        if(!isMaster) {{ state.puck = data.puck; state.scores = data.scores; }}
        if(currentUser !== "Mert") state.pMert = data.pMert || state.pMert;
        if(currentUser !== "Rümeysa") state.pRumeysa = data.pRumeysa || state.pRumeysa;
        if(isMaster) state.scores = data.scores || state.scores;
        render();
    }}
}});

// Kontrolcü Mantığı
const area = document.getElementById("gameArea");
const myPaddleId = currentUser === "Mert" ? "paddleMert" : "paddleRumeysa";

area.addEventListener('pointermove', (e) => {{
    let rect = area.getBoundingClientRect();
    let x = e.clientX - rect.left;
    let y = e.clientY - rect.top;
    
    // Kendi yarısına kısıtlama
    if(currentUser === "Mert" && y < 270) y = 270;
    if(currentUser === "Rümeysa" && y > 230) y = 230;
    
    if(x < 20) x = 20; if(x > 280) x = 280;
    if(y < 20) y = 20; if(y > 480) y = 480;
    
    if(currentUser === "Mert") state.pMert = {{x, y}};
    else state.pRumeysa = {{x, y}};
    
    update(gameRef, currentUser === "Mert" ? {{pMert: {{x, y}}}} : {{pRumeysa: {{x, y}}}});
}});

// Fizik Motoru (Sadece "Mert" çalıştırır)
if(isMaster) {{
    setInterval(() => {{
        let dt = 0.03; // 30ms step
        let p = state.puck;
        p.x += p.vx * dt;
        p.y += p.vy * dt;
        
        // Sürtünme
        p.vx *= 0.99; p.vy *= 0.99;
        
        // Duvar çarpmaları
        if(p.x <= 10 || p.x >= 290) p.vx *= -1;
        
        // Gol kontrolü
        if(p.y <= 10) {{
            if(p.x >= 100 && p.x <= 200) {{ state.scores.Mert++; resetPuck(); }}
            else {{ p.y = 10; p.vy *= -1; }}
        }}
        if(p.y >= 490) {{
            if(p.x >= 100 && p.x <= 200) {{ state.scores.Rumeysa++; resetPuck(); }}
            else {{ p.y = 490; p.vy *= -1; }}
        }}
        
        // Paddle Çarpmaları
        checkCollision(p, state.pMert);
        checkCollision(p, state.pRumeysa);
        
        update(gameRef, {{puck: p, scores: state.scores}});
    }}, 30);
}}

function checkCollision(puck, paddle) {{
    let dx = puck.x - paddle.x;
    let dy = puck.y - paddle.y;
    let dist = Math.sqrt(dx*dx + dy*dy);
    if(dist < 30) {{ // 10px puck + 20px paddle rad
        // Hız vektörü ekle
        puck.vx = (dx / dist) * 300;
        puck.vy = (dy / dist) * 300;
    }}
}}

function resetPuck() {{
    state.puck = {{x: 150, y: 250, vx: 0, vy: 0}};
}}

window.resetGame = function() {{
    if(currentUser === "Mert") {{
        state.scores = {{Mert: 0, Rumeysa: 0}};
        resetPuck();
        update(gameRef, {{scores: state.scores, puck: state.puck}});
    }}
}}

function render() {{
    document.getElementById("puck").style.left = state.puck.x + "px";
    document.getElementById("puck").style.top = state.puck.y + "px";
    document.getElementById("paddleMert").style.left = state.pMert.x + "px";
    document.getElementById("paddleMert").style.top = state.pMert.y + "px";
    document.getElementById("paddleRumeysa").style.left = state.pRumeysa.x + "px";
    document.getElementById("paddleRumeysa").style.top = state.pRumeysa.y + "px";
    document.getElementById("scoreMert").innerText = "Mert: " + state.scores.Mert;
    document.getElementById("scoreRumeysa").innerText = "Rüm: " + state.scores.Rumeysa;
}}

</script>
</body>
</html>
"""
reset_html = '<button style="margin-top:20px; padding:10px; background:#ff4b4b; color:white; border:none; border-radius:5px; font-weight:bold; cursor:pointer;" onclick="resetGame()">🔄 SIFIRLA</button>' if kimsin == "Mert" else ""
html_code = html_code.replace("<!-- RESET_BTN -->", reset_html)

components.html(html_code, height=650)
