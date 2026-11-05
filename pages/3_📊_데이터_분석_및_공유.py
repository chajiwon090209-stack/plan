import streamlit as st
import pandas as pd
import json
import altair as alt

# ==========================================
# 1. 페이지 기본 설정 및 세션 데이터 바인딩
# - 데이터 분석 및 공유 페이지 타이틀, 아이콘, 와이드 레이아웃 설정
# - 세션에 저장된 진단 로그(plant_logs)를 불러와 데이터프레임 분석용 변수에 할당
# ==========================================
st.set_page_config(page_title="데이터 분석 및 공유", page_icon="📊", layout="wide")

st.title("📊 환경 데이터 분석 및 친구와 기록 공유")

if "plant_logs" not in st.session_state:
    st.session_state.plant_logs = []

logs = st.session_state.plant_logs

tab1, tab2 = st.tabs(["📊 환경 데이터 시각화", "🤝 친구와 기록 공유"])

with tab1:
    # ==========================================
    # 2-1. 누적 진단 데이터프레임 구성 및 샘플 처리
    # - 저장된 데이터가 없는 경우 가상의 샘플 데이터프레임 제공
    # ==========================================
    st.subheader("📈 누적 진단 데이터 시각화 분석")
    if not logs:
        st.info("💡 저장된 데이터가 없어 샘플 시각화를 제공합니다.")
        df = pd.DataFrame([
            {"작물명": "🍅 방울토마토", "토양수분": "적정", "광조건": "양지"},
            {"작물명": "🥬 상추", "토양수분": "과습", "광조건": "반양지"},
            {"작물명": "🍓 딸기", "토양수분": "건조", "광조건": "음지"}
        ])
    else:
        df = pd.DataFrame(logs)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("##### 💧 토양 수분 분포")
        water_counts = df['토양수분'].value_counts().reset_index()
        water_counts.columns = ['토양수분', '건수']
        chart1 = alt.Chart(water_counts).mark_bar(color='#60a5fa', width=35).encode(
            x=alt.X('토양수분:N', sort=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('건수:Q', title='건수')
        ).properties(width=350, height=250)
        st.altair_chart(chart1, use_container_width=True)

    with col2:
        st.markdown("##### ☀️ 광환경 조건 분포")
        light_counts = df['광조건'].value_counts().reset_index()
        light_counts.columns = ['광조건', '건수']
        chart2 = alt.Chart(light_counts).mark_bar(color='#34d399', width=35).encode(
            x=alt.X('광조건:N', sort=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('건수:Q', title='건수')
        ).properties(width=350, height=250)
        st.altair_chart(chart2, use_container_width=True)

with tab2:
    st.subheader("🤝 공동 작업 및 데이터 내보내기/불러오기")
    col_ex, col_im = st.columns(2, gap="large")
    
    with col_ex:
        st.markdown("##### 📤 내 데이터 공유 코드 생성")
        if logs:
            export_str = json.dumps(logs, ensure_ascii=False, indent=2)
            st.text_area("아래 코드를 복사해서 친구에게 전달하세요!", export_str, height=180)
        else:
            st.info("공유할 데이터가 없습니다.")

    with col_im:
        st.markdown("##### 📥 친구의 공유 코드 병합하기")
        import_str = st.text_area("친구의 코드를 여기에 붙여넣으세요", height=180)
        if st.button("🔄 데이터 병합하기", use_container_width=True):
            try:
                friend_data = json.loads(import_str)
                st.session_state.plant_logs.extend(friend_data)
                st.success(f"🎉 성공적으로 {len(friend_data)}건의 데이터를 병합했습니다!")
                st.rerun()
            except:
                st.error("❌ 코드 형식이 올바르지 않습니다.")
