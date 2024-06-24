import streamlit as st
from datetime import datetime, timedelta
import time

# 루틴 기록 및 체크리스트를 위한 데이터 초기화
if 'routines' not in st.session_state:
    st.session_state.routines = []

if 'checklist' not in st.session_state:
    st.session_state.checklist = []

# 새로운 루틴 입력
routine = st.text_input('새 루틴을 입력하세요:')

if st.button('시작'):
    if routine and routine not in [r['routine'] for r in st.session_state.routines]:
        end_time = datetime.now() + timedelta(hours=1)
        st.session_state.routines.append({'routine': routine, 'end_time': end_time})
        st.success(f"'{routine}' 루틴이 시작되었습니다!")
    elif routine in [r['routine'] for r in st.session_state.routines]:
        st.warning("이미 진행 중인 루틴입니다.")
    else:
        st.warning("루틴을 입력하세요.")

# 진행 중인 루틴 표시
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

# 새로운 날에 다시 시작할 수 있는 버튼 추가
st.write("## 다시 시작 가능한 루틴:")
for r in st.session_state.routines:
    if r['end_time'] <= current_time:
        if st.button(f"{r['routine']} 다시 시작"):
            end_time = datetime.now() + timedelta(hours=1)
            st.session_state.routines.append({'routine': r['routine'], 'end_time': end_time})
            st.success(f"'{r['routine']}' 루틴이 다시 시작되었습니다!")
            st.experimental_rerun()

# 체크리스트 표시
st.write("## 체크리스트:")
for item in st.session_state.checklist:
    st.write(f"- {item}")

# 루틴 타이머 업데이트
for r in st.session_state.routines:
    if r['end_time'] > current_time:
        timer_placeholder = st.empty()
        while datetime.now() < r['end_time']:
            remaining_time = r['end_time'] - datetime.now()
            timer_placeholder.write(f"{r['routine']} - 남은 시간: {str(remaining_time).split('.')[0]}")
            time.sleep(1)
        timer_placeholder.write(f"{r['routine']} - 완료")
        if r['routine'] not in st.session_state.checklist:
            st.session_state.checklist.append(r['routine'])
