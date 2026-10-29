import streamlit as st
import pandas as pd

st.set_page_config(page_title="원예작물 맞춤형 생장 환경 진단 시스템", page_icon="🌱", layout="wide")

# 세션 상태 초기화
if "plant_logs" not in st.session_state:
    st.session_state.plant_logs = []

st.title("🌱 원예작물 맞춤형 생장 환경 진단 시스템")
st.caption("원하는 작물과 현재 재배 환경 조건을 입력하면 생리 반응에 맞춘 정밀 가이드를 제시합니다.")

# 화면을 좌우 2열로 분할
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("### 📥 재배 환경 입력")
    
    # 1. 작물 이름 입력
    crop_name = st.text_input("진단할 작물 이름을 입력하세요", value="방울토마토", placeholder="예: 방울토마토, 상추 등")
    
    # 2. 온도 슬라이더
    current_temp = st.slider("현재 재배 온도 (°C)", 0, 40, 22)
    
    # 3. 토양 수분 상태 선택
    soil_moisture = st.selectbox("토양 수분 상태", ["건조", "적정", "과습"])
    
    # 4. 생장 단계 선택
    growth_stage = st.selectbox("현재 작물의 생장 단계", ["발아/유묘기", "영양생장기", "개화/수분기", "결실/수확기"])
    
    # 5. 광 조건 (조도) 선택 -> st.pills를 활용해 깔끔한 버튼 형태로 개선!
    st.markdown("광 조건 (조도)")
    light_condition = st.pills(
        "광 조건 선택",
        ["음지", "반양지", "양지(강한 직사광선)", "LED 인공광"],
        default="양지(강한 직사광선)",
        label_visibility="collapsed"
    )

with col_right:
    st.markdown("### 💡 생육 진단 결과 및 정밀 가이드")
    
    # 온도 적정성 평가 로직
    if 18 <= current_temp <= 27:
        temp_status = "적정"
        temp_msg = f"적정 온도: 현재 온도({current_temp}°C)가 최적 생육 범위(18~27°C) 내에 잘 유지되고 있습니다."
        st.success(f"✅ {temp_msg}")
    elif current_temp < 18:
        temp_status = "저온 경고"
        temp_msg = f"저온 경고: 현재 온도({current_temp}°C)가 다소 낮습니다. 보온 조치를 고려하세요."
        st.warning(f"⚠️ {temp_msg}")
    else:
        temp_status = "고온 경고"
        temp_msg = f"고온 경고: 현재 온도({current_temp}°C)가 높습니다. 환기 및 차광이 필요합니다."
        st.error(f"🚨 {temp_msg}")
        
    # 맞춤형 리포트 박스
    with st.container(border=True):
        st.markdown(f"#### 🧬 [{crop_name}] 생육 진단 리포트")
        st.markdown(f"""
        - **생장 단계 분석:** 현재 `{growth_stage}` 단계입니다. 단계별 맞춤 수분(`{soil_moisture}`) 및 양분 관리법을 적용하세요.
        - **광환경 진단:** 선택된 `{light_condition}` 환경에 맞춰 광합성 효율을 극대화하세요.
        - **원예생명 진단 팁:** 영양생장기에는 과습을 피하고, 개화기/수분기에는 적절한 온도를 유지해야 결실율이 높아집니다.
        """)
    
    st.markdown("")
    
    # 일지 추가 버튼 (눈에 띄게 배치)
    if st.button("📋 이 진단 기록을 생장 일지에 추가", type="primary", use_container_width=True):
        new_log = {
            "작물명": crop_name,
            "현재온도": f"{current_temp}°C",
            "토양수분": soil_moisture,
            "생장단계": growth_stage,
            "광조건": light_condition,
            "진단결과": temp_status
        }
        st.session_state.plant_logs.insert(0, new_log)
        st.success("🎉 진단 기록이 생장 관리 일지에 성공적으로 추가되었습니다!")
