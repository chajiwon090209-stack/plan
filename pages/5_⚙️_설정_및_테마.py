import streamlit as st

# ==========================================
# 1. 설정 페이지 기본 설정 및 테마 세션 초기화
# ==========================================
st.set_page_config(page_title="설정 및 테마 변경", page_icon="⚙️", layout="wide")

# 세션 상태에 테마, 포인트 색상, 폰트 색상 초기화
if "app_theme" not in st.session_state:
    st.session_state.app_theme = "다크 모드 (기본)"
if "custom_color" not in st.session_state:
    st.session_state.custom_color = "#1e293b"  # 기본 다크 배경 색상 (어두운 남색)
if "font_color" not in st.session_state:
    st.session_state.font_color = "#ffffff"  # 기본 흰색 폰트

# ==========================================
# 🌟 [핵심] 사용자가 고른 색상을 앱 전체 CSS에 실시간 반영
# ==========================================
st.markdown(
    f"""
    <style>
    /* 웹앱 전체 배경색 및 폰트 색상 변경 */
    .stApp {{
        background-color: {st.session_state.custom_color};
        color: {st.session_state.font_color};
    }}
    
    /* 주요 텍스트 및 마크다운 글자색 강제 적용 */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {{
        color: {st.session_state.font_color} !important;
    }}
    
    /* 사이드바 배경 및 텍스트 맞춤 조정 */
    section[data-testid="stSidebar"] {{
        background-color: {st.session_state.custom_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("⚙️ 앱 설정 및 테마 모드 변경")
st.caption("원하시는 화면 테마와 나만의 포인트 색상, 그리고 폰트 색상을 지정하여 웹앱 전체 분위기를 꾸며보세요.")

with st.container(border=True):
    st.subheader("🎨 화면 테마 및 색상 세부 설정")
    
    # ==========================================
    # 2-1. 화면 테마 모드 선택 라디오 버튼
    # ==========================================
    theme_choice = st.radio(
        "사용할 테마 모드를 선택하세요:",
        ["다크 모드 (기본)", "라이트 모드 (밝은 화면)", "스마트팜 그린 모드"],
        index=0 if st.session_state.app_theme == "다크 모드 (기본)" else (1 if st.session_state.app_theme == "라이트 모드 (밝은 화면)" else 2)
    )
    
    st.markdown("---")
    
    # ==========================================
    # 2-2. 듀얼 컬러 피커(Color Picker)
    # ==========================================
    col_c1, col_c2 = st.columns(2, gap="large")
    
    with col_c1:
        st.markdown("🖌️ **웹앱 전체 배경 색상**")
        user_color = st.color_picker("배경 컬러 선택:", st.session_state.custom_color, key="picker_point")
        
    with col_c2:
        st.markdown("✍️ **웹앱 전체 폰트(글자) 색상**")
        user_font_color = st.color_picker("폰트 컬러 선택:", st.session_state.font_color, key="picker_font")
    
    st.markdown("")

    # ==========================================
    # 2-3. 설정 적용 버튼 및 세션 상태 갱신
    # ==========================================
    if st.button("✨ 테마 및 색상 전체 적용하기", use_container_width=True):
        st.session_state.app_theme = theme_choice
        st.session_state.custom_color = user_color
        st.session_state.font_color = user_font_color
        st.success(f"🎉 성공적으로 설정이 적용되었습니다!\n- **선택 테마:** {theme_choice}\n- **배경 색상:** `{user_color}`\n- **폰트 색상:** `{user_font_color}`")
        st.rerun()  # 즉시 새로고침하여 전체 화면에 색상 반영

st.markdown("---")

# ==========================================
# 3. 현재 계정 및 시스템 설정 정보 요약 출력
# ==========================================
st.subheader("👤 현재 계정 및 시스템 정보")
current_user = st.session_state.get("username", "비로그인 사용자")
st.markdown(f"""
- **현재 접속 계정:** `{current_user}`
- **현재 적용된 테마:** `{st.session_state.app_theme}`
- **적용된 배경 색상:** `{st.session_state.custom_color}`
- **적용된 폰트 색상:** `{st.session_state.font_color}`
- **플랫폼 버전:** SmartFarm Horticulture v2.7
""")
