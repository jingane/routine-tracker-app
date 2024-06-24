import streamlit as st
import json
import time
from datetime import datetime, timedelta

# 데이터 로드
def load_data():
    try:
        with open('routines.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# 데이터 저장
def save_data(data):
    with open('routines.json', 'w') as file:
        json.dump(data, file)

# 시간 포맷 변환
def format_time(seconds):
    return str(timedelta(seconds=seconds))

st.title("루틴 늘리기 앱")

# 세션 상태 초기화
if "routines" not in st.session_state:
    st.session_state.routines = load_data()

# 루틴 입력 섹션
new_routine = st.text_input("새 루틴 추가")
if st.button("루틴 시작"):
    if new_routine:
        st.session_state.routines.append({"name": new_routine, "start_time": datetime.now().isoformat(), "completed": False})
        save_data(st.session_state.routines)
        st.experimental_rerun()

# 루틴 리스트
st.header("현재 루틴")
for routine in st.session_state.routines:
    start_time = datetime.fromisoformat(routine["start_time"])
    time_elapsed = (datetime.now() - start_time).total_seconds()
    time_remaining = max(0, 3600 - time_elapsed)

    if time_remaining > 0:
        st.write(f"루틴: {routine['name']}")
        timer_placeholder = st.empty()

        # 타이머 업데이트
        while time_remaining > 0:
            time_remaining = max(0, 3600 - (datetime.now() - start_time).total_seconds())
            timer_placeholder.text(f"남은 시간: {format_time(int(time_remaining))}")
            time.sleep(1)
    else:
        routine["completed"] = True

# 완료된 루틴
st.header("완료된 루틴")
for routine in st.session_state.routines:
    if routine["completed"]:
        st.write(f"루틴: {routine['name']} 완료")

# 데이터 저장
save_data(st.session_state.routines)
