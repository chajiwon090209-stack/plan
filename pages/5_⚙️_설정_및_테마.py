import streamlit as st

# ==========================================
# 1. 설정 페이지 기본 설정 및 세션 상태 초기화
# - 브라우저 탭 설정, 레이아웃 구성
# - 테마 모드, 커스텀 모드 여부, 배경 및 폰트 색상 기본값 정의
# ==========================================
st.set_page_config(page_title="설정 및 테마 변경", page_icon="⚙️", layout="wide")

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
# 🌟 [핵심] 웹앱 전체 CSS 스타일 실시간 주입
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

# ==========================================
# 2. UI 화면 구성
# ==========================================
st.title("⚙️ 앱 설정 및 테마 모드 변경")
st.caption("원하시는 화면 테마 모드를 선택하거나, 나만의 커스텀 색상을 지정하여 웹앱 전체 분위기를 꾸며보세요.")

with st.container(border=True):
    st.subheader("🎨 화면 테마 모드 선택")
    
    theme_options = ["다크 모드 (기본)", "라이트 모드 (밝은 화면)", "스마트팜 그린 모드"]
    current_index = theme_options.index(st.session_state.app_theme) if st.session_state.app_theme in theme_options else 0
    
    # 테마 라디오 버튼
    theme_choice = st.radio(
        "사용할 테마 모드를 선택하세요:",
        theme_options,
        index=current_index
    )
    
    st.markdown("---")
    
    # 사용자 지정 커스텀 색상 사용 여부 토글
    use_custom = st.checkbox("✨ 나만의 색상 직접 지정하기 (컬러 피커 사용)", value=st.session_state.custom_mode)
    
    if use_custom:
        col_c1, col_c2 = st.columns(2, gap="large")
        with col_c1:
            st.markdown("🖌️ **커스텀 배경 색상**")
            user_bg = st.color_picker("배경 컬러 선택:", st.session_state.custom_bg, key="picker_bg")
        with col_c2:
            st.markdown("✍️ **커스텀 폰트(글자) 색상**")
            user_font = st.color_picker("폰트 컬러 선택:", st.session_state.custom_font, key="picker_font")
    
    st.markdown("")

    # 설정 적용 버튼
    if st.button("✨ 테마 설정 즉시 적용하기", use_container_width=True):
        st.session_state.app_theme = theme_choice
        st.session_state.custom_mode = use_custom
        if use_custom:
            st.session_state.custom_bg = user_bg
            st.session_state.custom_font = user_font
        
        st.success(f"🎉 성공적으로 적용되었습니다! (현재 모드: {theme_choice})")
        st.rerun()

st.markdown("---")

# ==========================================
# 3. 현재 계정 및 시스템 설정 정보 요약 출력
# ==========================================
st.subheader("👤 현재 계정 및 시스템 정보")
current_user = st.session_state.get("username", "비로그인 사용자")
st.markdown(f"""
- **현재 접속 계정:** `{current_user}`
- **현재 적용된 테마 모드:** `{st.session_state.app_theme}`
- **적용된 배경 색상:** `{current_bg}`
- **적용된 폰트 색상:** `{current_font}`
- **플랫폼 버전:** SmartFarm Horticulture v2.7
""")
