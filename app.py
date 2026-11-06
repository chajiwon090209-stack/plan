import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 및 세션 상태 초기화
# - 브라우저 탭 설정, 레이아웃 구성
# - 테마 모드, 커스텀 모드 여부, 배경 및 폰트 색상 기본값 정의
# ==========================================
st.set_page_config(page_title="스마트팜 원예 플랫폼 로그인", page_icon="🔑", layout="wide")

# ==========================================
# 🌟 [공통 테마 적용] 세션 상태에 따른 전역 CSS 실시간 주입
# ==========================================
if "app_theme" not in st.session_state:
    st.session_state.app_theme = "다크 모드 (기본)"
if "custom_mode" not in st.session_state:
    st.session_state.custom_mode = False
if "custom_bg" not in st.session_state:
    st.session_state.custom_bg = "#0e1117"
if "custom_font" not in st.session_state:
    st.session_state.custom_font = "#ffffff"

# ==========================================
# 🎨 테마 모드별 기본 색상 프리셋(Preset) 딕셔너리 정의
# - 다크 모드, 라이트 모드, 스마트팜 그린 모드의 배경/글자 색상 매핑
# ==========================================
theme_presets = {
    "다크 모드 (기본)": {"bg": "#0e1117", "font": "#ffffff"},
    "라이트 모드 (밝은 화면)": {"bg": "#ffffff", "font": "#111827"},
    "스마트팜 그린 모드": {"bg": "#064e3b", "font": "#ecfdf5"}
}

# ==========================================
# 🌟 [핵심 로직] 현재 모드에 따른 배경 및 폰트 색상 동적 계산
# - 사용자가 커스텀 색상 모드를 켰는지 여부에 따라 프리셋 또는 커스텀 값 선택
# ==========================================
if st.session_state.custom_mode:
    current_bg = st.session_state.custom_bg
    current_font = st.session_state.custom_font
else:
    preset = theme_presets.get(st.session_state.app_theme, theme_presets["다크 모드 (기본)"])
    current_bg = preset["bg"]
    current_font = preset["font"]

# ==========================================
# 🌟 [CSS 스타일 주입] 웹앱 전체 테마 실시간 반영
# - Streamlit 메인 영역(.stApp), 마크다운 텍스트, 사이드바 배경 색상 강제 오버라이드
# ==========================================
st.markdown(
    f"""
    <style>
    /* 웹앱 전체 배경색 및 폰트 색상 변경 */
    .stApp {{
        background-color: {current_bg};
        color: {current_font};
    }}
    
    /* 주요 텍스트 및 마크다운 글자색 강제 적용 */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {{
        color: {current_font} !important;
    }}
    
    /* 사이드바 배경 및 텍스트 맞춤 조정 */
    section[data-testid="stSidebar"] {{
        background-color: {current_bg};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

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
