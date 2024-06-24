import streamlit as st
from datetime import datetime, timedelta
import time

# 파일 이름
ROUTINES_FILE = 'routines.txt'
CHECKLIST_FILE = 'checklist.txt'

# 데이터 초기화 및 로드
def load_data(file_name):
    try:
        with open(file_name, 'r') as f:
            data = f.read().splitlines()
        return data
    except FileNotFoundError:
        return []

def save_data(data, file_name):
    with open(file_name, 'w') as f:
        for item in data:
            f.write(f"{item}\n")

# 초기 데이터 로드
if 'routines' not in st.session_state:
    st.session_state.routines = load_data(ROUTINES_FILE)

if 'checklist' not in st.session_state:
    st.session_state.checklist = load_data(CHECKLIST_FILE)

# 루틴 추가 입력
new_routine = st.text_input('새로운 루틴을 추가하세요:', key='new_routine')

if st.button('추가'):
    if new_routine and new_routine not in st.session_state.checklist:
        st.session_state.checklist.append(new_routine)
        save_data(st.session_state.checklist, CHECKLIST_FILE)
        st.success(f"'{new_routine}' 루틴이 체크리스트에 추가되었습니다!")
    elif new_routine in st.session_state.checklist:
        st.warning("이미 체크리스트에 있는 루틴입니다.")
    else:
        st.warning("루틴을 입력하세요.")

# 루틴 표시
st.write("## 체크리스트:")
for item in st.session_state.checklist:
    st.write(f"- {item}")

# 카운트다운 타이머 표시
st.write("## 카운트다운 타이머:")
start_time = st.session_state.get('start_time', None)
if st.button('타이머 시작'):
    start_time = datetime.now()
    st.session_state.start_time = start_time

if start_time:
    elapsed_time = datetime.now() - start_time
    remaining_time = timedelta(hours=1) - elapsed_time
    if remaining_time.total_seconds() <= 0:
        st.warning("타이머가 완료되었습니다!")
    else:
        st.write(f"남은 시간: {remaining_time}")
        time.sleep(1)  # 1초마다 업데이트
