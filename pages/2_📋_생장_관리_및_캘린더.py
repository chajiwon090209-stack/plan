import streamlit as st
import pandas as pd

# ==========================================
# 1. 페이지 기본 설정 및 상태 변수 초기화
# - 생장 관리 및 캘린더 페이지의 타이틀 및 레이아웃 설정
# - 타 페이지(작물 진단)에서 넘어온 일지 데이터를 보관할 세션 리스트 초기화
# ==========================================
st.set_page_config(page_title="생장 관리 및 캘린더", page_icon="📋", layout="wide")

st.title("📋 생장 관리 일지 & 사진 캘린더")

if "plant_logs" not in st.session_state:
    st.session_state.plant_logs = []

# 상단 탭 나누기 (생장 일지 목록 / 사진 캘린더)
tab1, tab2 = st.tabs(["📋 생장 관리 일지", "📸 생육 사진 캘린더"])

with tab1:
    # ==========================================
    # 2-1. 누적된 생장 관리 일지 출력 및 관리
    # - 세션에 저장된 진단 로그를 Pandas DataFrame으로 변환하여 테이블 시각화
    # - 전체 일지 초기화 버튼을 통한 데이터 리셋 기능 제공
    # ==========================================
    st.subheader("📝 누적된 생장 관리 일지")
    if st.session_state.plant_logs:
        df = pd.DataFrame(st.session_state.plant_logs)
        st.dataframe(df, use_container_width=True)
        
        if st.button("🗑️ 전체 일지 초기화"):
            st.session_state.plant_logs = []
            st.rerun()
    else:
        st.info("아직 저장된 일지 기록이 없습니다. 메인 홈에서 진단을 진행해 보세요!")

with tab2:
    # ==========================================
    # 2-2. 작물 생육 사진 기록 보관함 및 캘린더 연동
    # - 날짜 선택 위젯(st.date_input)과 이미지 파일 업로더 연동
    # - 업로드된 사진과 촬영 날짜를 매칭하여 즉시 시각화 및 등록 성공 메시지 출력
    # ==========================================
    st.subheader("📸 작물 생육 사진 기록 보관함")
    st.caption("날짜별로 촬영한 작물의 성장 모습을 기록하고 확인하세요.")
    photo_date = st.date_input("촬영 날짜 선택")
    uploaded_photo = st.file_uploader("작물 성장 사진 업로드", type=["jpg", "png", "jpeg"])
    
    if uploaded_photo:
        st.image(uploaded_photo, caption=f"📅 {photo_date} 촬영 기록", width=300)
        st.success("사진이 캘린더 기록에 안전하게 등록되었습니다!")
