import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="원예작물 과일 합치기 게임", page_icon="🎮", layout="wide")

st.title("🎮 미니 게임: 원예작물 과일 합치기 (수박 게임)")
st.caption("상자 안을 클릭하여 씨앗을 떨어뜨리세요! 같은 과일끼리 닿으면 더 큰 작물로 합쳐집니다.")

# HTML 코드를 멀티라인 문자열 충돌 없이 안전하게 조립
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
    <style>
        body {
            background-color: #0e1117;
            color: white;
            font-family: sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        #score-board {
            font-size: 22px;
            margin: 10px 0;
            color: #34d399;
            font-weight: bold;
        }
        #game-box {
            width: 400px;
            height: 550px;
            margin: 0 auto;
            border: 4px solid #34d399;
            border-radius: 12px;
            background: #1e293b;
            position: relative;
            cursor: pointer;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }
        .btn {
            background-color: #34d399;
            color: #0e1117;
            border: none;
            padding: 10px 24px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
        }
        .btn:hover {
            background-color: #059669;
            color: white;
        }
    </style>
</head>
<body>

    <div id="score-board">현재 점수: <span id="score">0</span> 점</div>
    <div id="game-box"></div>
    <button class="btn" onclick="startGame()">게임 다시 시작</button>

    <script>
        const { Engine, Render, Runner, Bodies, Composite, Events } = Matter;

        let engine, render, runner;
        let score = 0;
        let canDrop = true;

        const FRUITS = [
            { radius: 16, color: '#a3e635', label: '🌱', score: 2 },
            { radius: 24, color: '#f43f5e', label: '🍓', score: 4 },
            { radius: 32, color: '#ef4444', label: '🍅', score: 8 },
            { radius: 40, color: '#a855f7', label: '🍇', score: 16 },
            { radius: 50, color: '#84cc16', label: '🍈', score: 32 },
            { radius: 64, color: '#10b981', label: '🍉', score: 64 }
        ];

        function startGame() {
            const box = document.getElementById('game-box');
            box.innerHTML = '';
            score = 0;
            document.getElementById('score').innerText = score;
            canDrop = true;

            engine = Engine.create();
            render = Render.create({
                element: box,
                engine: engine,
                options: {
                    width: 400,
                    height: 550,
                    wireframes: false,
                    background: '#1e293b'
                }
            });

            const ground = Bodies.rectangle(200, 565, 400, 30, { isStatic: true, render: { fillStyle: '#334155' } });
            const leftWall = Bodies.rectangle(-10, 275, 20, 550, { isStatic: true, render: { fillStyle: '#334155' } });
            const rightWall = Bodies.rectangle(410, 275, 20, 550, { isStatic: true, render: { fillStyle: '#334155' } });

            Composite.add(engine.world, [ground, leftWall, rightWall]);

            Render.run(render);
            runner = Runner.create();
            Runner.run(runner, engine);

            box.addEventListener('click', function(e) {
                if (!canDrop) return;
                const rect = box.getBoundingClientRect();
                let x = e.clientX - rect.left;
                x = Math.max(30, Math.min(370, x));

                let level = Math.random() < 0.7 ? 0 : 1; // 씨앗 또는 딸기 생성
                dropFruit(x, 30, level);

                canDrop = false;
                setTimeout(function() { canDrop = true; }, 350);
            });

            Events.on(engine, 'collisionStart', function(event) {
                event.pairs.forEach(function(pair) {
                    let b1 = pair.bodyA;
                    let b2 = pair.bodyB;

                    if (b1.fruitLevel !== undefined && b2.fruitLevel !== undefined) {
                        if (b1.fruitLevel === b2.fruitLevel) {
                            let lvl = b1.fruitLevel;
                            if (lvl < FRUITS.length - 1) {
                                Composite.remove(engine.world, [b1, b2]);
                                let nx = (b1.position.x + b2.position.x) / 2;
                                let ny = (b1.position.y + b2.position.y) / 2;
                                dropFruit(nx, ny, lvl + 1);

                                score += FRUITS[lvl + 1].score;
                                document.getElementById('score').innerText = score;
                            }
                        }
                    }
                });
            });

            Events.on(render, 'afterRender', function() {
                let ctx = render.context;
                let bodies = Composite.allBodies(engine.world);
                bodies.forEach(function(b) {
                    if (b.fruitLevel !== undefined) {
                        let f = FRUITS[b.fruitLevel];
                        ctx.font = (f.radius * 0.9) + 'px sans-serif';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillText(f.label, b.position.x, b.position.y);
                    }
                });
            });
        }

        function dropFruit(x, y, level) {
            let f = FRUITS[level];
            let body = Bodies.circle(x, y, f.radius, {
                restitution: 0.2,
                friction: 0.1,
                render: { fillStyle: f.color }
            });
            body.fruitLevel = level;
            Composite.add(engine.world, body);
        }

        window.onload = startGame;
    </script>
</body>
</html>
"""

components.html(game_html, height=680)
