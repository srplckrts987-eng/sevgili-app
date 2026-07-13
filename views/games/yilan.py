import streamlit as st
import streamlit.components.v1 as components

st.title("🐍 Yılan (Snake)")
st.write("Klasik yılan oyunu. Skorunuzu artırın!")

kimsin = st.session_state.current_user

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ background: #222; color: white; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; margin: 0; padding: 20px; }}
    canvas {{ background: #111; border: 2px solid #555; border-radius: 5px; }}
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

<h2>Skor: <span id="score" style="color:#ff4b4b;">0</span></h2>
<canvas id="gameCanvas" width="300" height="300"></canvas>
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
    const scoreRef = ref(db, 'snake_highscores');
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

    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const TILE = 15;
    let snake = [{{x: 10, y: 10}}];
    let apple = {{x: 5, y: 5}};
    let dx = 1; let dy = 0;
    let score = 0;
    let gameLoop;
    
    function reset() {{
        if (score > myHighScore) {{
            set(ref(db, 'snake_highscores/' + currentUser), score);
        }}
        snake = [{{x: 10, y: 10}}];
        dx = 1; dy = 0; score = 0;
        document.getElementById("score").innerText = score;
        placeApple();
    }}
    
    window.reset = reset;

    function placeApple() {{
        apple.x = Math.floor(Math.random() * (canvas.width / TILE));
        apple.y = Math.floor(Math.random() * (canvas.height / TILE));
    }}
    
    window.setDir = function(nx, ny) {{
        if(nx !== 0 && dx !== 0) return;
        if(ny !== 0 && dy !== 0) return;
        dx = nx; dy = ny;
    }}
    
    // Klavye
    document.addEventListener("keydown", (e) => {{
        let key = e.key.toLowerCase();
        if(key === "arrowup" || key === "w") setDir(0, -1);
        if(key === "arrowdown" || key === "s") setDir(0, 1);
        if(key === "arrowleft" || key === "a") setDir(-1, 0);
        if(key === "arrowright" || key === "d") setDir(1, 0);
    }});
    
    // Dokunmatik Kaydırma
    let touchX = 0; let touchY = 0;
    canvas.addEventListener('touchstart', e => {{
        touchX = e.changedTouches[0].screenX;
        touchY = e.changedTouches[0].screenY;
    }}, {{passive: false}});
    
    canvas.addEventListener('touchmove', e => {{ e.preventDefault(); }}, {{passive: false}});
    
    canvas.addEventListener('touchend', e => {{
        let ex = e.changedTouches[0].screenX;
        let ey = e.changedTouches[0].screenY;
        let diffX = ex - touchX;
        let diffY = ey - touchY;
        
        if(Math.abs(diffX) > Math.abs(diffY)) {{
            if(diffX > 30) setDir(1, 0);
            else if(diffX < -30) setDir(-1, 0);
        }} else {{
            if(diffY > 30) setDir(0, 1);
            else if(diffY < -30) setDir(0, -1);
        }}
    }}, {{passive: false}});
    
    function update() {{
        let head = {{x: snake[0].x + dx, y: snake[0].y + dy}};
        
        if(head.x < 0 || head.x >= canvas.width/TILE || head.y < 0 || head.y >= canvas.height/TILE) return reset();
        
        for(let part of snake) {{
            if(head.x === part.x && head.y === part.y) return reset();
        }}
        
        snake.unshift(head);
        
        if(head.x === apple.x && head.y === apple.y) {{
            score += 10;
            document.getElementById("score").innerText = score;
            placeApple();
        }} else {{
            snake.pop();
        }}
        
        ctx.fillStyle = "#111";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = "red";
        ctx.fillRect(apple.x * TILE, apple.y * TILE, TILE-1, TILE-1);
        
        ctx.fillStyle = "lime";
        for(let part of snake) {{
            ctx.fillRect(part.x * TILE, part.y * TILE, TILE-1, TILE-1);
        }}
    }}
    
    placeApple();
    gameLoop = setInterval(update, 200);
</script>
</body>
</html>
"""
kimsin = st.session_state.current_user
reset_html = '<button class="btn" style="width:200px; margin-top:20px; background:#ff4b4b; font-size:1.2em;" onclick="reset()">🔄 YENİDEN BAŞLAT</button>' if kimsin == "Mert" else ""
html_code = html_code.replace("<!-- RESET_BTN -->", reset_html)

components.html(html_code, height=750)
