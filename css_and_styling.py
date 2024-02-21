import streamlit as st

def add_custom_css():

    custom_css = """
    <style>

    @keyframes bounce {
        10%, 11%, 14% {
            transform: translateY(0);
        }
        12% {
            transform: translateY(-20px);
        }
        13% {
            transform: translateY(-10px);
        }
    }

    button[kind="primary"] {
        color: #216a82;
        border-color: #216a82;
        width: 50%;   /* Increase button width */
        height: 50px;   /* Increase button height */
        font-size: 20px; /* Increase font size */
        animation: bounce 10s infinite; /* Add bouncing animation */
    }
    
    </style>
    """

    # Inject custom CSS with markdown
    st.markdown(custom_css, unsafe_allow_html=True)