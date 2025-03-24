import streamlit as st
from openai import OpenAI

def get_system_message(feedback_style: str) -> str:
    system_messages = {
        "MILD": """
        당신은 따뜻하고 긍정적인 글쓰기 멘토입니다. 작성자의 노력과 창의성을 진심으로 칭찬하고, 그들의 잠재력을 이끌어내는 것이 주된 역할입니다.
        
        글을 읽고 다음과 같은 방식으로 피드백을 제공해주세요:
        - 글의 독특하고 인상적인 부분을 구체적으로 언급하며 진심 어린 칭찬
        - 작성자의 노력과 성장 가능성을 적극적으로 인정
        - 작성자가 자신감을 가질 수 있도록 따뜻한 격려의 말 포함
        - 개선점은 최소화하고 긍정적인 제안 형태로 부드럽게 표현
        - 작성자의 다음 글이 기대된다는 응원의 메시지로 마무리
        - 3-4줄의 간단하고 따뜻한 톤의 피드백
        서문이나 넘버링 없이, 바로 진심 어린 칭찬과 격려 위주의 피드백을 작성해주세요.
        """,
        
        "HOT": """
        당신은 따뜻하고 건설적인 글쓰기 멘토입니다. 작성자의 노력을 인정하고 격려하면서도, 더 나은 방향으로 발전할 수 있도록 도와주는 역할을 합니다.

        글을 읽고 다음과 같은 방식으로 피드백을 제공해주세요:
        - 작성자의 관점과 의도를 이해하고 공감하는 따뜻한 피드백
        - 개선점을 제안할 때는 부드럽고 건설적인 표현 사용
        - 글의 장점을 먼저 언급한 후 보완할 점 제시
        - 3-4줄의 간단명료한 피드백
        - 작성자를 존중하는 격려의 말로 마무리

        서문이나 넘버링 없이, 바로 피드백 내용만 따뜻한 어조로 작성해주세요.
        """,

        "FIRE": """
        당신은 날카로운 통찰력을 지닌 글쓰기 멘토입니다. 건설적이면서도 명확한 개선점을 제시합니다.

        다음 기준으로 3-4줄의 간단명료한 피드백을 제공해주세요:
        - 글의 주요 문제점을 명확하게 지적
        - 구체적인 개선 방향 제시
        - 글의 잠재력을 끌어올릴 수 있는 도전 과제 제안
        - 객관적이고 직설적인 어조 유지
        서문이나 넘버링 없이, 피드백 내용만 간단히 작성해주세요. 
        """,
        
        "DIABLO": """
        당신은 직설적이고 명확한 글쓰기 멘토입니다. 불필요한 미화 없이 핵심적인 개선점을 지적하되, 건설적인 방향을 제시합니다.

        글을 읽고 다음과 같은 방식으로 피드백을 제공해주세요:
        - 핵심적인 문제점을 직접적으로 지적
        - 구체적인 개선 방향 제시
        - 불필요한 칭찬은 배제하고 실질적인 조언에 집중
        - 3-4줄의 간단명료한 피드백
        - 실행 가능한 구체적 개선 제안으로 마무리
        서문이나 넘버링 없이, 바로 피드백 내용만 직설적인 어조로 작성해주세요.
        """
    }
    return system_messages[feedback_style]

def get_feedback_message(blog: str) -> str:
    return f"""
    우선, Blog를 읽으세요. <blog>{blog}</blog> 
    다음, 평가 기준 <guideline>을 참고하여 제출된 글에 대한 피드백을 생각하세요.

    <guideline>
    1. 구조적 완성도
    - 서론/본론/결론의 명확한 구조
    - 서론: 글의 요약, 독자 타겟팅, 기대효과, 작성 동기 포함
    - 본론: 문제 상황 → 원인 분석 → 해결 과정의 자연스러운 흐름
    - 결론: 내용 요약, 효과, 한계점 제시

    2. 내용의 독창성과 전문성
    - 개인적 경험과 관점의 반영도
    - 주제에 대한 독자적 해석과 통찰
    - 배경지식 설명의 적절성
    - 단순 정보 나열이 아닌 개인의 관점 제시
    - 독자의 이해를 돕는 예시/비유 활용

    3. 가독성과 표현력
    - 문단 구분과 여백의 적절성
    - 폰트, 자간, 강조의 일관성
    - 이미지와 코드의 적절한 배치
    - 오타 및 문법적 오류
    - 적절한 길이와 문장력

    4. 독자 친화성
    - 첫 문장의 흥미 유발도
    - 전문용어에 대한 적절한 설명
    - 글의 흐름과 연결성
    - 적절한 유머와 이모지 활용
    - 독자와의 소통을 고려한 문체
    </guideline>
    """

def get_openai_feedback(api_key: str, base_url: str, model: str, blog_text: str, feedback_style: str) -> str:
    # OpenAI 클라이언트 설정
    client_params = {"api_key": api_key}
    if base_url:  # base_url이 입력된 경우에만 추가
        client_params["base_url"] = base_url
    
    client = OpenAI(**client_params)
    
    try:
        system_message = get_system_message(feedback_style)
        user_message = get_feedback_message(blog_text)
        
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1024,
            temperature=0.2,
            top_p=0.9
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating feedback: {str(e)}"

def main():
    st.set_page_config(page_title="글또 피드백 생성기", page_icon="📝", layout="wide")
    
    st.title("📝 글또 피드백 생성기")
    st.markdown("---")

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ 설정")
        api_key = st.text_input("API Key", type="password")
        base_url = st.text_input(
            "Base URL (선택사항)",
            placeholder="예: https://api.openai.com/v1 (OpenAI 사용시 비워두세요)",
            help="OpenAI 호환 API를 사용할 경우 Base URL을 입력하세요. OpenAI 사용시에는 비워두세요."
        )
        model = st.text_input(
            "모델명",
            placeholder="예: gpt-4, gpt-3.5-turbo, anthropic.claude-3-sonnet-20240229-v1:0",
            help="사용하고자 하는 모델명을 입력하세요"
        )
        
        # 피드백 스타일 선택 옵션 변경
        style_mapping = {
            "🌱 순한맛": "MILD",
            "🧄 보통맛": "HOT",
            "🌶️ 매운맛": "FIRE",
            "☠️ 지옥맛": "DIABLO"
        }
        
        selected_style = st.selectbox(
            "피드백 스타일",
            list(style_mapping.keys()),
            index=0
        )
        feedback_style = style_mapping[selected_style]

    # Main content area
    st.header("📄 블로그 글 입력")
    blog_text = st.text_area("피드백을 받고 싶은 글을 입력하세요", height=300)

    if st.button("피드백 생성", type="primary"):
        if not api_key:
            st.error("API Key를 입력해주세요!")
            return
        
        if not model:
            st.error("모델명을 입력해주세요!")
            return
        
        if not blog_text:
            st.error("블로그 글을 입력해주세요!")
            return

        with st.spinner("피드백을 생성하고 있습니다..."):
            feedback = get_openai_feedback(api_key, base_url, model, blog_text, feedback_style)
            
            st.header("💬 생성된 피드백")
            st.markdown(feedback)

if __name__ == "__main__":
    main()
