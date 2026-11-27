import streamlit as st


# 오답노트 초기화
def init_wrong_note():
    if "wrong_notes" not in st.session_state:
        st.session_state.wrong_notes = []


# 틀린 문제와 답안 정보 저장
def save_wrong_question(quiz, selected_index):
    init_wrong_note()

    st.session_state.wrong_notes.append({
        "question": quiz["question"],
        "options": quiz["options"].copy(),
        "selected_answer": quiz["options"][selected_index],
        "correct_answer": quiz["options"][quiz["correct_index"]],
        "correct_index": quiz["correct_index"],
        "explanation": quiz["explanation"]
    })


# 오답노트 화면
def show_wrong_note():
    init_wrong_note()

    st.header("오답노트")
    notes = st.session_state.wrong_notes

    if not notes:
        st.info("저장된 오답이 없습니다.")
        return

    st.write(f"총 {len(notes)}개의 오답")

    for i, note in enumerate(notes, start=1):
        with st.expander(f"{i}. {note['question']}"):
            st.write("문제:", note["question"])
            st.error("내가 선택한 답: " + note["selected_answer"])
            st.success("정답: " + note["correct_answer"])
            st.write("해설:", note["explanation"])
