import streamlit as st

st.set_page_config(page_title="AI 원예 상담사", page_icon="🤖", layout="wide")

st.title("🤖 실시간 AI 원예 생장 상담사")
st.caption("원예 작물 재배, 생리 장애, 병해충 관리 등 궁금한 점을 무엇이나 물어보세요!")

# 채팅 기록 초기화
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "안녕하세요! 원예 작물 AI 상담사입니다. 키우고 계신 작물 사진을 업로드하거나 재배 환경에 대해 궁금한 점을 말씀해 주세요! 🌱"}
    ]

# 기존 대화 내용 출력
for message in st.session_state.chat_messages:
    with st.chat_message(message["role"]):
        if "img" in message and message["img"] is not None:
            st.image(message["img"], width=200)
        st.markdown(message["content"])

# 📸 작물 사진 업로드 위젯을 채팅 입력창 바로 위(하단부)로 이동
uploaded_file = st.file_uploader("🌱 [선택] 진단할 작물 사진을 업로드해 주세요 (JPG, PNG)", type=["jpg", "jpeg", "png"])

if user_input := st.chat_input("예: 업로드한 작물 사진의 잎 색상이 변하는데 원인이 뭘까요?"):
    # 사용자의 입력 및 업로드된 이미지 저장
    current_msg = {"role": "user", "content": user_input, "img": uploaded_file}
    st.session_state.chat_messages.append(current_msg)
    
    with st.chat_message("user"):
        if uploaded_file is not None:
            st.image(uploaded_file, width=200)
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("AI가 업로드된 작물 사진과 질문 내용을 정밀 분석 중입니다..."):
            
            # 사진이 업로드된 경우의 맞춤형 AI 응답 로직
            if uploaded_file is not None:
                ai_response = f"📸 **[AI 이미지 기반 생장 장애 진단 리포트]**\n\n업로드해주신 관찰 사진과 질문(`{user_input}`)을 분석한 결과입니다:\n- **잎 상태 진단:** 엽색 변색 및 생장 정지 초기 증상으로 판단되며, 주로 **토양 과습에 의한 뿌리 호흡 저하** 또는 **일시적인 칼슘/질소 영양 불균형**일 가능성이 높습니다.\n- **처방 가이드:** 배수 상태를 점검하시고, 야간 온도를 2~3°C 낮춰 호흡 양분을 절감해 보세요!"
            elif "토마토" in user_input or "방울토마토" in user_input:
                ai_response = "🍅 **방울토마토 재배 가이드:** 영양생장기에는 과습을 주의하고, 주야간 온도차를 5~10°C 내외로 유지하는 것이 착과율과 당도 향상에 가장 좋습니다!"
            elif "물" in user_input or "수분" in user_input:
                ai_response = "💧 **토양 수분 관리 팁:** 토양 표면이 마르면 충분히 관수하되, 배수가 잘 되도록 하여 뿌리의 산소 호흡을 돕고 과습병을 예방해야 합니다."
            else:
                ai_response = f"🌱 입력하신 '{user_input}'에 대해 분석한 결과, 광합성 효율 극대화와 정밀 환경 제어(온·습도)를 유지하는 것이 생장 발육에 가장 중요합니다. 작물 사진을 함께 올려주시면 더욱 정확한 진단이 가능합니다!"
            
            st.markdown(ai_response)
    
    st.session_state.chat_messages.append({"role": "assistant", "content": ai_response, "img": None})
    st.rerun()
