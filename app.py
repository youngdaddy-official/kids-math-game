import streamlit as st
import random
import time

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
    st.session_state.selected_character = "🐰 토끼 래비"

# 2. 캐릭터별 대사 데이터 베이스
char_dialogue = {
    "🐰 토끼 래비": {
        "welcome": "안녕! 난 래비야! 깡총깡총 신나게 수학 문제를 풀어보자! 🥕", 
        "correct": "🐰 래비: 와아! 정답이야! 너 진짜 천재구나! 🥕✨", 
        "wrong": "🐰 래비: 아쉽다아! 괜찮아, 다음 문제는 꼭 맞힐 수 있어! 힘내! 🐾"
    },
    "🐻 곰돌이 곰이": {
        "welcome": "안녕~ 난 곰이야! 우리 차근차근 재미있게 문제를 맞춰보자! 🍯", 
        "correct": "🐻 곰이: 우와 대단해! 달콤한 꿀맛 같은 정답이야! 🍯💛", 
        "wrong": "🐻 곰이: 토닥토닥~ 너무 아쉬워하지 마! 다음 문제 고고! 🌲"
    },
    "🐱 고양이 야옹이": {
        "welcome": "야옹~ 난 야옹이야! 날카로운 눈빛으로 정답을 골라보라냥! 🐾", 
        "correct": "🐱 야옹이: 대단하다냥! 완벽한 정답이다냥! 최고코코! 🐟", 
        "wrong": "🐱 야옹이: 냐아오옹~ 아쉽다냥! 다음엔 꼭 성공하라냥! 🐾"
    }
}

# 3. 문제 생성 알고리즘
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
        n2 = random.randint(1, n1)
        ans = n1 - n2
        symbol = "-"
    else:
        n1 = random.randint(2, 9)
        n2 = random.randint(1, 9)
        ans = n1 * n2
        symbol = "×"
    
    # 객관식 보기 생성
    options = {ans}
    while len(options) < 4:
        wrong = ans + random.randint(-7, 7)
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
st.set_page_config(page_title="귀여운 산수 왕", page_icon="🐰", layout="centered")

# 캐릭터 테마별 색상 설정
current_char = st.session_state.selected_character

# [화면 1] 게임 종료 결과
if st.session_state.game_over:
    st.title("🏆 미션 완료! 축하해!")
    st.balloons()
    
    st.markdown(f"""
    <div style='background-color: #FFF0F5; padding: 25px; border-radius: 30px; border: 3px dashed #FF69B4; text-align: center;'>
        <h2>✨ {st.session_state.score} / {st.session_state.total_questions} 문제 성공! ✨</h2>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    
    if st.session_state.score == st.session_state.total_questions:
        st.success(f"🌟 {current_char[:2]} 완벽해! 너가 우리 동네 최고의 산수 왕이야!!")
    else:
        st.info(f"👍 정말 열심히 잘 풀었어! 다음 모험에서 또 만나자!")

    if st.button("🏠 처음으로 돌아가기", use_container_width=True):
        st.session_state.game_over = False
        st.session_state.game_started = False
        st.rerun()

# [화면 2] 귀여운 대기 화면 (캐릭터, 모드 선택)
elif not st.session_state.game_started:
    st.markdown("<h1 style='text-align: center; color: #FF6b6b;'>🧸 말하는 산수 동물원 2.0</h1>", unsafe_allow_html=True)
    st.write("같이 공부할 귀여운 동물 친구와 연산을 골라보세요!")
    
    # 캐릭터 선택 추가!
    st.session_state.selected_character = st.radio(
        "🤝 함께 모험을 떠날 친구를 골라줘!", 
        ["🐰 토끼 래비", "🐻 곰돌이 곰이", "🐱 고양이 야옹이"],
        horizontal=True
    )
    
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.game_mode = st.selectbox("어떤 연산을 연습할까?", ["더하기", "빼기", "곱하기", "혼합"])
    with col2:
        st.session_state.total_questions = st.number_input("몇 문제를 풀까? (5~30)", min_value=5, max_value=30, value=10, step=5)
    
    # 파스텔톤 안내 상자
    st.markdown(f"""
    <div style='background-color: #E8F5E9; padding: 15px; border-radius: 20px; text-align: center; border: 1px solid #C8E6C9;'>
        <b>{st.session_state.selected_character}</b>와 함께 <b>{st.session_state.game_mode}</b> 모드로 <b>{st.session_state.total_questions}문제</b> 시험을 시작합니다!
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    
    if st.button("🚀 신나는 수학 모험 시작하기!", use_container_width=True):
        st.session_state.game_started = True
        st.session_state.score = 0
        st.session_state.q_num = 1
        st.session_state.need_new_question = True
        st.rerun()

# [화면 3] 게임 플레이 중
else:
    if st.session_state.need_new_question:
        generate_question(st.session_state.game_mode)

    # 귀여운 캐릭터 말상자 UI
    st.markdown(f"""
    <div style='background-color: #FFF9C4; padding: 18px; border-radius: 25px; border: 2px solid #FFF59D; margin-bottom: 15px;'>
        <span style='font-size: 22px; font-weight: bold;'>{char_dialogue[current_char]['welcome']}</span>
    </div>
    """, unsafe_allow_html=True)

    # 진행 상단바
    progress = st.session_state.q_num / st.session_state.total_questions
    st.progress(progress)
    st.write(f"💎 문제 {st.session_state.q_num} / {st.session_state.total_questions}")
    
    # 문제 출력
    st.markdown(f"<h1 style='text-align: center; font-size: 85px; color: #4A90E2;'>{st.session_state.n1} {st.session_state.symbol} {st.session_state.n2} = ?</h1>", unsafe_allow_html=True)
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

    # 정답 확인 후 피드백 및 [자동 화면 넘어가기] 핵심 로직
    if st.session_state.answered:
        st.write("---")
        if st.session_state.user_correct:
            st.success(char_dialogue[current_char]['correct'])
        else:
            st.error(f"{char_dialogue[current_char]['wrong']} (정답은 {st.session_state.ans}야!)")

        # 🔔 중요: 아이가 정답 화면을 확인할 수 있도록 1.7초간 정지 후 자동으로 코드를 넘김
        time.sleep(1.7)
        
        if st.session_state.q_num < st.session_state.total_questions:
            st.session_state.q_num += 1
            st.session_state.need_new_question = True
        else:
            st.session_state.game_over = True
        st.rerun()
