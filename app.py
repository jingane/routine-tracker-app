import streamlit as st
from datetime import datetime, timedelta
import json

# 데이터를 파일에 저장할 경로
DATA_FILE = 'routines.json'

# 페이지 제목 및 설명을 HTML과 CSS로 스타일링
st.markdown("""
    <style>
    .title {
        font-size: 28px;
        font-weight: bold;
        color: #4CAF50;
    }
    .subtitle {
        font-size: 16px;
        color: #555;
    }
    </style>
    <h1 class="title">나만의 루틴 만들기</h1>
    <p class="subtitle">하루 1시간 루틴을 만들어 내 빈 시간을 꽉 채워볼까요~</p>
""", unsafe_allow_html=True)

# 데이터 로드 함수
def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# 데이터 저장 함수
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 루틴 기록을 위한 데이터 초기화 및 로드
if 'routines' not in st.session_state:
    st.session_state.routines = load_data()

# 새로운 루틴 입력
routine = st.text_input('새 루틴을 입력하세요:')

if st.button('시작'):
    if routine and routine not in [r['routine'] for r in st.session_state.routines]:
        end_time = datetime.now() + timedelta(hours=1)
        st.session_state.routines.append({'routine': routine, 'end_time': end_time})
        st.success(f"'{routine}' 루틴이 시작되었습니다!")
        save_data(st.session_state.routines)  # 데이터 저장
    elif routine in [r['routine'] for r in st.session_state.routines]:
        st.warning("이미 진행 중인 루틴입니다.")
    else:
        st.warning("루틴을 입력하세요.")

# 진행 중인 루틴 표시 및 관리
st.write("## 진행 중인 루틴:")
current_time = datetime.now()
for r in st.session_state.routines:
    remaining_time = r['end_time'] - current_time
    if remaining_time.total_seconds() > 0:
        st.write(f"{r['routine']} - 남은 시간: {str(remaining_time).split('.')[0]}")
    else:
        st.write(f"{r['routine']} - 완료")
        st.session_state.routines.remove(r)
        save_data(st.session_state.routines)  # 데이터 저장

# 새로운 날에 다시 시작할 수 있는 버튼 추가
st.write("## 다시 시작 가능한 루틴:")
for r in st.session_state.routines:
    if r['end_time'] <= current_time:
        if st.button(f"{r['routine']} 다시 시작"):
            end_time = datetime.now() + timedelta(hours=1)
            st.session_state.routines.append({'routine': r['routine'], 'end_time': end_time})
            st.success(f"'{r['routine']}' 루틴이 다시 시작되었습니다!")
            save_data(st.session_state.routines)  # 데이터 저장
            st.experimental_rerun()

# 루틴 타이머 업데이트 (이 부분은 실시간 타이머를 표시하는 부분이므로 파일 저장과는 직접적인 관련이 없습니다)
