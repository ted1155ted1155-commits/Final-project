import streamlit as st


# 풀이 기록 초기화
def init_statistics():
    if "quiz_history" not in st.session_state:
        st.session_state.quiz_history = []


# 문제 풀 때마다 기록 1개씩 저장
def save_quiz_record(topic, difficulty, quiz, selected_index):
    init_statistics()
    is_correct = (selected_index == quiz["correct_index"])

    st.session_state.quiz_history.append({
        "번호": len(st.session_state.quiz_history) + 1,
        "주제": topic,
        "난이도": difficulty,
        "문제": quiz["question"],
        "선택한 답": quiz["options"][selected_index],
        "정답": quiz["options"][quiz["correct_index"]],
        "정답 여부": "정답" if is_correct else "오답",
        "해설": quiz["explanation"]
    })


# 총 문제 수 / 정답 수 / 오답 수 / 정답률 계산
def calculate_statistics(total_count, correct_count):
    wrong_count = max(0, total_count - correct_count)
    accuracy = (correct_count / total_count * 100) if total_count > 0 else 0.0
    return {
        "total": total_count,
        "correct": correct_count,
        "wrong": wrong_count,
        "accuracy": round(accuracy, 1)
    }