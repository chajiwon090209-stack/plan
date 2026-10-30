import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="공동 작업 및 기록 공유", page_icon="🤝", layout="wide")

st.title("🤝 친구와 생장 일지 & 기록 공유")
st.caption("내 작물 생장 일지 데이터를 공유 코드로 내보내거나, 친구의 공유 코드를 입력해 데이터를 함께 확인해보세요!")

# 세션 상태 초기화
if "plant_logs" not in st.session_state:
    st.session_state.plant_logs = []

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📤 내 일지 데이터 공유하기")
    st.write("현재 저장된 생장 관리 일지를 공유할 수 있는 텍스트 코드로 변환합니다.")
    
    if st.session_state.plant_logs:
        # 현재 일지 데이터를 JSON 문자열로 변환
        export_data = json.dumps(st.session_state.plant_logs, ensure_ascii=False, indent=2)
        
        st.text_area("아래 코드를 복사해서 친구에게 전달하세요!", export_data, height=200)
        st.success(f"총 {len(st.session_state.plant_logs)}건의 데이터가 공유 준비되었습니다.")
    else:
        st.info("💡 공유할 생장 일지 데이터가 아직 없습니다. 메인 진단 페이지에서 일지를 먼저 추가해 보세요!")

with col2:
    st.subheader("📥 친구의 공유 코드 불러오기")
    st.write("친구에게 전달받은 공유 코드를 아래 칸에 붙여넣고 불러오기 버튼을 누르세요.")
    
    import_input = st.text_area("여기에 친구의 공유 코드를 입력하세요", height=200, placeholder="[...데이터 붙여넣기...]")
    
    if st.button("🔄 공유 데이터 병합 및 불러오기", use_container_width=True):
        if import_input.strip():
            try:
                imported_logs = json.loads(import_input)
                if isinstance(imported_logs, list):
                    # 기존 데이터에 친구 데이터 합치기
                    st.session_state.plant_logs.extend(imported_logs)
                    st.success(f"🎉 성공적으로 {len(imported_logs)}건의 데이터를 불러와 병합했습니다!")
                    st.rerun()
                else:
                    st.error("❌ 올바르지 않은 데이터 형식입니다. 올바른 공유 코드를 입력해 주세요.")
            except Exception as e:
                st.error("❌ 코드 파싱 중 오류가 발생했습니다. 코드를 다시 확인해 주세요.")
        else:
            st.warning("⚠️ 입력된 공유 코드가 없습니다.")

st.markdown("---")
st.subheader("📋 현재 내 앱에 누적된 전체 데이터 미리보기")
if st.session_state.plant_logs:
    st.dataframe(pd.DataFrame(st.session_state.plant_logs), use_container_width=True)
else:
    st.info("현재 저장된 데이터가 비어 있습니다.")
