import streamlit as st
import random
import time

# 1. 세션 상태 초기화 (게임 데이터 저장 창고)
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.score = 0
    st.session_state.q_num = 1
    st.session_state.total_questions = 10
    st.session_state.semester_mode = "1학년 1학기"
    st.session_state.game_mode = "더하기"
    st.session_state.need_new_question = True
    st.session_state.answered = False
    st.session_state.game_over = False
    st.session_state.selected_character = "🐰 토끼 래비"
    st.session_state.start_time = 0.0
    st.session_state.total_time = 0.0

# 캐릭터별 대사 데이터 베이스
char_dialogue = {
    "🐰 토끼 래비": {
        "welcome": "안녕! 난 래비야! 우리가 고른 맞춤형 문제를 풀러 가볼까? 🥕", 
        "correct": "🐰 래비: 정답이야! 귀가 쫑긋해질 정도로 멋진 실력이야! 🥕✨", 
        "wrong": "🐰 래비: 아쉽다아! 괜찮아, 다음 문제는 꼭 맞힐 수 있어! 🐾"
    },
    "🐻 곰돌이 곰이": {
        "welcome": "안녕~ 난 곰이야! 우리가 직접 만든 문제라 더 재미있을 거야! 🍯", 
        "correct": "🐻 곰이: 우와 대단해! 정말 달콤한 정답이야! 🍯💛", 
        "wrong": "🐻 곰이: 갠차나 갠차나~ 다음 문제에서 실력을 보여줘! 🌲"
    },
    "🐱 고양이 야옹이": {
        "welcome": "야옹~ 난 야옹이야! 마음에 드는 연산을 골랐으니 시작해보라냥! 🐾", 
        "correct": "🐱 야옹이: 대단하다냥! 완벽한 정답이다냥! 최고코코! 🐟", 
        "wrong": "🐱 야옹이: 냐아오옹~ 아쉽다냥! 다음엔 꼭 성공하라냥! 🐾"
    }
}

# 2. 학년별 수 범위 + 선택 연산 반영 문제 생성 알고리즘
def generate_question(semester, mode):
    current_op = mode
    # 혼합 모드일 경우 무작위 선택
    if mode == "혼합":
        if "1학년" in semester:
            current_op = random.choice(["더하기", "빼기"]) # 1학년은 더하기/빼기만 혼합
        else:
            current_op = random.choice(["더하기", "빼기", "곱하기"]) # 2학년은 곱하기까지 혼합

    # 난이도 세부 설정
    if semester == "1학년 1학기":
        if current_op == "더하기":
            n1 = random.randint(1, 8)
            n2 = random.randint(1, 9 - n1) # 합이 9 이하
            ans = n1 + n2
            symbol = "+"
        elif current_op == "빼기":
            n1 = random.randint(1, 9)
            n2 = random.randint(1, n1) # 받아내림 없음
            ans = n1 - n2
            symbol = "-"
        else: # 1학년이 곱하기를 고른 경우 (기초 구구단)
            n1 = random.choice([2, 5]) # 쉬운 2, 5단 위주
            n2 = random.randint(1, 9)
            ans = n1 * n2
            symbol = "×"

    elif semester == "1학년 2학기":
        if current_op == "더하기":
            n1 = random.randint(5, 15)
            n2 = random.randint(5, 15) # 합이 30 이내
            ans = n1 + n2
            symbol = "+"
        elif current_op == "빼기":
            n1 = random.randint(10, 29)
            n2 = random.randint(1, 9) # 받아내림이 적은 두자리-한자리
            ans = n1 - n2
            symbol = "-"
        else:
            n1 = random.randint(2, 5) # 2~5단 범위
            n2 = random.randint(1, 9)
            ans = n1 * n2
            symbol = "×"

    elif semester == "2학년 1학기":
        if current_op == "더하기":
            n1 = random.randint(10, 69)
            n2 = random.randint(11, 29) # 본격 두 자리 수 더하기
            ans = n1 + n2
            symbol = "+"
        elif current_op == "빼기":
            n1 = random.randint(30, 99)
            n2 = random.randint(11, n1 - 1) # 받아내림 있는 빼기 포함
            ans = n1 - n2
            symbol = "-"
        else:
            n1 = random.randint(2, 9)
            n2 = random.randint(1, 9)
            ans = n1 * n2
            symbol = "×"

    else: # 2학년 2학기 (가장 높은 난이도)
        if current_op == "더하기":
            n1 = random.randint(25, 89)
            n2 = random.randint(25, 99)
            ans = n1 + n2
            symbol = "+"
        elif current_op == "빼기":
            n1 = random.randint(50, 99)
            n2 = random.randint(15, n1 - 1)
            ans = n1 - n2
            symbol = "-"
        else:
            n1 = random.randint(2, 9) # 전 범위 구구단 심화
            n2 = random.randint(1, 9)
            ans = n1 * n2
            symbol = "×"
    
    # 객관식 보기 생성
    options = {ans}
    while len(options) < 4:
        if semester == "1학년 1학기" and current_op != "곱하기":
            wrong = random.randint(0, 10)
        else:
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
st.set_page_config(page_title="교과서 산수 왕", page_icon="🏫", layout="centered")
current_char = st.session_state.selected_character

