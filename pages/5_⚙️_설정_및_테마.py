import streamlit as st

# ==========================================
# 1. 설정 페이지 기본 설정 및 테마 세션 초기화
# - 설정 페이지의 타이틀, 아이콘, 와이드 레이아웃 설정
# - 앱 테마 모드, 포인트 색상, 폰트 색상을 유지하기 위한 세션 상태 기본값 정의
# ==========================================
st.set_page_config(page_title="설정 및 테마 변경", page_icon="⚙️", layout="wide")

st.title("⚙️ 앱 설정 및 테마 모드 변경")
st.caption("원하시는 화면 테마와 나만의 포인트 색상, 그리고 폰트 색상을 지정하여 웹앱의 분위기를 꾸며보세요.")

# 세션 상태에 테마, 포인트 색상, 폰트 색상 초기화
if "app_theme" not in st.session_state:
    st.session_state.app_theme = "다크 모드 (기본)"
if "custom_color" not in st.session_state:
    st.session_state.custom_color = "#34d399"  # 기본 스마트팜 그린 색상
if "font_color" not in st.session_state:
    st.session_state.font_color = "#ffffff"  # 기본 흰색 폰트

with st.container(border=True):
    st.subheader("🎨 화면 테마 및 색상 세부 설정")
    
   # ==========================================
    # 2-1. 화면 테마 모드 선택 라디오 버튼
    # - 다크 모드, 라이트 모드, 스마트팜 그린 모드 중 사용자가 원하는 테마 선택
    # ==========================================
    theme_choice = st.radio(
        "사용할 테마 모드를 선택하세요:",
        ["다크 모드 (기본)", "라이트 모드 (밝은 화면)", "스마트팜 그린 모드"],
        index=0 if st.session_state.app_theme == "다크 모드 (기본)" else (1 if st.session_state.app_theme == "라이트 모드 (밝은 화면)" else 2)
    )
    
    st.markdown("---")
    
    # 2. 컬러 피커 2개 배치 (포인트 색상 / 폰트 색상)
    col_c1, col_c2 = st.columns(2, gap="large")
    
    with col_c1:
        st.markdown("🖌️ **나만의 포인트 색상**")
        user_color = st.color_picker("포인트 컬러 선택:", st.session_state.custom_color, key="picker_point")
        
    with col_c2:
        st.markdown("✍️ **나만의 폰트(글자) 색상**")
        user_font_color = st.color_picker("폰트 컬러 선택:", st.session_state.font_color, key="picker_font")
    
    st.markdown("")
    if st.button("✨ 테마 및 색상 적용하기", use_container_width=True):
        st.session_state.app_theme = theme_choice
        st.session_state.custom_color = user_color
        st.session_state.font_color = user_font_color
        st.success(f"🎉 성공적으로 설정이 적용되었습니다!\n- **선택 테마:** {theme_choice}\n- **포인트 색상:** `{user_color}`\n- **폰트 색상:** `{user_font_color}`")

# 선택된 커스텀 색상 및 폰트 색상을 시각적으로 보여주는 미리보기 박스
st.markdown(
    f"""
    <div style="padding: 20px; border-radius: 10px; background-color: {st.session_state.custom_color}; color: {st.session_state.font_color}; font-weight: bold; text-align: center; margin-top: 20px; font-size: 16px;">
        ✨ 폰트 및 포인트 색상 미리보기 (글자색: {st.session_state.font_color} / 배경색: {st.session_state.custom_color})
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
st.subheader("👤 현재 계정 및 시스템 정보")
current_user = st.session_state.get("username", "비로그인 사용자")
st.markdown(f"""
- **현재 접속 계정:** `{current_user}`
- **현재 적용된 테마:** `{st.session_state.app_theme}`
- **커스텀 포인트 색상:** `{st.session_state.custom_color}`
- **커스텀 폰트 색상:** `{st.session_state.font_color}`
- **플랫폼 버전:** SmartFarm Horticulture v2.7
""")
