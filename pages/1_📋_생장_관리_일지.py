import streamlit as st
import pandas as pd

st.set_page_config(page_title="생장 관리 일지", page_icon="📋", layout="wide")

st.title("📋 저장된 생장 관리 일지")
st.caption("누적된 작물 생육 환경 기록 및 진단 내역입니다.")

# 세션 상태 초기화
if "plant_logs" not in st.session_state:
    st.session_state.plant_logs = []

logs = st.session_state.plant_logs

# 💡 기록이 없을 때 보여줄 샘플(더미) 데이터 정의
if not logs:
    st.info("💡 **[미리보기 모드]** 아직 직접 저장된 일지가 없어, 이해를 돕기 위한 **샘플 데이터(Dummy Data)** 예시를 보여드립니다. 메인 진단 페이지에서 일지를 추가하면 실제 데이터로 전환됩니다!")
    
    sample_df = pd.DataFrame([
        {"작물명": "🍅 방울토마토", "현재온도": "22°C", "토양수분": "적정", "생장단계": "영양생장기", "광조건": "양지(강한 직사광선)", "진단결과": "적정"},
        {"작물명": "🥬 상추", "현재온도": "26°C", "토양수분": "과습", "생장단계": "개화/수분기", "광조건": "반양지", "진단결과": "고온 경고"},
        {"작물명": "🍓 딸기", "현재온도": "16°C", "토양수분": "건조", "생장단계": "발아/유묘기", "광조건": "음지", "진단결과": "저온 경고"}
    ])
    
    st.markdown("### 총 누적 기록 건수 (예시)")
    st.markdown("### **3 건 (미리보기)**")
    st.markdown("---")
    st.subheader("📋 [미리보기] 생장 관리 일지 예시 테이블")
    st.dataframe(sample_df, use_container_width=True)

else:
    df = pd.DataFrame(logs)
    st.markdown(f"### 총 누적 기록 건수")
    st.markdown(f"### **{len(df)} 건**")
    st.markdown("---")
    
    st.subheader("📋 전체 누적 데이터 원본")
    st.dataframe(df, use_container_width=True)
    
    if st.button("🗑️ 전체 일지 기록 초기화"):
        st.session_state.plant_logs = []
        st.success("모든 일지 기록이 초기화되었습니다.")
        st.rerun()
