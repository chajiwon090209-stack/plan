import streamlit as st
from datetime import datetime

st.set_page_config(page_title="사용자 인증 및 로그인", page_icon="🔑", layout="wide")

st.title("🔑 사용자 인증 및 로그인")
st.caption("원예작물 생장 환경 진단 및 일지 시스템에 오신 것을 환영합니다. 로그인 후 기록을 안전하게 유지하세요.")

# 세션 상태 초기화 (로그인 여부 및 로그인 기록 저장용)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "login_history" not in st.session_state:
    st.session_state.login_history = []

# 이미 로그인된 상태일 때
if st.session_state.logged_in:
    st.success(f"✅ 환영합니다, **{st.session_state.username}**님! 로그인이 완료되었습니다.")
    
    # 💡 로그인 접속 기록(로그) 섹션 추가
    st.markdown("---")
    st.subheader("📋 최근 로그인 접속 기록")
    st.caption("본 계정으로 시스템에 접근한 인증 타임라인 기록입니다.")
    
    if st.session_state.login_history:
        import pandas as pd
        history_df = pd.DataFrame(st.session_state.login_history)
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("기록된 로그인 이력이 없습니다.")

    if st.button("로그아웃"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# 로그인이 안 된 상태일 때
else:
    with st.form("login_form"):
        st.subheader("📝 로그인 정보 입력")
        user_id = st.text_input("아이디 (학번 또는 이름)", placeholder="예: 2학년 3반 차귀금")
        user_pw = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
        
        submit_btn = st.form_submit_button("로그인")
        
        if submit_btn:
            if user_id.strip() != "":
                st.session_state.logged_in = True
                st.session_state.username = user_id
                
                # 🕒 현재 로그인 시각 기록 추가
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.login_history.insert(0, {
                    "접속자": user_id,
                    "인증 시각": current_time,
                    "상태": "성공 (Authorized)"
                })
                
                st.success(f"🎉 환영합니다, {user_id}님! 인증되었습니다.")
                st.rerun()
            else:
                st.warning("⚠️ 아이디(학번 또는 이름)를 입력해 주세요!")
