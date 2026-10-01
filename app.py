import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="PlantGrowth AI", page_icon="🌿", layout="wide")

# 세션 상태(Session State) 초기화
if "plant_logs" not in st.session_state:
    st.session_state.plant_logs = []

# 원예작물 생육 적정 환경 데이터
PLANT_DATA = {
    "방울토마토": {"min_temp": 18, "max_temp": 27, "humidity": "60-70%", "light": "양지(강한 광량)", "tip": "영양생장기에는 과습을 피하고, 개화기에는 적절한 온도를 유지해야 결실율이 높아집니다."},
    "상추": {"min_temp": 15, "max_temp": 20, "humidity": "70-80%", "light": "반양지", "tip": "고온(25°C 이상) 지속 시 꽃대가 올라오는 추대 현상이 발생하여 품질이 떨어집니다."},
    "바질": {"min_temp": 20, "max_temp": 30, "humidity": "50-60%", "light": "양지", "tip": "추위에 매우 약하므로 15°C 이하로 떨어지지 않도록 관리해야 합니다."},
    "딸기": {"min_temp": 17, "max_temp": 23, "humidity": "60-70%", "light": "양지", "tip": "수확기 고온은 과실을 무르게 하므로 통풍과 온도 관리가 필수적입니다."}
}

# 메인 화면 구성
st.title("🌱 원예작물 맞춤형 생장 환경 진단 시스템")
st.caption("작물 종류와 현재 재배 환경을 입력하면 생리 반응에 맞춘 관리 방법을 제시합니다.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 재배 환경 입력")
    selected_plant = st.selectbox("진단할 작물 선택", list(PLANT_DATA.keys()))
    current_temp = st.slider("현재 재배 온도 (°C)", 0, 40, 22)
    water_status = st.select_slider("토양 수분 상태", options=["건조", "적정", "과습"])
    
with col2:
    st.subheader("💡 생육 진단 결과 및 가이드")
    info = PLANT_DATA[selected_plant]
    
    # 온도 진단 로직
    if current_temp < info["min_temp"]:
        st.warning(f"⚠️ **저온 주의:** 현재 온도({current_temp}°C)가 생육 적정 하한선({info['min_temp']}°C)보다 낮습니다. 생육이 지연될 수 있으니 보온이 필요합니다.")
    elif current_temp > info["max_temp"]:
        st.error(f"🚨 **고온 스트레스 경고:** 현재 온도({current_temp}°C)가 적정 상한선({info['max_temp']}°C)을 초과했습니다. 통풍 및 차광 처리가 필요합니다.")
    else:
        st.success(f"✅ **적정 온도:** 현재 온도가 생육 최적 범위({info['min_temp']}~{info['max_temp']}°C)에 속해 있습니다.")

    # 생리적 관리 팁 안내
    st.info(f"📌 **{selected_plant} 맞춤 관리 팁:**\n{info['tip']}")
    
    # 일지 저장 버튼
    if st.button("💾 이 진단 기록을 생장 일지에 추가"):
        st.session_state.plant_logs.append({
            "작물명": selected_plant,
            "현재온도": f"{current_temp}°C",
            "토양수분": water_status,
            "진단결과": "적정" if info["min_temp"] <= current_temp <= info["max_temp"] else "환경 개선 필요"
        })
        st.success("✅ 생장 일지에 기록되었습니다! 왼쪽 사이드바의 '생장 관리 일지' 페이지에서 확인하세요.")
