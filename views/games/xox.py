import streamlit as st
import streamlit.components.v1 as components

st.title("❌ XOX (Tic Tac Toe)")
st.write("Sıfır gecikmeli çok oyunculu XOX.")

kimsin = st.session_state.current_user

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ font-family: 'Inter', sans-serif; display: flex; flex-direction: column; align-items: center; }}
    .board {{ display: grid; grid-template-columns: repeat(3, 100px); grid-gap: 5px; background-color: #333; padding: 5px; border-radius: 10px; margin-top:20px; }}
    .cell {{ width: 100px; height: 100px; background-color: white; display: flex; align-items: center; justify-content: center; font-size: 3em; font-weight: bold; cursor: pointer; }}
    .cell:hover {{ background-color: #f0f0f0; }}
    .turn {{ font-size: 1.5em; font-weight: bold; margin-bottom: 10px; }}
    .btn {{ margin-top: 20px; padding: 10px 20px; font-size: 1.2em; background-color: #ff4b4b; color: white; border: none; border-radius: 8px; cursor: pointer; display: none; }}
</style>
</head>
<body>
<div class="turn" id="turnIndicator">Yükleniyor...</div>
<div class="board" id="board">
    <div class="cell" id="c_0" onclick="play(0)"></div><div class="cell" id="c_1" onclick="play(1)"></div><div class="cell" id="c_2" onclick="play(2)"></div>
    <div class="cell" id="c_3" onclick="play(3)"></div><div class="cell" id="c_4" onclick="play(4)"></div><div class="cell" id="c_5" onclick="play(5)"></div>
    <div class="cell" id="c_6" onclick="play(6)"></div><div class="cell" id="c_7" onclick="play(7)"></div><div class="cell" id="c_8" onclick="play(8)"></div>
</div>
<button class="btn" id="resetBtn" onclick="resetGame()">Yeniden Başlat</button>

<script type="module">
import {{ initializeApp }} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import {{ getDatabase, ref, onValue, set }} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-database.js";

const app = initializeApp({{ databaseURL: "https://sevgiliwepsite-default-rtdb.europe-west1.firebasedatabase.app" }});
const db = getDatabase(app);
const gameRef = ref(db, 'xox_game');

const currentUser = "{kimsin}";
let gameState = null;

onValue(gameRef, (snapshot) => {{
    let data = snapshot.val();
    if (!data) {{ resetGame(); return; }}
    gameState = data;
    if (!gameState.board) gameState.board = Array(9).fill("");
    render();
}});

function render() {{
    let turnText = (gameState.turn === currentUser) ? "Senin Sıran!" : "Sıra onda...";
    if(gameState.winner) {{
        turnText = gameState.winner === "Berabere" ? "Oyun Berabere!" : "Kazanan: " + gameState.winner + " 🏆";
        if(currentUser === "Mert") document.getElementById("resetBtn").style.display = "block";
    }} else {{
        document.getElementById("resetBtn").style.display = "none";
    }}
    document.getElementById("turnIndicator").innerText = turnText;
    
    for(let i=0; i<9; i++) {{
        let mark = gameState.board[i] || "";
        let cell = document.getElementById("c_" + i);
        cell.innerText = mark === "Mert" ? "X" : (mark === "Rümeysa" ? "O" : "");
        cell.style.color = mark === "Mert" ? "#007bff" : "#ff4b4b";
    }}
}}

window.play = function(i) {{
    if(!gameState || gameState.winner || gameState.board[i]) return;
    if(gameState.turn !== currentUser) {{ alert("Sıra sende değil!"); return; }}
    
    gameState.board[i] = currentUser;
    
    // Kazanma Kontrolü
    const wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
    let won = false;
    for(let combo of wins) {{
        if(gameState.board[combo[0]] && gameState.board[combo[0]] === gameState.board[combo[1]] && gameState.board[combo[1]] === gameState.board[combo[2]]) {{
            gameState.winner = currentUser;
            won = true; break;
        }}
    }}
    
    if(!won && !gameState.board.includes("")) gameState.winner = "Berabere";
    if(!won) gameState.turn = currentUser === "Mert" ? "Rümeysa" : "Mert";
    
    set(gameRef, gameState);
}}

window.resetGame = function() {{
    set(gameRef, {{ turn: "Mert", board: Array(9).fill(""), winner: null }});
}}
</script>
</body>
</html>
"""
components.html(html_code, height=500)
