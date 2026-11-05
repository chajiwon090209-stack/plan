import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 및 헤더 영역
# - 웹앱의 탭 제목, 아이콘 및 레이아웃(wide) 설정
# - 스마트팜 로그인 시스템 안내 타이틀 및 캡션 출력
# ==========================================
st.set_page_config(page_title="스마트팜 원예 플랫폼 로그인", page_icon="🔑", layout="wide")

st.title("🔑 사용자 인증 및 로그인")
st.caption("원예작물 생장 환경 진단 및 일지 시스템에 오신 것을 환영합니다. 로그인 후 기록을 안전하게 유지하세요.")

# ==========================================
# 2. 세션 상태(Session State) 초기화
# - 앱 전역에서 유저의 로그인 상태와 아이디를 유지하기 위한 변수 세팅
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

with st.container(border=True):
    st.markdown("### 📝 로그인 정보 입력")
    
    # ==========================================
    # 3-1. 로그인 완료 상태 분기 (Logout 처리)
    # - 이미 로그인된 경우 환영 문구와 로그아웃 버튼 제공
    # ==========================================
    if st.session_state.logged_in:
        st.success(f"🎉 현재 **{st.session_state.username}**님으로 로그인되어 있습니다!")
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
        
    # ==========================================
    # 3-2. 미로그인 상태 분기 (Login 입력 및 검증)
    # - 학번 또는 이름을 입력받고 공백 여부를 검증한 뒤 세션 갱신
    # ==========================================
    else:
        input_id = st.text_input("아이디 (학번 또는 이름)", placeholder="예: 0학년 0반 홍길동")
        input_pw = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
        
        if st.button("로그인", use_container_width=True):
            if input_id.strip():
                st.session_state.logged_in = True
                st.session_state.username = input_id.strip()
                st.success(f"환영합니다, {st.session_state.username}님! 왼쪽 사이드바에서 메뉴를 선택하여 이용해 주세요.")
                st.rerun()
            else:
                st.warning("⚠️ 아이디를 올바르게 입력해 주세요.")