# [화면 1] 게임 종료 결과 화면
if st.session_state.game_over:
    st.title("🏁 모험 끝! 성적표 발표")
    st.balloons()
    
    min_time = int(st.session_state.total_time // 60)
    sec_time = int(st.session_state.total_time % 60)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🎯 맞힌 문제", f"{st.session_state.score} / {st.session_state.total_questions} 문제")
    with col2:
        if min_time > 0:
            st.metric("⏱️ 걸린 시간", f"{min_time}분 {sec_time}초")
        else:
            st.metric("⏱️ 걸린 시간", f"{sec_time}초")

    st.markdown(f"""
    <div style='background-color: #FFF0F5; padding: 20px; border-radius: 30px; border: 3px dashed #FF69B4; text-align: center;'>
        <h3>설정: {st.session_state.semester_mode} [{st.session_state.game_mode}]</h3>
        <p style='font-size: 20px;'>문제당 평균 약 <b>{round(st.session_state.total_time / st.session_state.total_questions, 1)}초</b>씩 걸려서 통과했어요!</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    
    if st.button("🏠 처음 화면으로 돌아가기", use_container_width=True):
        st.session_state.game_over = False
        st.session_state.game_started = False
        st.rerun()

# [화면 2] 대기 화면 (캐릭터, 학년, 연산, 문제 수 선택)
elif not st.session_state.game_started:
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🎒 스마트 교과서 산수 게임</h1>", unsafe_allow_html=True)
    st.write("아이의 실력에 맞춰 조건들을 자유롭게 조합해 보세요!")
    
    st.session_state.selected_character = st.radio(
        "🤝 함께할 동물 친구 선택", 
        ["🐰 토끼 래비", "🐻 곰돌이 곰이", "🐱 고양이 야옹이"],
        horizontal=True
    )
    st.write("---")
    
    # 🌟 세 가지 선택 요소를 깔끔하게 3열로 배치했습니다!
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.semester_mode = st.selectbox(
            "🏫 학년/학기 (숫자 크기)", 
            ["1학년 1학기", "1학년 2학기", "2학년 1학기", "2학년 2학기"]
        )
    with col2:
        st.session_state.game_mode = st.selectbox(
            "🧮 연산 종류 선택",
            ["더하기", "빼기", "곱하기", "혼합"]
        )
    with col3:
        st.session_state.total_questions = st.number_input(
            "💎 문제 개수 (5~100)", 
            min_value=5, max_value=100, value=10, step=5
        )
    
    st.write("")
    if st.button("🚀 나만의 맞춤 수학 탐험대 출발!", use_container_width=True):
        st.session_state.game_started = True
        st.session_state.score = 0
        st.session_state.q_num = 1
        st.session_state.need_new_question = True
        st.session_state.start_time = time.time()
        st.rerun()

# [화면 3] 게임 진행 중 화면
else:
    if st.session_state.need_new_question:
        generate_question(st.session_state.semester_mode, st.session_state.game_mode)

    # 대사창 UI
    st.markdown(f"""
    <div style='background-color: #FFF9C4; padding: 15px; border-radius: 25px; border: 2px solid #FFF59D; margin-bottom: 15px;'>
        <span style='font-size: 20px; font-weight: bold;'>{char_dialogue[current_char]['welcome']}</span>
    </div>
    """, unsafe_allow_html=True)

    # 프로그레스 바
    progress = st.session_state.q_num / st.session_state.total_questions
    st.progress(progress)
    st.write(f"⭐ 난이도: {st.session_state.semester_mode} ({st.session_state.game_mode}) | 💎 문제 {st.session_state.q_num} / {st.session_state.total_questions}")
    
    # 문제 대형 출력
    st.markdown(f"<h1 style='text-align: center; font-size: 85px; color: #2E7D32;'>{st.session_state.n1} {st.session_state.symbol} {st.session_state.n2} = ?</h1>", unsafe_allow_html=True)
    st.write("")
    
    # 4지선다 버튼 배치
    cols = st.columns(4)
    for i, opt in enumerate(st.session_state.options):
        with cols[i]:
            if st.button(str(opt), key=f"ans_{i}", disabled=st.session_state.answered, use_container_width=True):
                st.session_state.answered = True
                if opt == st.session_state.ans:
                    st.session_state.score += 1
                    st.session_state.user_correct = True
                st.rerun()

    # 정답 피드백 및 자동 넘어가기
    if st.session_state.answered:
        st.write("---")
        if st.session_state.user_correct:
            st.success(char_dialogue[current_char]['correct'])
        else:
            st.error(f"{char_dialogue[current_char]['wrong']} (정답은 {st.session_state.ans}이야!)")

        time.sleep(1.7)
        
        if st.session_state.q_num < st.session_state.total_questions:
            st.session_state.q_num += 1
            st.session_state.need_new_question = True
        else:
            st.session_state.game_over = True
            st.session_state.total_time = time.time() - st.session_state.start_time
        st.rerun()
