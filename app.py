import streamlit as st
from datetime import datetime, timedelta

# 페이지 제목 설정
st.title('루틴 늘리기 앱')

# 루틴 입력 받기
new_routine = st.text_input('새로운 루틴을 입력하세요.')

# 저장된 루틴들 표시
st.write('### 저장된 루틴')
saved_routines = st.text_area('저장된 루틴 목록', height=200)
if saved_routines:
    saved_routines_list = saved_routines.split('\n')
else:
    saved_routines_list = []

# 새로운 루틴 추가
if new_routine:
    saved_routines_list.append(new_routine)
    st.text_area('저장된 루틴 목록', '\n'.join(saved_routines_list), height=200)

# 시간 업데이트 함수
def update_time():
    return (datetime.now() + timedelta(hours=1)).strftime('%H:%M:%S')

# 타이머
st.write('### 루틴 타이머')
time_remaining = st.empty()
while True:
    current_time = update_time()
    time_remaining.text(f'남은 시간: {current_time}')
    if current_time == '00:00:00':
        break

# 완료 메시지
st.write('### 루틴 완료!')
st.write('루틴을 성공적으로 완료했습니다.')

# 하단의 빈칸
st.write('### 새로운 루틴 추가하기')
new_routine_text = st.text_input('새로운 루틴을 추가하세요.')

# 앱의 자동 저장 기능을 구현해야 함
