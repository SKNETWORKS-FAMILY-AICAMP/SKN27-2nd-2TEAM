import streamlit as st

def render_model():
    html_content = """
        <div class="page-header">
            <h2 class="page-title">
                ⚙️ 모델 정보
            </h2>
            <p class="page-description">
                모델에 대한 설명과 모델링 과정의 시각화 정보가 표시됩니다.
            </p>
        </div>
    """
    st.html(html_content)
    
    st.info("이곳에 모델 관련 상세 설명 및 시각화 데이터가 들어갈 예정입니다.")