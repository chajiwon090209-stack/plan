import streamlit as st
import random

st.set_page_config(page_title="원예작물 과일 합치기 게임", page_icon="🎮", layout="wide")

st.title("🎮 미니 게임: 원예작물 과일 키우기 & 합치기")
st.caption("버튼을 눌러 과일을 심고, 같은 단계의 작물이 만나면 더 큰 단계로 진화시켜 보세요!")

# 세션 상태로 게임 점수 및 작물 단계 관리
if "game_score" not in st.session_state:
    st.session_state.game_score = 0
if "farm_stage" not in st.session_state:
    st.session_state.farm_stage = 0

# 과일/작물 진화 단계 정의
FRUIT_STEPS = [
    {"name": "씨앗", "emoji": "🌱", "score": 2},
    {"name": "딸기", "emoji": "🍓", "score": 5},
    {"name": "방울토마토", "emoji": "🍅", "score": 10},
    {"name": "포도", "emoji": "🍇", "score": 20},
    {"name": "샤인머스캣", "emoji": "🍈", "score": 40},
    {"name": "대형 수박", "emoji": "🍉", "score": 100}
]

current = FRUITS_STEP = FRUIT_STEPS[st.session_state.farm_stage]

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 🌾 현재 재배 중인 작물")
    with st.container(border=True):
        st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{current['emoji']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>단계: {current['name']}</h3>", unsafe_allow_html=True)
    
    st.metric("현재 획득 점수", f"{st.session_state.game_score} 점")

with col2:
    st.markdown("### 🕹️ 작물 관리 및 합치기 액션")
    st.write("버튼을 눌러 물을 주거나 햇빛을 쬐어주면 작물이 성장합니다!")
    
    if st.button("💧 물 주기 (성장 시도)", use_container_width=True, type="primary"):
        if st.session_state.farm_stage < len(FRUIT_STEPS) - 1:
            st.session_state.farm_stage += 1
            added_score = FRUIT_STEPS[st.session_state.farm_stage]['score']
            st.session_state.game_score += added_score
            st.success(f"🎉 작물이 무럭무럭 자라서 **{FRUIT_STEPS[st.session_state.farm_stage]['name']}({FRUIT_STEPS[st.session_state.farm_stage]['emoji']})**(으)로 진화했습니다! (+{added_score}점)")
            st.rerun()
        else:
            st.balloons()
            st.success("🏆 축하합니다! 이미 최고 단계인 대형 수박까지 완벽하게 키워내셨습니다!")

    if st.button("☀️ 햇빛 쬐어주기 (무작위 보너스)", use_container_width=True):
        bonus = random.randint(5, 15)
        st.session_state.game_score += bonus
        st.info(f"☀️ 따스한 햇빛을 받아 광합성이 활발해졌습니다! 보너스 점수 +{bonus}점 획득!")
        st.rerun()

    st.markdown("---")
    if st.button("🔄 게임 초기화 (처음부터 다시)", use_container_width=True):
        st.session_state.game_score = 0
        st.session_state.farm_stage = 0
        st.success("게임이 초기화되었습니다.")
        st.rerun()

st.markdown("---")
st.markdown("### 📈 진화의 고리 (작물 도감)")
cols = st.columns(len(FRUIT_STEPS))
for idx, step in enumerate(FRUIT_STEPS):
    with cols[idx]:
        with st.container(border=True):
            st.markdown(f"<p style='text-align: center; font-size: 30px;'>{step['emoji']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 12px;'><b>{step['name']}</b></p>", unsafe_allow_html=True)
