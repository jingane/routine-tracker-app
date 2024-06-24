import streamlit as st
from datetime import datetime, timedelta
import time

# Initialize routines and checklist in session state if not already present
if 'routines' not in st.session_state:
    st.session_state.routines = []

if 'checklist' not in st.session_state:
    st.session_state.checklist = []

# Function to restart a routine
def restart_routine(routine):
    end_time = datetime.now() + timedelta(hours=1)
    st.session_state.routines.append({'routine': routine, 'end_time': end_time})
    st.success(f"'{routine}' 루틴이 다시 시작되었습니다!")

# Displaying current routines
st.write("## 진행 중인 루틴:")
current_time = datetime.now()
for r in st.session_state.routines:
    remaining_time = r['end_time'] - current_time
    if remaining_time.total_seconds() > 0:
        st.write(f"{r['routine']} - 남은 시간: {str(remaining_time).split('.')[0]}")
    else:
        st.write(f"{r['routine']} - 완료")
        if r['routine'] not in st.session_state.checklist:
            st.session_state.checklist.append(r['routine'])

# Button to restart completed routines
st.write("## 다시 시작 가능한 루틴:")
for r in st.session_state.routines:
    if r['end_time'] <= current_time:
        if st.button(f"{r['routine']} 다시 시작"):
            restart_routine(r['routine'])
            st.experimental_rerun()

# Add new routine
new_routine = st.text_input('새로운 루틴을 추가하세요:', key='new_routine')

if st.button('추가'):
    if new_routine and new_routine not in st.session_state.checklist:
        st.session_state.checklist.append(new_routine)
        st.success(f"'{new_routine}' 루틴이 체크리스트에 추가되었습니다!")
    elif new_routine in st.session_state.checklist:
        st.warning("이미 체크리스트에 있는 루틴입니다.")
    else:
        st.warning("루틴을 입력하세요.")

# Routine timer update
for r in st.session_state.routines:
    if r['end_time'] > current_time:
        while datetime.now() < r['end_time']:
            remaining_time = r['end_time'] - datetime.now()
            st.write(f"{r['routine']} - 남은 시간: {str(remaining_time).split('.')[0]}")
            time.sleep(1)
        st.write(f"{r['routine']} - 완료")
        if r['routine'] not in st.session_state.checklist:
            st.session_state.checklist.append(r['routine'])
