import streamlit as st

# Streamlit 앱
def main():
    st.title("루틴 늘리기 앱")

    # HTML과 CSS로 시계처럼 시간이 흐르는 효과 구현
    st.components.v1.html("""
    <div id="countdown">
        <div id="timer">60:00</div>
    </div>
    <style>
    #countdown {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
        font-size: 48px;
        font-weight: bold;
        background-color: #f0f0f0;
    }
    #timer {
        animation: countdown-animation 3600s linear;
    }
    @keyframes countdown-animation {
        from { width: 100%; }
        to { width: 0%; }
    }
    </style>
    <script>
    // JavaScript to update countdown timer
    setInterval(updateTimer, 1000);

    function updateTimer() {
        var timerElement = document.getElementById("timer");
        var timeLeft = parseFloat(timerElement.textContent);
        if (timeLeft > 0) {
            timeLeft -= 1;
            var minutes = Math.floor(timeLeft / 60);
            var seconds = Math.floor(timeLeft % 60);
            timerElement.textContent = minutes.toString().padStart(2, '0') + ':' + seconds.toString().padStart(2, '0');
        }
    }
    </script>
    """)

    # 새로운 루틴 입력
    new_routine = st.text_input("새로운 루틴을 입력하세요:")
    if st.button("루틴 시작"):
        st.write(f"루틴 시작: {new_routine}")

    # 기존 루틴 표시
    st.write("기존 루틴:")
    st.write("1. 루틴 1 완료")
    st.write("2. 루틴 2 완료")

if __name__ == "__main__":
    main()
