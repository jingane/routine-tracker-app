import streamlit as st
from datetime import datetime, timedelta

# 루틴 기록을 위한 리스트
if 'routines' not in st.session_state:
    st.session_state.routines = []

# 루틴 입력
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

# 완료된 루틴 표시
st.write("완료된 루틴:")
for r in st.session_state.routines:
    if r['end_time'] <= datetime.now():
        st.write(f"{r['routine']} - 완료")

# 새로운 루틴 입력
st.text_input('새로운 루틴을 추가하세요:', key='new_routine')
