import streamlit as st
import json
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

# 파일 경로 설정
data_file = "routines.json"

# 데이터 로드 함수
def load_data():
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
            # JSON에서 datetime 문자열을 datetime 객체로 변환
            for r in data:
                r['end_time'] = datetime.fromisoformat(r['end_time'])
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        return []

# 데이터 저장 함수
def save_data(data):
    # datetime 객체를 문자열로 변환하여 저장
    data_to_save = []
    for r in data:
        data_to_save.append({
            'routine': r['routine'],
            'end_time': r['end_time'].isoformat()  # datetime 객체를 ISO 포맷 문자열로 변환
        })
    
    with open(data_file, 'w') as f:
        json.dump(data_to_save, f, default=str)  # default=str을 사용하여 datetime을 문자열로 변환

# 루틴 기록을 위한 데이터 초기화
if 'routines' not in st.session_state:
    st.session_state.routines = load_data()

# 새로운 루틴 입력
routine = st.text_input('새 루틴을 입력하세요:')

if st.button('시작'):
    if routine and routine not in [r['routine'] for r in st.session_state.routines]:
        end_time = datetime.now() + timedelta(hours=1)
        st.session_state.routines.append({'routine': routine, 'end_time': end_time})
        save_data(st.session_state.routines)  # 데이터 저장
        st.success(f"'{routine}' 루틴이 시작되었습니다!")
        st.experimental_rerun()  # 새로운 루틴 추가 후 애플리케이션 다시 실행
    elif routine in [r['routine'] for r in st.session_state.routines]:
        st.warning("이미 진행 중인 루틴입니다.")
    else:
        st.warning("루틴을 입력하세요.")

# 진행 중인 루틴 표시 및 관리
st.write("## 진행 중인 루틴:")
current_time = datetime.now()
for r in st.session_state.routines:
    remaining_time = r['end_time'] - current_time
    if remaining_time.total_seconds() > 0:
        # 루틴과 함께 삭제 버튼 추가
        if st.button("삭제"):
            st.session_state.routines.remove(r)
            save_data(st.session_state.routines)  # 데이터 저장
            st.experimental_rerun()  # 삭제 후 애플리케이션 다시 실행
        else:
            st.write(f"{r['routine']}")
    else:
        # 남은 시간이 없는 경우에는 삭제 처리
        st.session_state.routines.remove(r)
        save_data(st.session_state.routines)  # 완료된 데이터 저장

# 새로운 날에 다시 시작할 수 있는 버튼 추가
st.write("## 다시 시작이 가능한 루틴:")
for r in st.session_state.routines:
    if r['end_time'] <= current_time:
        if st.button(f"{r['routine']} 다시 시작"):
            end_time = datetime.now() + timedelta(hours=1)
            r['end_time'] = end_time
            save_data(st.session_state.routines)  # 데이터 업데이트
            st.success(f"'{r['routine']}' 루틴이 다시 시작되었습니다!")
            st.experimental_rerun()  # 루틴 다시 시작 후 애플리케이션 다시 실행

# 루틴 타이머 업데이트 (실시간 업데이트는 Streamlit에서는 고급 기능이므로 대화형 애플리케이션으로 개발할 때 유용합니다)
for r in st.session_state.routines:
    if r['end_time'] > current_time:
        timer_placeholder = st.empty()
        while datetime.now() < r['end_time']:
            remaining_time = r['end_time'] - datetime.now()
            timer_placeholder.write(f"{r['routine']} - 남은 시간: {str(remaining_time).split('.')[0]}")
            time.sleep(1)
        timer_placeholder.write(f"{r['routine']} - 완료")
