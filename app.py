import streamlit as st

# Streamlit 앱의 제목과 설명
st.title('루틴늘리기 앱')
st.write('하나의 루틴을 설정하고 시작을 누르면 1시간 후에 루틴이 완료됩니다.')

# 사용자 입력을 받는 루틴 텍스트 상자
new_routine = st.text_input('새로운 루틴 추가하기')

# 선택된 루틴을 저장할 리스트
existing_routines = st.sidebar.empty()
selected_routines = existing_routines.multiselect('기존 루틴', ['운동하기', '공부하기', '독서하기'])

# 타이머 관련 초기 설정
timer_running = False
timer_seconds = 3600  # 1시간을 초로 설정

# 타이머 함수
def run_timer():
    global timer_running, timer_seconds
    timer_running = True
    while timer_seconds > 0:
        mins, secs = divmod(timer_seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        st.header(timeformat)
        timer_seconds -= 1
        time.sleep(1)
    st.header('루틴 완료!')

# 시작 버튼 처리
start_button = st.button('시작')

if start_button and not timer_running:
    st.write(f'루틴 "{new_routine}" 시작!')
    run_timer()

# 저장된 루틴 업데이트 및 자동 저장
st.sidebar.subheader('저장된 루틴')
if new_routine:
    selected_routines.append(new_routine)

existing_routines.multiselect('기존 루틴', selected_routines)

# 매일 잘하고 있는지 체크리스트
st.subheader('매일 잘하고 있는지 체크리스트')
if st.checkbox('오늘의 루틴을 완료했나요?'):
    st.write('축하합니다! 오늘의 루틴을 완료하셨습니다.')

