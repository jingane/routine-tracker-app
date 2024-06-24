import streamlit as st
from datetime import datetime, timedelta
import time

# Streamlit session state 초기화
if 'routines' not in st.session_state:
    st.session_state.routines = []

if 'checklist' not in st.session_state:
    st.session_state.checklist = []

# 새로운 루틴 입력 폼
new_routine = st.text_input('새로운 루틴을 입력하세요:', key='new_routine')

if st.button('추가'):
    if new_routine:
        # 이미 추가된 루틴인지 확인
        if new_routine not in [r['routine'] for r in st.session_state.routines]:
            end_time = datetime.now() + timedelta(hours=1)
            st.session_state.routines.append({'routine': new_routine, 'end_time': end_time})
            st.success(f"'{new_routine}' 루틴이 추가되었습니다!")
        else:
            st.warning("이미 추가된 루틴입니다.")
    else:
        st.warning("루틴을 입력하세요.")

# 화면 업데이트 함수
def update_routine_status():
    st.write("## 루틴 상태:")
    for r in st.session_state.routines:
        remaining_time = r['end_time'] - datetime.now()
        if remaining_time.total_seconds() > 0:
            st.write(f"{r['routine']} - 남은 시간: {str(remaining_time).split('.')[0]}")
        else:
            st.write(f"{r['routine']} - 완료")
            if r['routine'] not in st.session_state.checklist:
                st.session_state.checklist.append(r['routine'])

# 1초마다 화면 업데이트
while True:
    update_routine_status()
    time.sleep(1)
    st.experimental_rerun()

# 진행 중인 루틴 표시
st.write("## 진행 중인 루틴:")
for r in st.session_state.routines:
    remaining_time = r['end_time'] - datetime.now()
    if remaining_time.total_seconds() > 0:
        st.write(f"{r['routine']} - 남은 시간: {str(remaining_time).split('.')[0]}")
    else:
        st.write(f"{r['routine']} - 완료")
        if r['routine'] not in st.session_state.checklist:
            st.session_state.checklist.append(r['routine'])

# 완료된 루틴 표시
st.write("## 완료된 루틴:")
for r in st.session_state.routines:
    if r['end_time'] <= datetime.now():
        st.write(f"{r['routine']} - 완료")

# 체크리스트 표시
st.write("## 체크리스트:")
for item in st.session_state.checklist:
    st.write(f"- {item}")
