import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="PlantGrowth AI", page_icon="🌿", layout="wide")

# 세션 상태(Session State) 초기화
if "plant_logs" not in st.session_state:
    st.session_state.plant_logs = []

# 원예작물 데이터베이스 (자유 입력 작물 탐색 기준)
PLANT_DB = {
    "방울토마토": {"min_temp": 18, "max_temp": 27, "tip": "영양생장기에는 과습을 피하고, 개화기/수분기에는 적절한 온도를 유지해야 결실율이 높아집니다."},
    "상추": {"min_temp": 15, "max_temp": 20, "tip": "고온(25°C 이상) 지속 시 꽃대가 올라오는 추대 현상이 발생하여 품질이 떨어집니다."},
    "바질": {"min_temp": 20, "max_temp": 30, "tip": "추위에 매우 약하므로 15°C 이하로 떨어지지 않도록 보온 관리가 필요합니다."},
    "딸기": {"min_temp": 17, "max_temp": 23, "tip": "수확기 고온은 과실을 무르게 하므로 통풍과 온도 관리가 필수적입니다."},
    "파프리카": {"min_temp": 20, "max_temp": 28, "tip": "주야간 온도차가 너무 크면 착과율이 떨어지므로 정밀한 온도 관리가 필요합니다."},
    "샤인머스캣": {"min_temp": 20, "max_temp": 30, "tip": "수확기 광량이 부족하면 당도 축적이 지연되므로 적절한 채광 관리가 중요합니다."}
}

# 메인 화면 구성
st.title("🌱 원예작물 맞춤형 생장 환경 진단 시스템")
st.caption("원하는 작물과 현재 재배 환경 조건을 입력하면 생리 반응에 맞춘 정밀 가이드를 제시합니다.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 재배 환경 입력")
    
    # 1. 작물 직접 입력 (text_input)
    user_plant = st.text_input("진단할 작물 이름을 입력하세요", value="방울토마토", placeholder="예: 방울토마토, 샤인머스캣, 파프리카 등")
    
    # 2. 재배 온도
    current_temp = st.slider("현재 재배 온도 (°C)", 0, 40, 22)
    
    # 3. 토양 수분 상태
    water_status = st.select_slider("토양 수분 상태", options=["건조", "적정", "과습"])
    
    # 4. 새로 추가된 환경 변수: 생장 단계
    growth_stage = st.selectbox("현재 작물의 생장 단계", ["발아/유묘기", "영양생장기", "개화/수분기", "결실/수확기"])
    
    # 5. 새로 추가된 환경 변수: 광 조건
    light_condition = st.radio("광 조건 (조도)", ["음지", "반양지", "양지(강한 직사광선)", "LED 인공광"], horizontal=True)

with col2:
    st.subheader("💡 생육 진단 결과 및 정밀 가이드")
    
    clean_plant_name = user_plant.strip()
    
    # 데이터베이스 검색 또는 기본 알고리즘 적용
    if clean_plant_name in PLANT_DB:
        info = PLANT_DB[clean_plant_name]
        min_t, max_t = info["min_temp"], info["max_temp"]
        custom_tip = info["tip"]
    else:
        # DB에 없는 새로운 작물일 경우 생리적 기본 기준값 자동 설정
        min_t, max_t = 18, 28
        custom_tip = f"입력하신 **'{clean_plant_name}'**은(는) 생장 단계[{growth_stage}]에 맞춰 적정 온·습도 유지 및 통풍 관리가 중요한 원예작물입니다."

    # 온도 진단 결과
    if current_temp < min_t:
        st.warning(f"⚠️ **저온 주의:** 현재 온도({current_temp}°C)가 생육 적정 하한선({min_t}°C)보다 낮습니다. 생육 지연 및 냉해 위험이 있으니 보온 조치가 필요합니다.")
        temp_result = "저온 경고"
    elif current_temp > max_t:
        st.error(f"🚨 **고온 스트레스 경고:** 현재 온도({current_temp}°C)가 적정 상한선({max_t}°C)을 초과했습니다. 호흡량 증가로 인한 영양 소모가 심해지니 차광 및 환기가 필요합니다.")
        temp_result = "고온 경고"
    else:
        st.success(f"✅ **적정 온도:** 현재 온도가 최적 생육 범위({min_t}~{max_t}°C) 내에 잘 유지되고 있습니다.")
        temp_result = "적정"

    # 생장 단계 & 광 조건 맞춤 진단 가이드
    st.info(f"""
    📌 **[{clean_plant_name}] 생육 진단 리포트**
    - **생장 단계 분석:** 현재 **{growth_stage}** 단계입니다. 단계별 맞춤 수분 및 양분 관리법을 적용하세요.
    - **광환경 진단:** 선택된 **[{light_condition}]** 환경에 맞춰 광합성 효율을 극대화하세요.
    - **원예생명 진단 팁:** {custom_tip}
    """)
    
    # 일지 저장 버튼
    if st.button("💾 이 진단 기록을 생장 일지에 추가"):
        st.session_state.plant_logs.append({
            "작물명": clean_plant_name,
            "현재온도": f"{current_temp}°C",
            "토양수분": water_status,
            "생장단계": growth_stage,
            "광조건": light_condition,
            "진단결과": temp_result
        })
        st.success("✅ 생장 일지에 성공적으로 기록되었습니다! 왼쪽 사이드바의 '생장 관리 일지' 페이지에서 확인하세요.")
