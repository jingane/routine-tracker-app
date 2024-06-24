import streamlit as st
from datetime import datetime, timedelta
import time
import json
import os

# 페이지 제목 및 설명을 HTML과 CSS로 스타일링
st.markdown("""
    <style>
    .title {
        font-size: 28px;
        font-weight: bold;
        color: #4CAF50;
    }
    .subtitle {
        font-size: 16px;
        color: #555;
    }
    </style>
    <h1 class="title">나만의 루틴 만들기</h1>
    <p class="subtitle">하루 1시간 루틴을 만들어 내 빈 시간을 꽉 채워볼까요~</p>
""", unsafe_allow_html=True)

# 데이터 파일 경로
DATA_FILE = 'data.json'

# 데이터 로드 함수
def load_data():
    data = {'routines': []}
    try:
        if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
    except json.JSONDecodeError as e:
        st.error(f"JSON 디코딩 오류 발생: {str(e)}")
    return data

# 데이터 저장 함수
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# 데이터 로드
st.session_state.data = load_data()

# 초기 데이터 설정
if 'routines' not in st.session_state.data:
    st.session_state.data['routines'] = []

# 사용자 인증
username = st.text_input('아이디를 입력하세요:')
password = st.text_input('암호를 입력하세요:', type='password')

if username == 'admin' and password == 'Masterit1234!':
    st.success('인증되었습니다.')
else:
    st.error('아이디 또는 암호가 잘못되었습니다.')
    st.stop()

# 새로운 루틴 입력
routine = st.text_input('새 루틴을 입력하세요:')

if st.button('시작'):
    if routine and routine not in [r['routine'] for r in st.session_state.data['routines']]:
        end_time = datetime.now() + timedelta(hours=1)
        st.session_state.data['routines'].append({'routine': routine, 'end_time': end_time})
        st.success(f"'{routine}' 루틴이 시작되었습니다!")
        save_data(st.session_state.data)
    elif routine in [r['routine'] for r in st.session_state.data['routines']]:
        st.warning("이미 진행 중인 루틴입니다.")
    else:
        st.warning("루틴을 입력하세요.")

# 진행 중인 루틴 표시 및 타이머 작동
st.write("## 진행 중인 루틴:")
current_time = datetime.now()
for r in st.session_state.data['routines']:
    remaining_time = r['end_time'] - current_time
    if remaining_time.total_seconds() > 0:
        st.write(f"{r['routine']} - 남은 시간: {str(remaining_time).split('.')[0]}")
        st.write(f"### 타이머:")
        st.progress((datetime.now() - current_time).total_seconds() / (r['end_time'] - current_time).total_seconds())
        time.sleep(1)  # 타이머를 초당 업데이트하기 위해 1초 쉬기
    else:
        st.write(f"{r['routine']} - 완료")
        st.session_state.data['routines'].remove(r)
        save_data(st.session_state.data)

# 새로운 날에 다시 시작할 수 있는 버튼 추가 (없앴음)

# 데이터 저장
save_data(st.session_state.data)
