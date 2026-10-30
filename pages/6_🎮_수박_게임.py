import streamlit as st

st.set_page_config(page_title="원예작물 과일 합치기 게임", page_icon="🎮", layout="wide")

st.title("🎮 미니 게임: 원예작물 과일 합치기 (수박 게임)")
st.caption("클릭한 위치로 과일이 떨어집니다! 같은 과일끼리 부딪히면 더 큰 작물로 합성되어 점수가 올라갑니다.")

# Matter.js 2D 물리 엔진 기반의 수박 게임 HTML/JS
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <!-- Matter.js 물리 엔진 라이브러리 불러오기 -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js"></script>
    <style>
        body {
            background-color: #0e1117;
            color: white;
            font-family: 'Pretendard', sans-serif;
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
        #canvas-container {
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
        canvas {
            border-radius: 8px;
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
            transition: 0.2s;
        }
        .btn:hover {
            background-color: #059669;
            color: white;
        }
    </style>
</head>
<body>

    <div id="score-board">현재 점수: <span id="score">0</span> 점</div>
    <div id="canvas-container"></div>
    <button class="btn" onclick="initGame()">게임 다시 시작</button>

    <script>
        const { Engine, Render, Runner, Bodies, Composite, Events, Body } = Matter;

        let engine, render, runner;
        let score = 0;
        let canDrop = true;

        // 과일 단계 설정 (반지름, 색상, 라벨, 점수)
        const FRUITS = [
            { radius: 15, color: '#a3e635', label: '🌱', name: '씨앗', score: 2 },
            { radius: 22, color: '#f43f5e', label: '🍓', name: '딸기', score: 4 },
            { radius: 30, color: '#ef4444', label: '🍅', name: '방울토마토', score: 8 },
            { radius: 38, color: '#a855f7', label: '🍇', name: '포도', score: 16 },
            { radius: 48, color: '#84cc16', label: '🍈', name: '샤인머스캣', score: 32 },
            { radius: 62, color: '#10b981', label: '🍉', name: '수박', score: 64 }
        ];

        function initGame() {
            const container = document.getElementById('canvas-container');
            container.innerHTML = '';
            
            score = 0;
            document.getElementById('score').innerText = score;
            canDrop = true;

            // 1. 물리 엔진 및 렌더러 생성
            engine = Engine.create();
            render = Render.create({
                element: container,
                engine: engine,
                options: {
                    width: 400,
                    height:
