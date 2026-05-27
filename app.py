import streamlit as st
import random

# 1. 세션 상태 초기화 (게임 데이터 저장 창고)
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.score = 0
    st.session_state.q_num = 1
    st.session_state.total_questions = 10
    st.session_state.game_mode = "더하기"
    st.session_state.need_new_question = True
    st.session_state.answered = False
    st.session_state.game_over = False

# 2. 문제 생성 알고리즘
def generate_question(mode):
    current_op = mode
    if mode == "혼합":
        current_op = random.choice(["더하기", "빼기", "곱하기"])

    if current_op == "더하기":
        n1 = random.randint(5, 50)
        n2 = random.randint(1, 30)
        ans = n1 + n2
        symbol = "+"
    elif current_op == "빼기":
        n1 = random.randint(10, 50)
        n2 = random.randint(1, n1) # 음수 방지
        ans = n1 - n2
        symbol = "-"
    else: # 곱하기 (구구단)
        n1 = random.randint(2, 9)
        n2 = random.randint(1, 9)
        ans = n1 * n2
        symbol = "×"
    
    # 객관식 보기 생성
    options = {ans}
    while len(options) < 4:
        wrong = ans + random.randint(-10, 10)
        if wrong >= 0 and wrong != ans:
            options.add(wrong)
    
    options_list = list(options)
    random.shuffle(options_list)
    
    st.session_state.n1 = n1
    st.session_state.n2 = n2
    st.session_state.symbol = symbol
    st.session_state.ans = ans
    st.session_state.options = options_list
    st.session_state.need_new_question = False
    st.session_state.answered = False
    st.session_state.user_correct = False

# --- UI 레이아웃 설정 ---
st.set_page_config(page_title="초등 산수 왕", page_icon="✏️", layout="centered")

# [상단바] 진행 상황 표시
if st.session_state.game_started and not st.session_state.game_over:
    progress = st.session_state.q_num / st.session_state.total_questions
    st.progress(progress)

# [화면 1] 게임 종료 결과
if st.session_state.game_over:
    st.title("🏆 미션 완료!")
    st.balloons()
    st.metric("최종 점수", f"{st.session_state.score} / {st.session_state.total_questions}")
    
    if st.session_state.score == st.session_state.total_questions:
        st.success("🌟 완벽해요! 당신은 진정한 수학 마스터입니다! 🌟")
    else:
        st.info("열심히 했어요! 한 번 더 도전하면 다 맞힐 수 있을 거예요!")

    if st.button("🏠 처음으로 돌아가기", use_container_width=True):
        st.session_state.game_over = False
        st.session_state.game_started = False
        st.rerun()

# [화면 2] 모드 및 문제 수 선택 화면
elif not st.session_state.game_started:
    st.title("🎨 산수 게임 2.0")
    st.write("오늘 풀고 싶은 연산과 문제 수를 골라주세요!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.game_mode = st.selectbox("연산 모드 선택", ["더하기", "빼기", "곱하기", "혼합"])
    with col2:
        st.session_state.total_questions = st.number_input("문제 수 (5~30)", min_value=5, max_value=30, value=10, step=5)
    
    st.write("---")
    st.info(f"💡 **{st.session_state.game_mode}** 모드로 **{st.session_state.total_questions}문제**를 풀게 됩니다.")
    
    if st.button("🎮 게임 시작!", use_container_width=True):
        st.session_state.game_started = True
        st.session_state.score = 0
        st.session_state.q_num = 1
        st.session_state.need_new_question = True
        st.rerun()

# [화면 3] 게임 플레이 중
else:
    if st.session_state.need_new_question:
        generate_question(st.session_state.game_mode)

    st.subheader(f"💎 문제 {st.session_state.q_num} / {st.session_state.total_questions}")
    st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{st.session_state.n1} {st.session_state.symbol} {st.session_state.n2} = ?</h1>", unsafe_allow_html=True)
    
    st.write("")
    
    # 보기 버튼 배치
    cols = st.columns(4)
    for i, opt in enumerate(st.session_state.options):
        with cols[i]:
            if st.button(str(opt), key=f"ans_{i}", disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == st.session_state.ans:
                    st.session_state.score += 1
                    st.session_state.user_correct = True
                st.rerun()

    # 정답 확인 후 피드백
    if st.session_state.answered:
        st.write("---")
        if st.session_state.user_correct:
            st.success("🎯 정답입니다! 최고예요!")
        else:
            st.error(f"😯 아쉬워요! 정답은 {st.session_state.ans}였어요.")

        if st.session_state.q_num < st.session_state.total_questions:
            if st.button("다음 문제로 ➡️", use_container_width=True):
                st.session_state.q_num += 1
                st.session_state.need_new_question = True
                st.rerun()
        else:
            if st.button("🏁 결과 확인하기", use_container_width=True):
                st.session_state.game_over = True
                st.rerun()
