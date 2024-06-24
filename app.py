import streamlit as st
import time

def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        st.header(timeformat)
        time.sleep(1)
        seconds -= 1
    st.write('루틴 완료!')

st.title('루틴늘리기 앱')

routine = st.text_input('하나의 루틴을 적어주세요.')

if st.button('시작'):
    st.write(f'루틴 "{routine}" 시작!')
    countdown_timer(3600)  # 1 hour countdown

st.sidebar.subheader('저장된 루틴')
# 예시 루틴 목록
existing_routines = ['운동하기', '공부하기', '독서하기']
selected_routines = st.sidebar.multiselect('기존 루틴', existing_routines)

# 새로운 루틴 추가
new_routine = st.sidebar.text_input('새로운 루틴 추가하기')

if new_routine:
    existing_routines.append(new_routine)

# 선택된 루틴 표시
st.sidebar.write('선택된 루틴:')
for routine in selected_routines:
    st.sidebar.write(f'- {routine}')
