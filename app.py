import streamlit as st
import time

# 체크리스트
checklist = []

# 시간 역순 카운트 다운 함수
def countdown(timer):
    while timer >= 0:
        minutes, seconds = divmod(timer, 60)
        time_str = f"{minutes:02}:{seconds:02}"
        st.write(f"남은 시간: {time_str}")
        time.sleep(1)
        timer -= 1

    st.write("루틴 완료!")
    checklist.append("루틴 완료")  # 체크리스트 업데이트

# Streamlit 앱
def main():
    st.title("루틴 늘리기 앱")
    
    # 새로운 루틴 입력
    new_routine = st.text_input("새로운 루틴을 입력하세요:")
    if st.button("루틴 시작"):
        st.write(f"루틴 시작: {new_routine}")
        countdown(3600)  # 1시간(3600초) 카운트 다운
    
    # 기존 루틴 표시
    st.write("기존 루틴:")
    for idx, item in enumerate(checklist):
        st.write(f"{idx+1}. {item}")

if __name__ == "__main__":
    main()
