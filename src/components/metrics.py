import streamlit as st

def render_metric_card(icon_name, icon_style_class, title, value, change_text, is_positive=True, emoji=""):
    """
    KPI 지표 카드 컴포넌트 렌더링
    
    Args:
        icon_name (str): Material symbol icon name
        icon_style_class (str): CSS class for icon background (primary, secondary, orange, tertiary)
        title (str): Card title
        value (str): Main metric value
        change_text (str): Percentage change text (e.g., "+12.5%")
        is_positive (bool): True for positive change, False for negative
        emoji (str): Optional emoji appended to the value
    """
    change_class = "positive" if is_positive else "negative"
    
    html_content = f"""
        <div class="metric-card h-full">
            <div class="metric-card-header">
                <span class="icon-badge {icon_style_class}">
                    <span class="material-symbols-outlined">{icon_name}</span>
                </span>
                <span class="change-tag {change_class}">{change_text}</span>
            </div>
            <div>
                <p class="metric-card-title">{title}</p>
                <p class="metric-card-value">{value} <span class="metric-card-emoji">{emoji}</span></p>
            </div>
        </div>
    """
    st.html(html_content)

def render_metrics_row():
    """
    상단 4개의 KPI 지표 카드를 나란히 렌더링합니다.
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card(
            icon_name="groups", 
            icon_style_class="primary", 
            title="Total Customers", 
            value="12,845", 
            change_text="+12.5%", 
            is_positive=True, 
            emoji="👥"
        )
    with col2:
        render_metric_card(
            icon_name="bolt", 
            icon_style_class="secondary", 
            title="Active Users", 
            value="4,231", 
            change_text="+8.2%", 
            is_positive=True, 
            emoji="📈"
        )
    with col3:
        render_metric_card(
            icon_name="person_off", 
            icon_style_class="orange", 
            title="Churn Rate", 
            value="3.4%", 
            change_text="-2.1%", 
            is_positive=False, 
            emoji="📉"
        )
    with col4:
        render_metric_card(
            icon_name="payments", 
            icon_style_class="tertiary", 
            title="Revenue", 
            value="$248k", 
            change_text="+15.7%", 
            is_positive=True, 
            emoji="💰"
        )