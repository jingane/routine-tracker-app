import streamlit as st
from datetime import datetime, timedelta
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

# 로그인 상태 확인 함수
def is_authenticated():
    return 'authenticated' in st.session_state and st.session_state.authenticated

# 로그아웃 함수
def logout():
    st.session_state.pop('authenticated', None)
    st.session_state.pop('username', None)

    # 로그아웃 후 로그인 페이지로 리다이렉트
    st.experimental_rerun()

# 데이터 로드
st.session_state.data = load_data()

# 로그인 페이지
if not is_authenticated():
    username = st.text_input('아이디를 입력하세요:')
    password = st.text_input('암호를 입력하세요:', type='password')

    if st.button('로그인'):
        if username == 'admin' and password == '3323':
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success('인증되었습니다.')
        else:
            st.error('아이디 또는 암호가 잘못되었습니다.')

# 로그인 상태일 때 프로그램 실행
if is_authenticated():
    # 로그아웃 링크
    if st.button('로그아웃'):
        logout()
    else:
        # 새로운 루틴 입력
        routine = st.text_input('새 루틴을 입력하세요:')
    
        if st.button('시작'):
            if routine:
                end_time = datetime.now() + timedelta(hours=1)
                st.session_state.data['routines'].append({'routine': routine, 'end_time': end_time})
                save_data(st.session_state.data)
                st.success(f"'{routine}' 루틴이 시작되었습니다!")
            else:
                st.warning("루틴을 입력하세요.")
    
        # 진행 중인 루틴 표시 및 타이머 작동
        st.write("## 진행 중인 루틴:")
        current_time = datetime.now()
        for r in st.session_state.data['routines']:
            remaining_time = r['end_time'] - current_time
            if remaining_time.total_seconds() > 0:
                st.write(f"{r['routine']} - 남은 시간: {str(remaining_time).split('.')[0]}")
            else:
                st.write(f"{r['routine']} - 완료")
                r['completed'] = True
                save_data(st.session_state.data)
