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
    data = {'routines': [], 'checklist': []}
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

if 'checklist' not in st.session_state.data:
    st.session_state.data['checklist'] = []

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
    elif routine in [r['routine'] for r in st.session_state.data['routines']]:
        st.warning("이미 진행 중인 루틴입니다.")
    else:
        st.warning("루틴을 입력하세요.")

# 진행 중인 루틴 표시
st.write("## 진행 중인 루틴:")
current_time = datetime.now()
for r in st.session_state.data['routines']:
    remaining_time = r['end_time'] - current_time
    if remaining_time.total_seconds() > 0:
        st.write(f"{r['routine']} - 남은 시간: {str(remaining_time).split('.')[0]}")
    else:
        st.write(f"{r['routine']} - 완료")
        if r['routine'] not in st.session_state.data['checklist']:
            st.session_state.data['checklist'].append(r['routine'])

# 완료된 루틴이 있는 경우 새로운 루틴 입력 칸 초기화
completed_routines = [r for r in st.session_state.data['routines'] if r['end_time'] <= current_time]
if completed_routines:
    routine = ''

# 새로운 날에 다시 시작할 수 있는 버튼 추가
st.write("## 다시 시작 가능한 루틴:")
for r in st.session_state.data['routines']:
    if r['end_time'] <= current_time:
        if st.button(f"{r['routine']} 다시 시작"):
            end_time = datetime.now() + timedelta(hours=1)
            st.session_state.data['routines'].append({'routine': r['routine'], 'end_time': end_time})
            st.success(f"'{r['routine']}' 루틴이 다시 시작되었습니다!")
            save_data(st.session_state.data)
            st.experimental_rerun()

# 체크리스트 표시
st.write("## 체크리스트:")
for item in st.session_state.data['checklist']:
    st.write(f"- {item}")

# 루틴 타이머 업데이트
for r in st.session_state.data['routines']:
    if r['end_time'] > current_time:
        timer_placeholder = st.empty()
        while datetime.now() < r['end_time']:
            remaining_time = r['end_time'] - datetime.now()
            timer_placeholder.write(f"{r['routine']} - 남은 시간: {str(remaining_time).split('.')[0]}")
            time.sleep(1)
        timer_placeholder.write(f"{r['routine']} - 완료")
        if r['routine'] not in st.session_state.data['checklist']:
            st.session_state.data['checklist'].append(r['routine'])
        save_data(st.session_state.data)
        st.experimental_rerun()
