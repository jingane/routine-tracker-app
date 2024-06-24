import streamlit as st
from datetime import datetime, timedelta

# Page title and description
st.title('루틴늘리기 앱')
st.write('하나의 루틴을 적고 시작을 누르면 1시간 후에 끝나는 타이머입니다.')

# Sidebar에 있는 루틴 입력 기능
new_routine = st.text_input('새로운 루틴 추가하기')

# 저장된 루틴을 불러오기 위한 리스트
routine_list = st.sidebar.empty()
existing_routines = routine_list.multiselect('기존 루틴', ['운동하기', '공부하기', '독서하기'])

# 타이머
start_time = st.empty()
end_time = st.empty()
progress_bar = st.empty()

start_button = st.button('시작')

if start_button:
    start_time.markdown(f'**시작 시간:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    duration = timedelta(hours=1)
    end_time.markdown(f'**예상 종료 시간:** {datetime.now() + duration}')

    while duration.total_seconds() > 0:
        progress_bar.progress(100 - int((duration.total_seconds() / 3600) * 100))
        duration = duration - timedelta(seconds=1)

    st.write('루틴 완료!')

# 매일 잘하고 있는지 체크리스트
st.subheader('매일 잘하고 있는지 체크리스트')
if st.checkbox('오늘의 루틴을 완료했나요?'):
    st.write('축하합니다! 오늘의 루틴을 완료하셨습니다.')

# 저장된 루틴 업데이트 및 자동 저장
st.sidebar.subheader('저장된 루틴')
if new_routine:
    existing_routines.append(new_routine)

routine_list.multiselect('기존 루틴', existing_routines)

# 앱이 새로고침 되더라도 데이터는 보존되어야 함

