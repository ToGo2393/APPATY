import streamlit as st

def inject_custom_css():
    """Inject CSS for mobile responsiveness and touch-friendly targets."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Roboto:wght@400;500&display=swap');

        /* Global Theme: Deep Midnight Blue */
        .stApp {
            background-color: #0A0E1A;
            font-family: 'Inter', sans-serif;
        }

        /* Typography */
        h1, h2, h3, h4, h5, h6, p, div, span, label {
            color: #E2E8F0 !important;
        }

        /* Primary Buttons */
        .stButton > button {
            background-color: #1D63FF !important;
            color: white !important;
            border: none;
            border-radius: 8px;
            min-height: 48px; /* Touch target */
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .stButton > button:hover {
            background-color: #3B75FF !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(29, 99, 255, 0.3);
        }
        .stButton > button:active {
            transform: translateY(0);
        }

        /* Input Fields */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
            background-color: #171F2E !important;
            border: 1px solid #1F2937 !important;
            border-radius: 12px !important;
            color: #E2E8F0 !important;
            min-height: 48px; /* Touch target */
        }
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: #1D63FF !important;
            box-shadow: 0 0 0 2px rgba(29, 99, 255, 0.2) !important;
        }

        /* Mobile Layout Optimizations */
        @media (max-width: 600px) {
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 auto !important;
                min-width: 100% !important;
            }
            .stButton > button {
                width: 100% !important;
            }
        }
        
        /* Sidebar Navigation Drawer Feel */
        [data-testid="stSidebar"] {
            background-color: #0F1423;
            border-right: 1px solid #1F2937;
        }

        /* --- VISIBILITY FIXES --- */
        /* Global Text and Headers */
        html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, label {
            color: #E0E0E0 !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #FFFFFF !important;
        }

        /* Selectbox Styling - Main View */
        div[data-baseweb="select"] > div {
            color: white !important; 
            background-color: #171F2E !important;
        }

        /* Dropdown menu options visibility */
        div[data-baseweb="popover"] li, div[data-baseweb="popover"] div {
            color: #111827 !important; /* Dark text for light dropdown background provided by browser/streamlit defaults */
        }
        
        /* Ensure specific widget labels are visible */
        .stNumberInput label, .stSelectbox label, .stTextInput label {
            color: #E2E8F0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

def inject_pwa_meta():
    """Inject Meta tags for PWA support."""
    meta_tags = """
    <!-- Mobile Web App Capable -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#0E1117">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    
    <!-- Title -->
    <meta name="apple-mobile-web-app-title" content="APPATY">
    
    <!-- Link to Manifest -->
    <link rel="manifest" href="static/manifest.json">
    """
    st.markdown(meta_tags, unsafe_allow_html=True)

def inject_haptics():
    """Inject JS for haptic feedback mockup."""
    js = """
    <script>
        // Haptic Feedback Mockup
        const vibrate = () => {
            if (navigator.vibrate) {
                navigator.vibrate(50); // 50ms vibration
            }
        };
        
        // Attach to all buttons once loaded
        document.addEventListener('DOMContentLoaded', () => {
            const buttons = document.querySelectorAll('button');
            buttons.forEach(btn => {
                btn.addEventListener('click', vibrate);
            });
        });
    </script>
    """
    # Streamlit html component might be needed for script execution if markdown doesn't persist
    # But for simple p.o.c markdown often works or st.components.v1.html
    st.components.v1.html(js, height=0, width=0)

def inject_auto_select_js():
    """Inject JS to auto-select input text on focus."""
    js = """
    <script>
    // Auto-select text in number inputs on focus
    const observeInputs = () => {
        const inputs = window.parent.document.querySelectorAll('input[type="number"]');
        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                input.select();
            });
        });
    };
    
    // Initial run
    observeInputs();
    
    // Re-run on DOM changes (Streamlit updates)
    const observer = new MutationObserver(observeInputs);
    observer.observe(window.parent.document.body, { childList: true, subtree: true });
    </script>
    """
    st.components.v1.html(js, height=0, width=0)
