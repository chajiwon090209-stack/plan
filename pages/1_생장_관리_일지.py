import streamlit as st

# 1. 페이지 정의 (app.py와 pages/1_생장_관리_일지.py 연결)
main_page = st.Page("app.py", title="생장 환경 진단", icon="🌱", default=True)
log_page = st.Page("pages/1_생장_관리_일지.py", title="생장 관리 일지", icon="📋")

# 2. 내비게이션 메뉴 생성 (사이드바에 강제 표시)
pg = st.navigation({
    "메뉴": [main_page, log_page]
})

# 페이지 기본 설정
st.set_page_config(page_title="PlantGrowth AI", page_icon="🌿", layout="wide")

# 세션 상태(Session State) 초기화
if "plant_logs" not in st.session_state:
    st.session_state.plant_logs = []

# 원예작물 데이터베이스
PLANT_DB = {
    "방울토마토": {"min_temp": 18, "max_temp": 27, "tip": "영양생장기에는 과습을 피하고, 개화기/수분기에는 적절한 온도를 유지해야 결실율이 높아집니다."},
    "상추": {"min_temp": 15, "max_temp": 20, "tip": "고온(25℃ 이상) 지속 시 꽃대가 올라오는 추대 현상이 발생하여 품질이 떨어집니다."},
    "바질": {"min_temp": 20, "max_temp": 30, "tip": "추위에 매우 약하므로 15℃ 이하로 떨어지지 않도록 보온 관리가 필요합니다."},
    "딸기": {"min_temp": 17, "max_temp": 23, "tip": "수확기 고온은 과실을 무르게 하므로 통풍과 온도 관리가 필수적입니다."},
    "파프리카": {"min_temp": 20, "max_temp": 28, "tip": "주야간 온도차가 너무 크면 착과율이 떨어지므로 정밀한 온도 관리가 필요합니다."},
    "샤인머스켓": {"min_temp": 20, "max_temp": 30, "tip": "수확기 광량이 부족하면 당도 축적이 지연되므로 적절한 채광 관리가 중요합니다."}
}

# 내비게이션에 따라 선택된 페이지 실행 (상단 메뉴 바 자동 생성)
if st.session_state.get("current_page") != pg:
    pg.run()
