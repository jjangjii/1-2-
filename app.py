import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="보건실 예약 앱", page_icon="🏥")

st.title("🏥 보건실 예약 시스템")

# 세션 상태 초기화
if "reservations" not in st.session_state:
    st.session_state.reservations = []

# 예약 입력 폼
with st.form("reservation_form"):
    st.subheader("예약하기")

    name = st.text_input("이름")
    student_id = st.text_input("학번")
    reason = st.selectbox(
        "방문 사유",
        ["두통", "복통", "감기", "상처 치료", "기타"]
    )

    visit_date = st.date_input("예약 날짜")
    visit_time = st.time_input("예약 시간")

    submit = st.form_submit_button("예약하기")

    if submit:
        if name and student_id:
            reservation = {
                "이름": name,
                "학번": student_id,
                "사유": reason,
                "날짜": str(visit_date),
                "시간": str(visit_time)
            }

            st.session_state.reservations.append(reservation)

            st.success("예약이 완료되었습니다!")
        else:
            st.error("이름과 학번을 입력하세요.")

# 예약 목록 표시
st.subheader("📋 예약 목록")

if st.session_state.reservations:
    df = pd.DataFrame(st.session_state.reservations)
    st.dataframe(df, use_container_width=True)
else:
    st.info("현재 예약이 없습니다.")
