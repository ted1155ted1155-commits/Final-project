import streamlit as st


# 오답노트 초기화
def init_wrong_note():
    if "wrong_notes" not in st.session_state:
        st.session_state.wrong_notes = []


# 틀린 문제와 답안 정보 저장
def save_wrong_question(quiz, selected_index):
    init_wrong_note()

    if selected_index == quiz["correct_index"]:
        return

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

            # 오답 다시 풀기
            retry = st.radio(
                "다시 풀어보세요.",
                range(len(note["options"])),
                format_func=lambda x: note["options"][x],
                key=f"retry_{i}",
                index=None
            )

            if st.button("정답 확인", key=f"check_{i}"):
                if retry is None:
                    st.warning("답을 선택해주세요.")
                elif retry == note["correct_index"]:
                    st.success("정답입니다!")
                else:
                    st.error("틀렸습니다. 다시 도전하세요.")

                if retry is not None:
                    st.write("정답:", note["correct_answer"])
                    st.write("해설:", note["explanation"])