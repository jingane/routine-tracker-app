import streamlit as st
import json
from datetime import datetime, timedelta
import time

# 페이지 제목 및 설명을 HTML과 CSS로 스타일링
st.markdown("""
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #4CAF50;
    }
    .subtitle {
        font-size: 20px;
        color: #555;
    }
    </style>
    <h1 class="title">나만의 루틴 만들기</h1>
    <p class="subtitle">하루 1시간 루틴을 만들어 내 빈 시간을 꽉 채워볼까요~</p>
""", unsafe_allow_html=True)

# 아이디와 암호 입력
username = st.sidebar.text_input("아이디")
password = st.sidebar.text_input("암호", type="password")

# 초기 관리자 아이디와 암호
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Masterit1234!"

# 세션 데이터 파일 경로
DATA_FILE = "routine_data.json"

# 관리자 로그인 체크
if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
    st.sidebar.success("로그인 성공!")
else:
    st.sidebar.error("아이디 또는 암호가 올바르지 않습니다.")
    st.stop()

# 데이터 로드 함수
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {'routines': [], 'checklist': []}
    return data

# 데이터 저장 함수
def save_data(data):
    def datetime_converter(o):
        if isinstance(o, datetime):
            return o.isoformat()
        raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, default=datetime_converter)

# 초기 데이터 로드
session_data = load_data()

# 루틴 기록을 위한 데이터 초기화
if 'routines' not in session_data:
    session_data['routines'] = []

if 'checklist' not in session_data:
    session_data['checklist'] = []

# 새로운 루틴 입력
routine = st.text_input('새 루틴을 입력하세요:')

if st.button('시작'):
    if routine and routine not in [r['routine'] for r in session_data['routines']]:
        end_time = datetime.now() + timedelta(hours=1)
        session_data['routines'].append({'routine': routine, 'end_time': end_time})
        st.success(f"'{routine}' 루틴이 시작되었습니다!")
    elif routine in [r['routine'] for r in session_data['routines']]:
        st.warning("이미 진행 중인 루틴입니다.")
    else:
        st.warning("루틴을 입력하세요.")

# 진행 중인 루틴 표시
st.write("## 진행 중인 루틴:")
current_time = datetime.now()
for r in session_data['routines']:
    remaining_time = r['end_time'] - current_time
    if remaining_time.total_seconds() > 0:
        st.write(f"{r['routine']} - 남은 시간: {str(remaining_time).split('.')[0]}")
    else:
        st.write(f"{r['routine']} - 완료")
        if r['routine'] not in session_data['checklist']:
            session_data['checklist'].append(r['routine'])

# 완료된 루틴이 있는 경우 새로운 루틴 입력 칸 초기화
completed_routines = [r for r in session_data['routines'] if r['end_time'] <= current_time]
if completed_routines:
    routine = ''

# 새로운 날에 다시 시작할 수 있는 버튼 추가
st.write("## 다시 시작 가능한 루틴:")
for r in session_data['routines']:
    if r['end_time'] <= current_time:
        if st.button(f"{r['routine']} 다시 시작"):
            end_time = datetime.now() + timedelta(hours=1)
            session_data['routines'].append({'routine': r['routine'], 'end_time': end_time})
            st.success(f"'{r['routine']}' 루틴이 다시 시작되었습니다!")
            save_data(session_data)
            st.experimental_rerun()

# 체크리스트 표시
st.write("## 체크리스트:")
for item in session_data['checklist']:
    st.write(f"- {item}")

# 데이터 자동 저장
save_data(session_data)

# 루틴 타이머 업데이트
for r in session_data['routines']:
    if r['end_time'] > current_time:
        timer_placeholder = st.empty()
        while datetime.now() < r['end_time']:
            remaining_time = r['end_time'] - datetime.now()
            timer_placeholder.write(f"{r['routine']} - 남은 시간: {str(remaining_time).split('.')[0]}")
            time.sleep(1)
        timer_placeholder.write(f"{r['routine']} - 완료")
        if r['routine'] not in session_data['checklist']:
            session_data['checklist'].append(r['routine'])
            save_data(session_data)
