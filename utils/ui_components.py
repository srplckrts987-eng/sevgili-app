import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        /* Minimalist and flat design overrides */
        .stButton>button {
            border-radius: 8px;
            border: None;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 10px;
        }
        .timeline-item {
            border-left: 3px solid #ff4b4b;
            padding-left: 15px;
            margin-bottom: 20px;
            position: relative;
        }
        .timeline-item::before {
            content: '';
            position: absolute;
            left: -9px;
            top: 0;
            width: 15px;
            height: 15px;
            background-color: #ff4b4b;
            border-radius: 50%;
        }
        .timeline-date {
            font-weight: bold;
            color: #666;
            font-size: 0.9em;
        }
        .timeline-content {
            font-size: 1.1em;
            color: #333;
        }
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
        }
    </style>
    """, unsafe_allow_html=True)

def render_metric_card(title, value, subtitle=""):
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="margin:0; color:#555;">{title}</h4>
        <h2 style="margin:10px 0; color:#ff4b4b;">{value}</h2>
        <p style="margin:0; color:#888; font-size:0.9em;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_timeline_item(date_str, content):
    st.markdown(f"""
    <div class="timeline-item">
        <div class="timeline-date">{date_str}</div>
        <div class="timeline-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)
