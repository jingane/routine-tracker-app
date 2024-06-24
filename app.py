import streamlit as st
from datetime import datetime, timedelta

# 루틴 기록 및 체크리스트를 위한 데이터 초기화
if 'routines' not in st.session_state:
    st.session_state.routines = []

if 'checklist' not in st.session_state:
    st.session_state.checklist = []

# 새로운 루틴 입력
routine = st.text_input('새 루틴을 입력하세요:')

if st.button('시작'):
    end_time = datetime.now() + timedelta(hours=1)
    st.session_state.routines.append({'routine': routine, 'end_time': end_time})

# 진행 중인 루틴 표시
st.write("진행 중인 루틴:")
for r in st.session_state.routines:
    remaining_time = r['end_time'] - datetime.now()
    if remaining_time.total_seconds() > 0:
        st.write(f"{r['routine']} - 남은 시간: {remaining_time}")
    else:
        st.write(f"{r['routine']} - 완료")
        if r['routine'] not in st.session_state.checklist:
            st.session_state.checklist.append(r['routine'])

# 완료된 루틴 표시
st.write("완료된 루틴:")
for r in st.session_state.routines:
    if r['end_time'] <= datetime.now():
        st.write(f"{r['routine']} - 완료")

# 체크리스트 표시
st.write("체크리스트:")
for item in st.session_state.checklist:
    st.write(f"- {item}")

# 새로운 루틴 추가 입력
new_routine = st.text_input('새로운 루틴을 추가하세요:', key='new_routine')

if st.button('추가'):
    if new_routine and new_routine not in st.session_state.checklist:
        st.session_state.checklist.append(new_routine)

