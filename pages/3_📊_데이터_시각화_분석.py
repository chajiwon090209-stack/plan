import streamlit as st
import pandas as pd

st.set_page_config(page_title="데이터 시각화 분석", page_icon="📊", layout="wide")

st.title("📊 원예 환경 및 생장 데이터 시각화 분석")
st.caption("누적된 생장 진단 데이터를 바탕으로 온도 분포 및 환경 조건을 시각적 차트로 분석합니다.")

# 세션 상태에 누적된 데이터 확인
if "plant_logs" not in st.session_state:
    st.session_state.plant_logs = []

logs = st.session_state.plant_logs

if logs:
    df = pd.DataFrame(logs)
    
    # 상단 요약 지표
    col1, col2, col3 = st.columns(3)
    col1.metric("총 진단 및 관리 건수", f"{len(df)} 건")
    col2.metric("등록된 작물 종류", f"{df['작물명'].nunique()} 개")
    col3.metric("주요 생장 단계", df['생장단계'].mode()[0] if not df.empty else "-")
    
    st.markdown("---")
    
    # 1. 토양 수분 상태별 비율 (파이 차트 또는 바 차트 대체용)
    st.subheader("💧 토양 수분 상태 분포")
    water_counts = df['토양수분'].value_counts()
    st.bar_chart(water_counts)
    
    # 2. 광 조건별 분포
    st.subheader("☀️ 광환경(조도) 조건 분포")
    light_counts = df['광조건'].value_counts()
    st.bar_chart(light_counts)
    
    # 3. 전체 데이터 테이블 확인
    st.subheader("📋 전체 누적 데이터 원본")
    st.dataframe(df, use_container_width=True)

else:
    st.info("⚠️ 아직 누적된 진단 데이터가 없습니다. 메인 페이지(생장 환경 진단)에서 작물 환경을 진단하고 '생장 일지에 추가' 버튼을 눌러 데이터를 쌓아보세요!")
