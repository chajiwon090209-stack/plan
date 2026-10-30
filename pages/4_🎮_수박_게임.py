import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="원예작물 과일 합치기 게임", page_icon="🎮", layout="wide")

st.title("🎮 미니 게임: 원예작물 과일 합치기 (수박 게임)")
st.caption("상자 안을 클릭하여 씨앗을 떨어뜨리세요! 같은 과일끼리 닿으면 더 큰 작물로 합쳐집니다.")

# 1. 로그인 사용자 확인 및 비로그인 사용자 랜덤 닉네임 부여
if "username" in st.session_state and st.session_state.username:
    current_player = st.session_state.username
else:
    if "random_player_name" not in st.session_state:
        random_titles = ["새싹농부", "스마트팜마스터", "방울토마토조아", "샤인머스캣헌터", "초보연구원", "식물집사"]
        st.session_state.random_player_name = f"{random.choice(random_titles)}_{random.randint(10, 99)}"
    current_player = st.session_state.random_player_name

# 2. 리더보드(점수판) 세션 상태 초기화
if "game_leaderboard" not in st.session_state:
    st.session_state.game_leaderboard = [
        {"name": "스마트팜고수", "score": 2450},
        {"name": "원예학과_김학생", "score": 1820},
        {"name": "식물사랑", "score": 1350}
    ]

# 화면 레이아웃 분할 (왼쪽: 게임 화면 / 오른쪽: 실시간 순위 점수판)
col_game, col_rank = st.columns([2, 1], gap="large")

