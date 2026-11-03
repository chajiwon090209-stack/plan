import streamlit as st

st.set_page_config(page_title="작물 진단 및 AI 상담", page_icon="🔬", layout="wide")

st.title("🌱 스마트팜 원예 작물 진단 및 AI 상담 플랫폼")
st.caption("작물의 생장 환경을 진단하고 실시간 AI 상담사에게 궁금한 점을 물어보세요.")

# 로그인 상태 확인 (선택 사항 안내용)
current_user = st.session_state.get("username", "비로그인 사용자")
st.info(현재 접속 중인 사용자: **{current_user}**)

# 상단 탭 나누기 (진단 홈 / AI 상담사)
tab1, tab2 = st.tabs(["🔬 작물 환경 진단", "🤖 실시간 AI 원예 상담사"])

with tab1:
    st.subheader("🔬 스마트 원예 작물 환경 진단")
    crop_name = st.selectbox("재배 작물 선택", ["방울토마토", "상추", "딸기", "샤인머스캣", "기타 작물"])
    temp = st.slider("현재 재배 온도 (°C)", 10, 35, 22)
    humidity = st.slider("토양 수분 상태 (%)", 10, 100, 60)
    light = st.selectbox("광환경 (조도) 조건", ["양지(강한 직사광선)", "반양지", "음지", "LED 인공광"])
    growth_stage = st.selectbox("현재 생장 단계", ["발아/유묘기", "영양생장기", "개화/수분기", "결실/수확기"])

    if st.button("🚀 종합 생장 진단 시작", use_container_width=True):
        if humidity < 30:
            result_msg = "건조 경고: 수분 공급이 시급합니다!"
        elif humidity > 85:
            result_msg = "과습 경고: 배수 및 통풍을 강화하세요!"
        elif temp > 30:
            result_msg = "고온 경고: 차광막 설치 및 환기가 필요합니다."
        else:
            result_msg = "적정 상태: 아주 훌륭한 재배 환경입니다! ✨"

        st.success(f"📌 **[{crop_name}] 진단 결과:** {result_msg}")

        if "plant_logs" not in st.session_state:
            st.session_state.plant_logs = []
        
        st.session_state.plant_logs.append({
            "작물명": crop_name,
            "현재온도": f"{temp}°C",
            "토양수분": "적정" if 30 <= humidity <= 85 else ("건조" if humidity < 30 else "과습"),
            "생장단계": growth_stage,
            "광조건": light,
            "진단결과": result_msg
        })
        st.info("💡 진단 내용이 '생장 관리 일지'에 자동으로 기록되었습니다!")

with tab2:
    st.subheader("🤖 실시간 AI 원예 생장 상담사")
    
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "안녕하세요! 원예 작물 AI 상담사입니다. 재배 환경이나 작물 상태에 대해 무엇이든 물어보세요! 🌱"}
        ]

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            if "img" in message and message["img"] is not None:
                st.image(message["img"], width=200)
            st.markdown(message["content"])

    uploaded_file = st.file_uploader("🌱 [선택] 진단할 작물 사진 업로드 (JPG, PNG)", type=["jpg", "jpeg", "png"])

    if user_input := st.chat_input("예: 엽색이 변하는 원인이 뭘까요?"):
        current_msg = {"role": "user", "content": user_input, "img": uploaded_file}
        st.session_state.chat_messages.append(current_msg)
        
        with st.chat_message("user"):
            if uploaded_file is not None:
                st.image(uploaded_file, width=200)
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("AI가 분석 중입니다..."):
                if uploaded_file is not None:
                    ai_response = "📸 **[AI 이미지 진단]** 업로드해주신 사진을 분석한 결과, 일시적인 과습 또는 영양 불균형 초기 증상으로 보입니다. 배수 상태를 점검해 보세요!"
                elif "토마토" in user_input:
                    ai_response = "🍅 방울토마토는 주야간 온도차를 5~10°C 유지하는 것이 당도 향상에 좋습니다."
                else:
                    ai_response = f"🌱 입력하신 '{user_input}'에 대해 정밀 환경 제어를 유지하는 것이 중요합니다. 작물 사진을 함께 첨부해 주시면 더욱 정확하게 진단해 드릴 수 있습니다!"
                st.markdown(ai_response)
        
        st.session_state.chat_messages.append({"role": "assistant", "content": ai_response, "img": None})
        st.rerun()
