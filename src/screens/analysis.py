import streamlit as st
from src.utils.data_loader import load_ui_config

def render_analysis():
    ui_config = load_ui_config()
    analysis_config = ui_config["analysis"]
    header_config = analysis_config["header"]
    selection_config = analysis_config["customer_selection"]

    html_content = f"""
        <div class="page-header">
            <h2 class="page-title">
                {header_config['title']}
            </h2>
            <p class="page-description">
                {header_config['description']}
            </p>
        </div>
    """
    st.html(html_content)
    
    st.markdown("### 고객 데이터 선택")
    
    # 드롭다운 목업 구현
    customer_options = selection_config["options"]
    
    selected_customer = st.selectbox(
        selection_config["label"],
        options=customer_options,
        index=0,
        help=selection_config["help"]
    )
    
    st.markdown("---")
    
    customer_name = selected_customer.split(' -')[0]
    info_message = analysis_config["info_template"].format(customer=customer_name)
    st.info(info_message)