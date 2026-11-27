import streamlit as st


# 오답노트 초기화
def init_wrong_note():
    if "wrong_notes" not in st.session_state:
        st.session_state.wrong_notes = []


# 틀린 문제 저장
def save_wrong_question(quiz):
    init_wrong_note()

    st.session_state.wrong_notes.append({
        "question": quiz["question"],
        "options": quiz["options"].copy()
    })