with col_game:
    # 파이썬 구문 충돌을 방지하기 위해 일반 문자열 조합 사용
    game_html = (
        "<!DOCTYPE html>"
        "<html>"
        "<head>"
        "<meta charset='utf-8'>"
        "<script src='https://cdnjs.cloudflare.com/ajax/libs/matter-js/0.19.0/matter.min.js'></script>"
        "<style>"
        "body { background-color: #0e1117; color: white; font-family: sans-serif; text-align: center; margin: 0; padding: 0; }"
        "#score-board { font-size: 20px; margin: 8px 0; color: #34d399; font-weight: bold; }"
        "#game-box { width: 380px; height: 520px; margin: 0 auto; border: 4px solid #34d399; border-radius: 12px; background: #1e293b; position: relative; cursor: pointer; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }"
        ".btn { background-color: #34d399; color: #0e1117; border: none; padding: 10px 24px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; margin-top: 12px; }"
        ".btn:hover { background-color: #059669; color: white; }"
        "</style>"
        "</head>"
        "<body>"
        f"<div id='score-board'>플레이어: {current_player} | 점수: <span id='score'>0</span> 점</div>"
        "<div id='game-box'></div>"
        "<button class='btn' onclick='startGame()'>게임 다시 시작</button>"
        "<script>"
        "const { Engine, Render, Runner, Bodies, Composite, Events } = Matter;"
        "let engine, render, runner;"
        "let score = 0;"
        "let canDrop = true;"
        "const FRUITS = ["
        "{ radius: 15, color: '#a3e635', label: '🌱', score: 2 },"
        "{ radius: 22, color: '#f43f5e', label: '🍓', score: 4 },"
        "{ radius: 30, color: '#ef4444', label: '🍅', score: 8 },"
        "{ radius: 38, color: '#a855f7', label: '🍇', score: 16 },"
        "{ radius: 48, color: '#84cc16', label: '🍈', score: 32 },"
        "{ radius: 60, color: '#10b981', label: '🍉', score: 64 }"
        "];"
        "function startGame() {"
        "  const box = document.getElementById('game-box');"
        "  box.innerHTML = '';"
        "  score = 0;"
        "  document.getElementById('score').innerText = score;"
        "  canDrop = true;"
        "  engine = Engine.create();"
        "  render = Render.create({ element: box, engine: engine, options: { width: 380, height: 520, wireframes: false, background: '#1e293b' } });"
        "  const ground = Bodies.rectangle(190, 535, 380, 30, { isStatic: true, render: { fillStyle: '#334155' } });"
        "  const leftWall = Bodies.rectangle(-10, 260, 20, 520, { isStatic: true, render: { fillStyle: '#334155' } });"
        "  const rightWall = Bodies.rectangle(390, 260, 20, 520, { isStatic: true, render: { fillStyle: '#334155' } });"
        "  Composite.add(engine.world, [ground, leftWall, rightWall]);"
        "  Render.run(render);"
        "  runner = Runner.create();"
        "  Runner.run(runner, engine);"
        "  box.addEventListener('click', function(e) {"
        "    if (!canDrop) return;"
        "    const rect = box.getBoundingClientRect();"
        "    let x = e.clientX - rect.left;"
        "    x = Math.max(30, Math.min(350, x));"
        "    let level = Math.random() < 0.7 ? 0 : 1;"
        "    dropFruit(x, 30, level);"
        "    canDrop = false;"
        "    setTimeout(function() { canDrop = true; }, 350);"
        "  });"
        "  Events.on(engine, 'collisionStart', function(event) {"
        "    event.pairs.forEach(function(pair) {"
        "      let b1 = pair.bodyA;"
        "      let b2 = pair.bodyB;"
        "      if (b1.fruitLevel !== undefined && b2.fruitLevel !== undefined) {"
        "        if (b1.fruitLevel === b2.fruitLevel) {"
        "          let lvl = b1.fruitLevel;"
        "          if (lvl < FRUITS.length - 1) {"
        "            Composite.remove(engine.world, [b1, b2]);"
        "            let nx = (b1.position.x + b2.position.x) / 2;"
        "            let ny = (b1.position.y + b2.position.y) / 2;"
        "            dropFruit(nx, ny, lvl + 1);"
        "            score += FRUITS[lvl + 1].score;"
        "            document.getElementById('score').innerText = score;"
        "          }"
        "        }"
        "      }"
        "    });"
        "  });"
        "  Events.on(render, 'afterRender', function() {"
        "    let ctx = render.context;"
        "    let bodies = Composite.allBodies(engine.world);"
        "    bodies.forEach(function(b) {"
        "      if (b.fruitLevel !== undefined) {"
        "        let f = FRUITS[b.fruitLevel];"
        "        ctx.font = (f.radius * 0.9) + 'px sans-serif';"
        "        ctx.textAlign = 'center';"
        "        ctx.textBaseline = 'middle';"
        "        ctx.fillText(f.label, b.position.x, b.position.y);"
        "      }"
        "    });"
        "  });"
        "}"
        "function dropFruit(x, y, level) {"
        "  let f = FRUITS[level];"
        "  let body = Bodies.circle(x, y, f.radius, { restitution: 0.2, friction: 0.1, render: { fillStyle: f.color } });"
        "  body.fruitLevel = level;"
        "  Composite.add(engine.world, body);"
        "}"
        "window.onload = startGame;"
        "</script>"
        "</body>"
        "</html>"
    )
    components.html(game_html, height=640)

with col_rank:
    st.markdown("### 🏆 명예의 전당 (실시간 순위)")
    st.caption(f"현재 접속자: **{current_player}**")
    
    with st.container(border=True):
        st.markdown("#### 🥇 TOP 3 랭킹")
        sorted_rank = sorted(st.session_state.game_leaderboard, key=lambda x: x['score'], reverse=True)
        for idx, rank in enumerate(sorted_rank[:3]):
            medal = ["🥇", "🥈", "🥉"][idx]
            st.markdown(f"{medal} **{rank['name']}** — `{rank['score']}점`")
            
    with st.container(border=True):
        st.markdown("💡 **게임 팁**")
        st.markdown("""
        - 같은 과일끼리 닿으면 합쳐집니다!
        - 로그인하면 본인 이름으로 순위에 기록됩니다.
        - 비로그인 시에는 귀여운 랜덤 닉네임이 부여됩니다!
        """)
