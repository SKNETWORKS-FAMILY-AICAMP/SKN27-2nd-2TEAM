import streamlit as st
from src.utils.data_loader import load_ui_config

def render_model():
    ui_config = load_ui_config()
    model_config = ui_config["model"]
    header_config = model_config["header"]

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
    
    st.info(model_config["info"])