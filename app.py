import streamlit as st
from datetime import timedelta

# 초기 데이터 초기화 (루틴 리스트)
if 'routines' not in st.session_state:
    st.session_state.routines = []

# 루틴 정보를 저장할 데이터 구조
class Routine:
    def __init__(self, name, duration_minutes):
        self.name = name
        self.duration = timedelta(minutes=duration_minutes)
        self.remaining_time = self.duration

# Streamlit 앱 시작
def main():
    st.title('루틴늘리기 앱')

    # 루틴 추가 섹션
    st.header('새로운 루틴 추가')
    new_routine_name = st.text_input('새로운 루틴 이름을 입력하세요:')
    new_routine_duration = st.slider('루틴 시간을 선택하세요 (분)', min_value=1, max_value=120, value=60, step=1)
    if st.button('추가하기'):
        new_routine = Routine(new_routine_name, new_routine_duration)
        st.session_state.routines.append(new_routine)

    # 현재 루틴 리스트 보기
    st.header('현재 루틴 리스트')
    for i, routine in enumerate(st.session_state.routines, start=1):
        st.write(f'{i}. {routine.name} ({routine.duration.seconds // 60} 분)')

        # 타이머 표시
        st.subheader('남은 시간:')
        if routine.remaining_time > timedelta(0):
            minutes = routine.remaining_time.seconds // 60
            seconds = routine.remaining_time.seconds % 60
            st.write(f'{minutes} 분 {seconds} 초')

    # 타이머 업데이트
    if st.session_state.routines:
        for routine in st.session_state.routines:
            routine.remaining_time -= timedelta(seconds=1)
            if routine.remaining_time < timedelta(0):
                routine.remaining_time = timedelta(0)

if __name__ == '__main__':
    main()
