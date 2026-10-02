import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="생장 관리 일지", page_icon="📋", layout="wide")

st.title("📋 저장된 생장 관리 일지")
st.caption("누적된 작물 생육 환경 기록 및 진단 내역입니다.")

# 세션 상태 초기화
if "plant_logs" not in st.session_state:
    st.session_state.plant_logs = []

st.metric(label="총 누적 기록 건수", value=f"{len(st.session_state.plant_logs)} 건")

if st.session_state.plant_logs:
    df = pd.DataFrame(st.session_state.plant_logs)
    st.dataframe(df, use_container_width=True)
else:
    st.info("아직 저장된 생장 일지가 없습니다. 메인 진단 페이지에서 환경 입력 후 '진단 기록 추가' 버튼을 눌러보세요!")
