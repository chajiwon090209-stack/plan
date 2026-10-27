import streamlit as st

st.set_page_config(page_title="로그인", page_icon="🔑", layout="wide")

st.title("🔑 사용자 인증 및 로그인")
st.caption("원예작물 생장 환경 진단 및 일지 시스템에 오신 것을 환영합니다. 로그인 후 기록을 안전하게 유지하세요.")

# 세션 상태에 로그인 정보 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# 이미 로그인된 경우
if st.session_state.logged_in:
    st.success(f"🎉 현재 **{st.session_state.username}**님 계정으로 로그인되어 있습니다!")
    
    if st.button("🚪 로그아웃"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# 로그인이 안 되어 있는 경우
else:
    with st.form("login_form"):
        st.subheader("📝 로그인 정보 입력")
        input_id = st.text_input("아이디 (학번 또는 이름)", placeholder="예: 0학년 0반 홍길동")
        input_pw = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
        
        submitted = st.form_submit_button("로그인")
        
        if submitted:
            if input_id.strip() != "":
                # 간단한 로그인 성공 처리 (어떤 아이디든 입력하면 바로 로그인되도록 설정)
                st.session_state.logged_in = True
                st.session_state.username = input_id.strip()
                st.success(f"✅ 환영합니다, {st.session_state.username}님! 로그인이 완료되었습니다.")
                st.rerun()
            else:
                st.warning("⚠️ 아이디(이름)를 입력해 주세요!")
