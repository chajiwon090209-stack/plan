import streamlit as st
from datetime import date

st.title("📸 날짜별 생육 사진 캘린더 & 기록")
st.caption("날짜별로 작물 사진을 업로드하고 생장 변화를 타임라인 형태로 기록·확인하세요.")

# 작물별 대표 이모티콘 매핑 함수
def get_crop_emoji(name):
    name_clean = name.strip()
    emoji_dict = {
        "토마토": "🍅", "방울토마토": "🍅",
        "상추": "🥬", "배추": "🥬", "시금치": "🥬",
        "딸기": "🍓",
        "포도": "🍇", "샤인머스캣": "🍇", "샤인머스켓": "🍇",
        "파프리카": "🫑", "피망": "🫑", "고추": "🌶️",
        "당근": "🥕", "옥수수": "🌽", "오이": "🥒", "가지": "🍆",
        "사과": "🍎", "복숭아": "🍑", "바나나": "🍌", "레몬": "🍋",
        "바질": "🌿", "허브": "🌿"
    }
    for crop_key, emoji in emoji_dict.items():
        if crop_key in name_clean:
            return emoji
    return "🌱"  # 목록에 없는 작물은 기본 싹 이모티콘 지정

# 세션 상태 초기화
if "photo_logs" not in st.session_state:
    st.session_state.photo_logs = []

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📅 일지 작성 및 사진 업로드")
    
    log_date = st.date_input("기록 날짜 선택", value=date.today())
    plant_name = st.text_input("작물 이름", value="방울토마토")
    uploaded_file = st.file_uploader("작물 생육 사진 업로드 (JPG, PNG)", type=["jpg", "jpeg", "png"])
    memo = st.text_area("오늘의 생육 관찰 메모", placeholder="예: 본잎이 2장 더 자랐고, 토양 수분이 적당함.")
    
    if st.button("💾 캘린더에 사진 일지 저장"):
        if uploaded_file is not None:
            # 이모티콘 자동 추출
            emoji = get_crop_emoji(plant_name)
            
            st.session_state.photo_logs.append({
                "날짜": str(log_date),
                "작물명": plant_name,
                "이모티콘": emoji,
                "이미지": uploaded_file,
                "메모": memo
            })
            st.success(f"✅ {emoji} {plant_name} 일지가 캘린더에 저장되었습니다!")
        else:
            st.warning("⚠️ 기록할 작물 사진을 업로드해 주세요!")

with col2:
    st.subheader("📆 날짜별 생육 타임라인 모음")
    
    if st.session_state.photo_logs:
        sorted_logs = sorted(st.session_state.photo_logs, key=lambda x: x["날짜"], reverse=True)
        
        for idx, log in enumerate(sorted_logs):
            emoji = log.get("이모티콘", "🌱")
            with st.expander(f"{emoji} [{log['날짜']}] {log['작물명']} 관찰 기록", expanded=(idx == 0)):
                st.image(log["이미지"], caption=f"촬영일: {log['날짜']} / 작물: {emoji} {log['작물명']}", use_column_width=True)
                st.write(f"**📝 관찰 메모:** {log['메모']}")
    else:
        st.info("아직 등록된 사진 일지가 없습니다. 왼쪽 화면에서 사진과 기록을 남겨보세요!")
