# app.py

import streamlit as st
import datetime

# 루틴 완료 기록을 저장할 리스트
completed_routines = []

# CSS 스타일 정의
css = """
<style>
body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    padding: 20px;
}
.container {
    max-width: 800px;
    margin: auto;
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
    color: #333;
}
.button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin-top: 10px;
    border-radius: 5px;
    cursor: pointer;
}
.input-box {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;
}
.checklist {
    margin-top: 20px;
}
</style>
"""

# 페이지 레이아웃 설정
st.markdown(css, unsafe_allow_html=True)
st.title('루틴늘리기 앱')
st.markdown('<div class="container">', unsafe_allow_html=True)

# 새로운 루틴 입력 박스
new_routine = st.text_input('새로운 루틴 입력', value='', max_chars=50, key='new_routine')

# 새로운 루틴 추가 버튼
if st.button('루틴 추가', key='add_routine'):
    if new_routine:
        st.markdown(f'<p>새로운 루틴 추가됨: {new_routine}</p>', unsafe_allow_html=True)

# 루틴 완료 버튼
if st.button('시작', key='start_routine'):
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(hours=1)
    st.markdown(f'<p>루틴 시작됨: {start_time.strftime("%H:%M")} 에 시작, {end_time.strftime("%H:%M")} 에 종료 예정</p>', unsafe_allow_html=True)

    # 1시간 후에 완료된 루틴 기록
    completed_routines.append(new_routine)
    st.markdown('<p><strong>완료된 루틴:</strong></p>', unsafe_allow_html=True)
    st.markdown('<ul>', unsafe_allow_html=True)
    for routine in completed_routines:
        st.markdown(f'<li>{routine}</li>', unsafe_allow_html=True)
    st.markdown('</ul>', unsafe_allow_html=True)

# 체크리스트
st.markdown('<div class="checklist">', unsafe_allow_html=True)
st.subheader('매일 잘하고 있는지 체크')
for routine in completed_routines:
    st.markdown(f'<p>- {routine}</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
