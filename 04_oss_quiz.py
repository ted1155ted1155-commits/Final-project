
import json

import streamlit as st
from google import genai
from google.genai import types
from wrong_note import save_wrong_question, show_wrong_note
MODEL = "gemini-3.5-flash-lite"

st.title("🎓 DCU OSS AI Quiz")
st.caption("Gemini를 활용한 OSS 시험 대비 도우미")


# AI의 역할과 문제 출제 규칙
SYSTEM_INSTRUCTION = """
당신은 대학교 1학년을 위한 OSS 시험 출제 도우미입니다.

1. 선택한 주제에 관한 객관식 문제를 1개 출제하세요.
2. 보기 4개 중 정답은 반드시 하나여야 합니다.
3. 문제와 해설은 한국어로 작성하세요.
4. 초보 학생이 이해할 수 있는 난이도로 출제하세요.
5. 힌트에는 정답 번호를 직접 알려주지 마세요.
6. 학습 내용에 관한 사실관계를 정확히 확인하세요.
"""


# Gemini API 연결
@st.cache_resource
def get_client():
    return genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"],
        http_options=types.HttpOptions(
            timeout=30000,
            retry_options=types.HttpRetryOptions(
                attempts=2
            )
        )
    )


client = get_client()


# AI 문제의 응답 형식
QUIZ_SCHEMA = {
    "type": "object",
    "properties": {
        "question": {"type": "string"},
        "options": {
            "type": "array",
            "items": {"type": "string"}
        },
        "correct_index": {"type": "integer"},
        "hint": {"type": "string"},
        "explanation": {"type": "string"}
    },
    "required": [
        "question",
        "options",
        "correct_index",
        "hint",
        "explanation"
    ]
}


# 문제 및 채점 상태 초기화
if "quiz" not in st.session_state:
    st.session_state.quiz = None
    st.session_state.quiz_id = 0
    st.session_state.quiz_topic = None
    st.session_state.show_hint = False
    st.session_state.show_answer = False


# 학습 주제 선택
topic = st.selectbox(
    "학습할 주제를 선택하세요.",
    ["OSS", "Git", "Python"]
)


# 새로운 문제 생성
if st.button("새 문제 생성", type="primary"):

    with st.spinner("AI가 문제를 생성하고 있습니다..."):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=(
                    f"주제: {topic}\n"
                    "대학교 1학년 수준의 객관식 문제를 "
                    "하나 만들어 주세요."
                ),
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    response_mime_type="application/json",
                    response_json_schema=QUIZ_SCHEMA
                )
            )

            quiz = json.loads(response.text)

            # 문제 형식 검사
            if (
                len(quiz["options"]) != 4
                or not 0 <= quiz["correct_index"] <= 3
            ):
                raise ValueError("문제 형식이 올바르지 않습니다.")

            # 문제 저장
            st.session_state.quiz = quiz
            st.session_state.quiz_topic = topic
            st.session_state.quiz_id += 1
            st.session_state.show_hint = False
            st.session_state.show_answer = False

        except Exception as e:
            st.error(f"문제 생성 오류: {type(e).__name__}: {e}")


# 현재 선택한 주제의 문제 출력
quiz = st.session_state.quiz

if quiz is not None and st.session_state.quiz_topic == topic:

    st.divider()
    st.subheader("📝 연습문제")

    st.write(quiz["question"])

    # 객관식 보기 출력
    choice = st.radio(
        "정답을 선택하세요.",
        options=range(4),
        format_func=lambda i: (
            f"{i + 1}. {quiz['options'][i]}"
        ),
        index=None,
        key=f"answer_{st.session_state.quiz_id}"
    )

    # 힌트 버튼
    if st.button("힌트 보기"):
        st.session_state.show_hint = True

    if st.session_state.show_hint:
        st.info(quiz["hint"])

    # 정답 확인 버튼
    if st.button("정답 확인"):
        if choice is None:
            st.warning("정답을 먼저 선택하세요.")
        else:
            st.session_state.show_answer = True
            if choice != quiz["correct_index"]:
                 save_wrong_question(quiz, choice)
    # Python으로 자동 채점
    if st.session_state.show_answer:

        correct = quiz["correct_index"]

        if choice == correct:
            st.success("정답입니다!")
        else:
            st.error("오답입니다.")

        st.write(
            "정답:",
            f"{correct + 1}. {quiz['options'][correct]}"
        )

        st.write("해설:", quiz["explanation"])

elif quiz is None:
    st.info("학습 주제를 선택하고 새 문제 생성을 눌러 주세요.")

else:
    st.info("변경한 주제의 새 문제를 생성해 주세요.")

st.divider()
show_wrong_note()