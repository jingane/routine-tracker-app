import streamlit as st
import json
from datetime import datetime, timedelta

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
            for key in data:
                for r in data[key]:
                    r['end_time'] = datetime.fromisoformat(r['end_time'])
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        return {'in_progress': [], 'completed': []}

# 데이터 저장 함수
def save_data(data):
    # datetime 객체를 문자열로 변환하여 저장
    data_to_save = {
        'in_progress': [],
        'completed': []
    }
    
    for r in data['in_progress']:
        data_to_save['in_progress'].append({
            'routine': r['routine'],
            'end_time': r['end_time'].isoformat()  # datetime 객체를 ISO 포맷 문자열로 변환
        })
    
    for r in data['completed']:
        data_to_save['completed'].append({
            'routine': r['routine'],
            'end_time': r['end_time'].isoformat()  # datetime 객체를 ISO 포맷 문자열로 변환
        })
    
    with open(data_file, 'w') as f:
        json.dump(data_to_save, f, default=str)  # default=str을 사용하여 datetime을 문자열로 변환

# 루틴 기록을 위한 데이터 초기화
if 'routines' not in st.session_state:
    st.session_state.routines = load_data()
    st.session_state.routines['in_progress'] = []
    st.session_state.routines['completed'] = []

# 새로운 루틴 입력
routine = st.text_input('새 루틴을 입력하세요:')

if st.button('시작'):
    if routine and routine not in [r['routine'] for r in st.session_state.routines['in_progress']]:
        end_time = datetime.now() + timedelta(hours=1)
        st.session_state.routines['in_progress'].append({'routine': routine, 'end_time': end_time})
        save_data(st.session_state.routines)  # 데이터 저장
        st.success(f"'{routine}' 루틴이 시작되었습니다!")
        st.experimental_rerun()  # 새로운 루틴 추가 후 애플리케이션 다시 실행
    elif routine in [r['routine'] for r in st.session_state.routines['in_progress']]:
        st.warning("이미 진행 중인 루틴입니다.")
    else:
        st.warning("루틴을 입력하세요.")

# 진행 중인 루틴 표시 및 관리
st.write("## 진행 중인 루틴:")
current_time = datetime.now()
for r in st.session_state.routines['in_progress']:
    remaining_time = r['end_time'] - current_time
    if remaining_time.total_seconds() > 0:
        # 루틴과 함께 삭제 버튼 추가
        if st.button(f"완료: {r['routine']}"):
            st.session_state.routines['completed'].append(r)
            st.session_state.routines['in_progress'].remove(r)
            save_data(st.session_state.routines)  # 데이터 저장
            st.experimental_rerun()  # 완료 후 애플리케이션 다시 실행
        else:
            st.write(f"{r['routine']} - 남은 시간: {str(remaining_time).split('.')[0]}")
    else:
        st.warning(f"{r['routine']} - 완료")

# 완료된 루틴 표시 및 재시작 버튼 추가
st.write("## 완료된 루틴:")
for r in st.session_state.routines['completed']:
    if st.button(f"{r['routine']} 다시 시작"):
        end_time = datetime.now() + timedelta(days=1)  # 내일로 설정
        r['end_time'] = end_time
        st.session_state.routines['in_progress'].append(r)
        st.session_state.routines['completed'].remove(r)
        save_data(st.session_state.routines)  # 데이터 업데이트
        st.success(f"'{r['routine']}' 루틴이 내일 다시 시작됩니다!")
        st.experimental_rerun()  # 루틴 다시 시작 후 애플리케이션 다시 실행
    else:
        st.write(f"{r['routine']} - 완료")

