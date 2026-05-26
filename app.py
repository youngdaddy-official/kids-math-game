import streamlit as st
import random

# 초기 설정
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.q_num = 1
    st.session_state.game_over = False
    st.session_state.need_new_question = True

def generate_question():
    op = random.choice(['+', '-'])
    if op == '+':
        n1, n2 = random.randint(5, 30), random.randint(1, 20)
        ans = n1 + n2
    else:
        n1 = random.randint(10, 40)
        n2 = random.randint(1, n1)
        ans = n1 - n2
    
    # 보기 생성 (정답 포함 4개)
    options = {ans}
    while len(options) < 4:
        options.add(ans + random.randint(-5, 5))
    options = list(options)
    random.shuffle(options)
    
    st.session_state.n1, st.session_state.n2, st.session_state.op = n1, n2, op
    st.session_state.ans, st.session_state.options = ans, options
    st.session_state.need_new_question = False
    st.session_state.answered = False

# 웹 화면 구성
st.title("🧮 신나는 산수 퀴즈!")
if st.session_state.game_over:
    st.balloons()
    st.success(f"참 잘했어요! 5문제 중 {st.session_state.score}문제를 맞혔어요!")
    if st.button("다시 하기"):
        st.session_state.score = 0
        st.session_state.q_num = 1
        st.session_state.game_over = False
        st.session_state.need_new_question = True
        st.rerun()
else:
    if st.session_state.need_new_question: generate_question()
    st.subheader(f"문제 {st.session_state.q_num}:")
    st.header(f"{st.session_state.n1} {st.session_state.op} {st.session_state.n2} = ?")
    
    for opt in st.session_state.options:
        if st.button(str(opt), key=f"btn_{opt}", disabled=st.session_state.answered):
            st.session_state.answered = True
            if opt == st.session_state.ans:
                st.session_state.score += 1
                st.success("정답입니다! 🎉")
            else:
                st.error(f"아쉬워요! 정답은 {st.session_state.ans}였어요.")
            st.button("다음 문제")
            if st.session_state.answered:
                if st.session_state.q_num < 5:
                    st.session_state.q_num += 1
                    st.session_state.need_new_question = True
                else:
                    st.session_state.game_over = True
                st.rerun()
