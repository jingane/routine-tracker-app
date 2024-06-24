import streamlit as st
from datetime import datetime, timedelta

# 초기 데이터 초기화 (루틴 리스트)
if 'routines' not in st.session_state:
    st.session_state.routines = []

# 현재 시간과 종료 시간 계산 함수
def calculate_end_time(start_time):
    start_datetime = datetime.strptime(start_time, '%H:%M:%S')
    end_datetime = start_datetime + timedelta(hours=1)
    return end_datetime.strftime('%H:%M:%S')

# Streamlit 앱 시작
def main():
    st.title('루틴늘리기 앱')

    # 루틴 추가 섹션
    st.header('새로운 루틴 추가')
    new_routine = st.text_input('새로운 루틴을 입력하세요:')
    if st.button('추가하기'):
        st.session_state.routines.append(new_routine)

    # 현재 루틴 리스트 보기
    st.header('현재 루틴 리스트')
    for i, routine in enumerate(st.session_state.routines, start=1):
        st.write(f'{i}. {routine}')

    # 타이머 섹션
    st.header('루틴 타이머')
    start_time = st.time_input('루틴 시작 시간을 입력하세요:', datetime.now().time())
    if st.button('시작'):
        end_time = calculate_end_time(start_time.strftime('%H:%M:%S'))
        st.write(f'루틴 종료 시간: {end_time}')

if __name__ == '__main__':
    main()
