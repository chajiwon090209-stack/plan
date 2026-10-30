import streamlit as st

st.set_page_config(page_title="원예작물 과일 합치기 게임", page_icon="🎮", layout="wide")

st.title("🎮 미니 게임: 원예작물 과일 합치기 (수박 게임)")
st.caption("작은 씨앗부터 대형 샤인머스캣과 수박까지! 같은 과일을 합쳐서 더 큰 작물로 진화시켜 보세요!")

# HTML 및 JavaScript로 구현된 미니 게임 컴포넌트 삽입
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-color: #0e1117;
            color: white;
            font-family: sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        #game-container {
            width: 400px;
            height: 500px;
            margin: 20px auto;
            border: 3px solid #34d399;
            border-radius: 12px;
            background: #1e293b;
            position: relative;
            overflow: hidden;
        }
        .fruit {
            position: absolute;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
            color: #fff;
            box-shadow: inset -3px -3px 6px rgba(0,0,0,0.3);
            cursor: pointer;
            transition: transform 0.1s;
        }
        #score-board {
            font-size: 20px;
            margin-bottom: 10px;
            color: #34d399;
            font-weight: bold;
        }
        .btn {
            background-color: #34d399;
            color: #0e1117;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 10px;
        }
        .btn:hover {
            background-color: #059669;
            color: white;
        }
    </style>
</head>
<body>

    <div id="score-board">현재 점수: <span id="score">0</span> 점</div>
    
    <div id="game-container" onclick="dropFruit(event)">
        <!-- 과일들이 생성되는 공간 -->
    </div>

    <button class="btn" onclick="resetGame()">게임 다시 시작</button>

    <script>
        let score = 0;
        const container = document.getElementById('game-container');
        const scoreDisplay = document.getElementById('score');

        // 과일 단계 정의 (이름, 크기반지름, 색상, 점수)
        const fruits = [
            { name: '🌱 씨앗', radius: 15, color: '#a3e635', score: 2 },
            { name: '🍓 딸기', radius: 22, color: '#f43f5e', score: 5 },
            { name: '🍅 방울토마토', radius: 30, color: '#ef4444', score: 10 },
            { name: '🍇 포도', radius: 40, color: '#a855f7', score: 20 },
            { name: '🍈 샤인머스캣', radius: 52, color: '#84cc16', score: 40 },
            { name: '🍉 대형 수박', radius: 68, color: '#10b981', score: 80 }
        ];

        function dropFruit(e) {
            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = Math.min(e.clientY - rect.top, 100); // 상단 부근에 생성

            createFruit(x, y, 0); // 항상 가장 작은 '씨앗'부터 떨어짐
        }

        function createFruit(x, y, level) {
            if (level >= fruits.length) level = fruits.length - 1;
            const f = fruits[level];

            const div = document.createElement('div');
            div.className = 'fruit';
            div.style.width = (f.radius * 2) + 'px';
            div.style.height = (f.radius * 2) + 'px';
            div.style.left = (x - f.radius) + 'px';
            div.style.top = y + 'px';
            div.style.backgroundColor = f.color;
            div.innerHTML = f.name;

            // 간단한 중력 및 바닥 정지 시뮬레이션
            let currentY = y;
            let fallInterval = setInterval(() => {
                currentY += 4;
                // 바닥에 닿았을 때 (컨테이너 높이 500 - 반지름 * 2)
                if (currentY >= 500 - (f.radius * 2)) {
                    currentY = 500 - (f.radius * 2);
                    clearInterval(fallInterval);
                }
                div.style.top = currentY + 'px';
            }, 20);

            div.onclick = function(event) {
                event.stopPropagation();
                // 클릭하면 다음 단계로 진화!
                score += f.score;
                scoreDisplay.innerText = score;
                
                const nextX = parseInt(div.style.left) + f.radius;
                const nextY = parseInt(div.style.top);
                container.removeChild(div);
                
                if (level + 1 < fruits.length) {
                    createFruit(nextX, nextY, level + 1);
                }
            };

            container.appendChild(div);
        }

        function resetGame() {
            container.innerHTML = '';
            score = 0;
            scoreDisplay.innerText = score;
        }
    </script>
</body>
</html>
"""

# Streamlit 내부에 HTML 게임 렌더링 (높이 650px)
st.components.v1.html(game_html, height=650)
