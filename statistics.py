import csv
import io
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


# CSV 파일 변환 (엑셀 한글 깨짐 방지 utf-8-sig 적용)
def convert_history_to_csv(history, stats):
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["[최종 통계 요약]"])
    writer.writerow(["총 문제 수", "정답 수", "오답 수", "정답률(%)"])
    writer.writerow([stats["total"], stats["correct"], stats["wrong"], f"{stats['accuracy']}%"])
    writer.writerow([])

    if history:
        headers = ["번호", "주제", "난이도", "문제", "선택한 답", "정답", "정답 여부", "해설"]
        writer.writerow(headers)
        for row in history:
            writer.writerow([row.get(h, "") for h in headers])

    return output.getvalue().encode("utf-8-sig")


# 최종 결과 화면 및 CSV 다운로드 버튼 출력
def show_statistics(total_count, correct_count):
    init_statistics()
    stats = calculate_statistics(total_count, correct_count)

    st.divider()
    st.subheader("📊 퀴즈 최종 결과 및 통계")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("총 문제 수", f"{stats['total']}문제")
    col2.metric("정답 수", f"{stats['correct']}개")
    col3.metric("오답 수", f"{stats['wrong']}개")
    col4.metric("정답률", f"{stats['accuracy']}%")

    history = st.session_state.quiz_history
    if history:
        st.write("### 📝 문제별 풀이 요약")
        st.dataframe(
            history,
            column_order=("번호", "주제", "난이도", "문제", "선택한 답", "정답", "정답 여부"),
            use_container_width=True,
            hide_index=True
        )

    csv_bytes = convert_history_to_csv(history, stats)
    st.download_button(
        label="📥 결과 및 통계 CSV 다운로드",
        data=csv_bytes,
        file_name="dcu_oss_quiz_result.csv",
        mime="text/csv",
        use_container_width=True
    )