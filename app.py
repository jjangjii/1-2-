import streamlit as st
from google import genai
from google.genai import types

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="보건실 이용 상담 챗봇",
    page_icon="🏥",
)

st.title("🏥 보건실 이용 상담 챗봇")

st.markdown(
    """
보건실 이용과 관련된 질문을 해보세요.

예시:
- 머리가 아픈데 보건실 가도 되나요?
- 체육시간에 다쳤어요.
- 약을 받을 수 있나요?
- 보건실 이용 절차가 궁금해요.
"""
)

# -----------------------------
# API 키 확인
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error(
        "GEMINI_API_KEY가 설정되지 않았습니다. "
        "Streamlit Secrets를 확인하세요."
    )
    st.stop()

# -----------------------------
# Gemini Client 생성
# -----------------------------
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 초기화 오류: {e}")
    st.stop()

# -----------------------------
# 채팅 기록 저장
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요. 보건실 이용 상담 챗봇입니다. "
                "보건실 이용 절차, 응급상황, 건강 관련 문의를 도와드릴게요."
            ),
        }
    ]

# -----------------------------
# 기존 대화 출력
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
prompt = st.chat_input("질문을 입력하세요")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # 이전 대화를 Gemini 형식으로 변환
            history_text = ""

            for msg in st.session_state.messages:
                speaker = (
                    "사용자"
                    if msg["role"] == "user"
                    else "상담봇"
                )
                history_text += f"{speaker}: {msg['content']}\n"

            system_prompt = """
당신은 학교 보건실 이용 안내 챗봇입니다.

규칙:
1. 학생이 이해하기 쉬운 한국어로 답변합니다.
2. 보건실 이용 절차를 친절하게 안내합니다.
3. 응급상황이 의심되면 즉시 교사, 보호자 또는 119 도움을 받도록 안내합니다.
4. 의료 진단을 확정하지 않습니다.
5. 답변은 간결하고 실용적으로 작성합니다.
"""

            full_prompt = f"""
{system_prompt}

대화 기록:
{history_text}

사용자 질문:
{prompt}
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=1000,
                ),
            )

            answer = response.text

            st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except Exception as e:
            error_msg = (
                f"오류가 발생했습니다.\n\n"
                f"오류 내용: {str(e)}"
            )

            st.error(error_msg)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_msg,
                }
            )

# -----------------------------
# 대화 초기화 버튼
# -----------------------------
st.sidebar.header("설정")

if st.sidebar.button("대화 초기화"):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요. 보건실 이용 상담 챗봇입니다. "
                "무엇을 도와드릴까요?"
            ),
        }
    ]
    st.rerun()
