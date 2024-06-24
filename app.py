import streamlit as st
from datetime import datetime, timedelta
import time

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

# 로그인 상태 확인 함수
def is_authenticated():
    return 'authenticated' in st.session_state and st.session_state.authenticated

# 로그인 함수
def login(username, password):
    # 예시로 고정된 아이디와 암호 설정
    if username == 'admin' and password == '3323':
        st.session_state.authenticated = True
        st.session_state.username = username
        return True
    else:
        return False

# 로그아웃 함수
def logout():
    st.session_state.pop('authenticated', None)
    st.session_state.pop('username', None)
    st.experimental_rerun()

# 데이터 저장 함수
def save_data(data):
    st.session_state.routines = data

# 데이터 로드 함수
def load_data():
    return st.session_state.get('routines', [])

# 초기 데이터 로드
session_data = load_data()

# 로그인 상태 확인
if not is_authenticated():
    username = st.text_input('아이디를 입력하세요:')
    password = st.text_input('암호를 입력하세요:', type='password')

    if st.button('로그인'):
        if login(username, password):
            st.success('로그인 되었습니다. 잠시만 기다려주세요...')
            st.experimental_rerun()
        else:
            st.error('아이디 또는 암호가 잘못되었습니다.')
else:
    # 로그아웃 링크
    if st.button('로그아웃'):
        logout()
    else:
        # 새 루틴 입력
        routine = st.text_input('새 루틴을 입력하세요:')
    
        if st.button('시작'):
            if routine:
                end_time = datetime.now() + timedelta(hours=1)
                session_data.append({'routine': routine, 'end_time': end_time})
                save_data(session_data)
                st.success(f"'{routine}' 루틴이 시작되었습니다!")
                st.experimental_rerun()
            else:
                st.warning("루틴을 입력하세요.")
    
        # 진행 중인 루틴 표시 및 타이머 작동
        st.write("## 진행 중인 루틴:")
        current_time = datetime.now()
        for r in session_data:
            remaining_time = r['end_time'] - current_time
            if remaining_time.total_seconds() > 0:
                st.write(f"{r['routine']} - 남은 시간: {str(remaining_time).split('.')[0]}", key=r['routine'])
            else:
                st.write(f"{r['routine']} - 완료")
        
        # 실시간으로 시간 업데이트
        st.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(1)
        st.experimental_rerun()
