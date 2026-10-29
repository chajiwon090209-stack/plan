import streamlit as st

st.set_page_config(page_title="AI 원예 상담사", page_icon="🤖", layout="wide")

st.title("🤖 실시간 AI 원예 생장 상담사")
st.caption("원예 작물 재배, 생리 장애, 병해충 관리 등 궁금한 점을 무엇이나 물어보세요!")

# 대화 기록을 저장할 세션 상태 초기화
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "안녕하세요! 원예 작물 AI 상담사입니다. 키우고 계신 작물이나 재배 환경에 대해 궁금한 점을 말씀해 주세요! 🌱"}
    ]

# 기존 대화 기록 화면에 출력
for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자가 채팅창에 입력했을 때
if user_input := st.chat_input("예: 토마토 생육에 가장 적절한 온도와 광량 조건을 알려줘"):
    # 사용자 메시지 추가 및 출력
    st.session_state.chat_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI의 실시간 응답 생성 (수행평가 시연용 스마트 응답 로직 또는 API 연동)
    with st.chat_message("assistant"):
        with st.spinner("AI가 최적의 원예 정보를 분석하는 중입니다..."):
            # 키워드 기반 맞춤 응답 시뮬레이션 (실제 API 연동 전 발표 시연용으로 매우 안정적입니다)
            if "토마토" in user_input or "방울토마토" in user_input:
                ai_response = "🍅 **방울토마토 재배 가이드:** 영양생장기에는 과습을 주의하고, 주야간 온도차를 5~10°C 내외로 유지하는 것이 착과율과 당도 향상에 가장 좋습니다!"
            elif "물" in user_input or "수분" in user_input:
                ai_response = "💧 **토양 수분 관리 팁:** 토양 표면이 마르면 충분히 관수(물주기)하되, 배수가 잘 되도록 하여 뿌리의 산소 호흡을 돕고 과습병을 예방해야 합니다."
            elif "온도" in user_input or "더위" in user_input or "추위" in user_input:
                ai_response = "🌡️ **온도 관리 핵심:** 대부분의 원예 작물은 18°C~28°C 범위가 최적입니다. 고온 시에는 차광막과 환기를, 저온 시에는 보온 조치를 취해 스트레스를 최소화하세요."
            else:
                ai_response = f"🌱 입력하신 '{user_input}'에 대해 분석한 결과, 작물의 광합성 효율 극대화와 정밀 환경 제어(온·습도)를 유지하는 것이 생장 발육에 가장 중요합니다. 추가로 궁금한 생장 단계를 알려주세요!"
            
            st.markdown(ai_response)
    
    # AI 응답 기록 저장
    st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})
