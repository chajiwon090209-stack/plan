import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="원예작물 과일 합치기 게임", page_icon="🎮", layout="wide")

st.title("🎮 미니 게임: 원예작물 과일 합치기 (수박 게임)")
st.caption("클릭한 위치로 과일이 떨어집니다! 같은 과일끼리 부딪히면 더 큰 작물로 합성되어 점수가 올라갑니다.")

# 2D 물리 엔진 Matter.js 기반 수박 게임
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
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
            font-
