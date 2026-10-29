import streamlit as st
import pandas as pd

st.set_page_config(page_title="데이터 시각화 분석", page_icon="📊", layout="wide")

st.title("📊 원예 환경 및 생장 데이터 시각화 분석")
st.caption("누적된 생장 진단 데이터를 바탕으로 온도 분포 및 환경 조건을 시각적 차트로 분석합니다.")

# 세션 상태 초기화
if "plant_logs" not in st.session_state:
    st.session_state.plant_logs = []

# 실제 누적 데이터 가져오기
logs = st.session_state.plant_logs

# 💡 데이터가 없을 때 보여줄 샘플(더미) 데이터 정의
if not logs:
    st.info("💡 **[미리보기 모드]** 아직 직접 쌓인 진단 데이터가 없어, 이해를 돕기 위한 **샘플 데이터(Dummy Data)**로 시각화 미리보기를 제공합니다. 메인 페이지에서 일지를 추가하면 실제 데이터로 바뀝니다!")
    
    sample_df = pd.DataFrame([
        {"작물명": "🍅 방울토마토", "현재온도": "22°C", "토양수분": "적정", "생장단계": "영양생장기", "광조건": "양지(강한 직사광선)", "진단결과": "적정"},
        {"작물명": "🥬 상추", "현재온도": "26°C", "토양수분": "과습", "생장단계": "개화/수분기", "광조건": "반양지", "진단결과": "고온 경고"},
        {"작물명": "🍓 딸기", "현재온도": "16°C", "토양수분": "건조", "생장단계": "발아/유묘기", "광조건": "음지", "진단결과": "저온 경고"},
        {"작물명": "🍇 샤인머스캣", "현재온도": "24°C", "토양수분": "적정", "생장단계": "결실/수확기", "광조건": "LED 인공광", "진단결과": "적정"},
        {"작물명": "🍅 방울토마토", "현재온도": "20°C", "토양수분": "적정", "생장단계": "영양생장기", "광조건": "양지(강한 직사광선)", "진단결과": "적정"}
    ])
    df = sample_df
    is_sample = True
else:
    df = pd.DataFrame(logs)
    is_sample = False

# 상단 요약 지표
col1, col2, col3 = st.columns(3)
col1.metric("총 진단 및 관리 건수", f"{len(df)} 건")
col2.metric("등록된 작물 종류", f"{df['작물명'].nunique()} 개")
col3.metric("주요 생장 단계", df['생장단계'].mode()[0] if not df.empty else "-")

st.markdown("---")

# 1. 토양 수분 상태별 분포 차트
st.subheader("💧 토양 수분 상태 분포")
water_counts = df['토양수분'].value_counts()
st.bar_chart(water_counts)

# 2. 광 조건별 분포 차트
st.subheader("☀️ 광환경(조도) 조건 분포")
light_counts = df['광조건'].value_counts()
st.bar_chart(light_counts)

# 3. 데이터 테이블 확인
if is_sample:
    st.subheader("📋 [미리보기] 샘플 데이터 원본 테이블")
else:
    st.subheader("📋 전체 누적 데이터 원본")

st.dataframe(df, use_container_width=True)
