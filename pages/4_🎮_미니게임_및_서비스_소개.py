import streamlit as st
import streamlit.components.v1 as components
import random

# ==========================================
# 1. 페이지 기본 설정 및 플레이어 세션 식별
# - 미니게임 및 서비스 소개 페이지 타이틀, 아이콘, 와이드 레이아웃 설정
# - 로그인된 유저 이름이 없으면 임의의 닉네임(새싹농부_XX)을 생성하여 게임 세션 바인딩
# ==========================================
st.set_page_config(page_title="미니게임 및 서비스 소개", page_icon="🎮", layout="wide")

tab1, tab2 = st.tabs(["🎮 수박 게임 (미니게임)", "📖 서비스 소개 및 가이드"])

with tab1:
    st.title("🎮 원예작물 과일 합치기 게임")
    st.caption("상자를 클릭해 씨앗을 떨어뜨리고 더 큰 작물로 진화시켜 보세요!")

    if "username" in st.session_state and st.session_state.username:
        current_player = st.session_state.username
    else:
        if "random_player_name" not in st.session_state:
            st.session_state.random_player_name = f"새싹농부_{random.randint(10, 99)}"
        current_player = st.session_state.random_player_name

    col_g, col_r = st.columns([2, 1], gap="large")

    with col_g:
        # ==========================================
        # 2-1. Matter.js 물리 엔진 기반 원예 과일 합치기 미니게임 렌더링
        # - HTML5 Canvas와 Matter.js 라이브러리를 활용해 중력, 충돌 감지, 작물 진화 및 점수 합산 구현
        # ==========================================
        game_html = (
            "<!DOCTYPE html><html><head><meta charset='utf-8'>"
            "<script src='https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js'></script>"
            "<style>"
            "body { background-color: #0e1117; color: white; font-family: sans-serif; text-align: center; margin: 0; }"
            "#score-board { font-size: 18px; margin: 6px 0; color: #34d399; font-weight: bold; }"
            "#game-box { width: 360px; height: 500px; margin: 0 auto; border: 4px solid #34d399; border-radius: 12px; background: #1e293b; position: relative; cursor: pointer; }"
            ".btn { background-color: #34d399; color: #0e1117; border: none; padding: 8px 20px; font-size: 15px; font-weight: bold; border-radius: 6px; cursor: pointer; margin-top: 10px; }"
            "</style></head><body>"
            f"<div id='score-board'>플레이어: {current_player} | 점수: <span id='score'>0</span> 점</div>"
            "<div id='game-box'></div><button class='btn' onclick='startGame()'>다시 시작</button>"
            "<script>"
            "const { Engine, Render, Runner, Bodies, Composite, Events } = Matter;"
            "let engine, render, runner, score = 0, canDrop = true;"
            "const FRUITS = [{r:15, c:'#a3e635', l:'🌱', s:2}, {r:22, c:'#f43f5e', l:'🍓', s:4}, {r:30, c:'#ef4444', l:'🍅', s:8}, {r:38, c:'#a855f7', l:'🍇', s:16}, {r:48, c:'#84cc16', l:'🍈', s:32}, {r:60, c:'#10b981', l:'🍉', s:64}];"
            "function startGame() {"
            "  const box = document.getElementById('game-box'); box.innerHTML = ''; score = 0; document.getElementById('score').innerText = score; canDrop = true;"
            "  engine = Engine.create(); render = Render.create({ element: box, engine: engine, options: { width: 360, height: 500, wireframes: false, background: '#1e293b' } });"
            "  Composite.add(engine.world, [Bodies.rectangle(180, 515, 360, 30, {isStatic:true}), Bodies.rectangle(-10, 250, 20, 500, {isStatic:true}), Bodies.rectangle(370, 250, 20, 500, {isStatic:true})]);"
            "  Render.run(render); runner = Runner.create(); Runner.run(runner, engine);"
            "  box.addEventListener('click', e => {"
            "    if (!canDrop) return; let x = Math.max(30, Math.min(330, e.clientX - box.getBoundingClientRect().left));"
            "    let body = Bodies.circle(x, 20, FRUITS[0].r, {restitution:0.2, render:{fillStyle:FRUITS[0].c}}); body.fl = 0;"
            "    Composite.add(engine.world, body); canDrop = false; setTimeout(() => canDrop = true, 350);"
            "  });"
            "  Events.on(engine, 'collisionStart', ev => {"
            "    ev.pairs.forEach(p => {"
            "      let b1 = p.bodyA, b2 = p.bodyB;"
            "      if (b1.fl !== undefined && b1.fl === b2.fl && b1.fl < FRUITS.length - 1) {"
            "        Composite.remove(engine.world, [b1, b2]); let lvl = b1.fl + 1;"
            "        let nb = Bodies.circle((b1.position.x+b2.position.x)/2, (b1.position.y+b2.position.y)/2, FRUITS[lvl].r, {restitution:0.2, render:{fillStyle:FRUITS[lvl].c}});"
            "        nb.fl = lvl; Composite.add(engine.world, nb); score += FRUITS[lvl].s; document.getElementById('score').innerText = score;"
            "      }"
            "    });"
            "  });"
            "  Events.on(render, 'afterRender', () => {"
            "    let ctx = render.context; Composite.allBodies(engine.world).forEach(b => {"
            "      if (b.fl !== undefined) { ctx.font = (FRUITS[b.fl].r*0.9)+'px sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText(FRUITS[b.fl].l, b.position.x, b.position.y); }"
            "    });"
            "  });"
            "}"
            "window.onload = startGame;"
            "</script></body></html>"
        )
        components.html(game_html, height=600)

    with col_r:
        # ==========================================
        # 2-2. 미니게임 명예의 전당 (Leaderboard)
        # - 현재 접속 중인 플레이어 정보와 실시간 상위 랭커 점수판 출력
        # ==========================================
        st.markdown("### 🏆 명예의 전당")
        st.caption(f"접속자: **{current_player}**")
        with st.container(border=True):
            st.markdown("🥇 **스마트팜고수** — `2450점`")
            st.markdown("🥈 **원예학과_김학생** — `1820점`")
            st.markdown("🥉 **식물사랑** — `1350점`")

with tab2:
    # ==========================================
    # 3. 서비스 소개 및 플랫폼 활용 가이드
    # - 고등학교 원예/식품생명공학 학습 지원 목적 및 4대 핵심 기능 안내
    # ==========================================
    st.title("📖 서비스 소개 및 도움말")
    st.markdown("""
    ### 🌱 스마트팜 원예 생장 분석 플랫폼이란?
    고등학교 원예 및 식품생명공학 학습을 지원하기 위해 제작된 웹 기반 지능형 플랫폼입니다.
    
    * **핵심 기능 안내:**
      1. **작물 환경 진단 & AI 상담:** 온·습도 및 광환경을 진단하고 AI를 통해 맞춤형 처방을 받습니다.
      2. **생장 관리 & 캘린더:** 일지 기록과 사진 캘린더로 작물의 성장 과정을 체계적으로 추적합니다.
      3. **데이터 시각화 & 공유:** 수집된 데이터를 그래프로 분석하고 친구와 코드를 주고받으며 협업합니다.
      4. **미니게임:** 학습 중간 쉬어갈 수 있는 원예 테마의 수박 게임을 즐길 수 있습니다.
    """)
