import streamlit as st

st.set_page_config(page_title="설정 및 테마 변경", page_icon="⚙️", layout="wide")

st.title("⚙️ 앱 설정 및 테마 모드 변경")
st.caption("원하시는 화면 테마를 선택하여 웹앱의 분위기를 바꿔보세요.")

# 세션 상태에 테마 정보 초기화
if "app_theme" not in st.session_state:
    st.session_state.app_theme = "다크 모드 (기본)"

with st.container(border=True):
    st.subheader("🎨 화면 테마 설정")
    
    theme_choice = st.radio(
        "사용할 테마 모드를 선택하세요:",
        ["다크 모드 (기본)", "라이트 모드 (밝은 화면)", "스마트팜 그린 모드"],
        index=0 if st.session_state.app_theme == "다크 모드 (기본)" else (1 if st.session_state.app_theme == "라이트 모드 (밝은 화면)" else 2)
    )
    
    if st.button("✨ 테마 적용하기", use_container_width=True):
        st.session_state.app_theme = theme_choice
        st.success(f"🎉 성공적으로 **[{theme_choice}]**(이)가 설정되었습니다!")
        st.info("💡 Streamlit 기본 설정 외에 커스텀 CSS 스타일을 연동하여 분위기를 전환할 수 있습니다.")

st.markdown("---")
st.subheader("👤 현재 계정 및 시스템 정보")
current_user = st.session_state.get("username", "비로그인 사용자")
st.markdown(f"""
- **현재 접속 계정:** `{current_user}`
- **현재 적용된 테마:** `{st.session_state.app_theme}`
- **플랫폼 버전:** SmartFarm Horticulture v2.5
""")
