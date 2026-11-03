import streamlit as st

st.set_page_config(page_title="설정 및 테마 변경", page_icon="⚙️", layout="wide")

st.title("⚙️ 앱 설정 및 테마 모드 변경")
st.caption("원하시는 화면 테마와 나만의 포인트 색상을 지정하여 웹앱의 분위기를 꾸며보세요.")

# 세션 상태에 테마 및 커스텀 색상 초기화
if "app_theme" not in st.session_state:
    st.session_state.app_theme = "다크 모드 (기본)"
if "custom_color" not in st.session_state:
    st.session_state.custom_color = "#34d399"  # 기본 스마트팜 그린 색상

with st.container(border=True):
    st.subheader("🎨 화면 테마 및 색상 설정")
    
    # 1. 테마 모드 선택
    theme_choice = st.radio(
        "사용할 테마 모드를 선택하세요:",
        ["다크 모드 (기본)", "라이트 모드 (밝은 화면)", "스마트팜 그린 모드"],
        index=0 if st.session_state.app_theme == "다크 모드 (기본)" else (1 if st.session_state.app_theme == "라이트 모드 (밝은 화면)" else 2)
    )
    
    st.markdown("---")
    
    # 2. 사용자 지정 포인트 색상 선택 (컬러 피커)
    st.markdown("🖌️ **나만의 포인트 색상 지정하기**")
    user_color = st.color_picker("앱 전반에 적용할 포인트 컬러를 선택하세요:", st.session_state.custom_color)
    
    if st.button("✨ 테마 및 색상 적용하기", use_container_width=True):
        st.session_state.app_theme = theme_choice
        st.session_state.custom_color = user_color
        st.success(f"🎉 성공적으로 설정이 적용되었습니다!\n- **선택 테마:** {theme_choice}\n- **포인트 색상:** `{user_color}`")
        st.info("💡 선택하신 커스텀 색상 코드는 세션에 저장되어 시각 요소나 버튼 등에 연동됩니다.")

# 선택된 커스텀 색상을 시각적으로 보여주는 박스 스타일 적용
st.markdown(
    f"""
    <div style="padding: 15px; border-radius: 8px; background-color: {st.session_state.custom_color}; color: #0e1117; font-weight: bold; text-align: center; margin-top: 20px;">
        🎨 현재 적용된 나만의 포인트 색상 미리보기 ({st.session_state.custom_color})
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
- **플랫폼 버전:** SmartFarm Horticulture v2.6
""")
