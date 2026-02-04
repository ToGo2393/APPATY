import streamlit as st

def inject_custom_css():
    """Inject CSS for mobile responsiveness and touch-friendly targets."""
    st.markdown("""
    <style>
        /* Mobile: Vertical Stacking & Larger Touch Targets */
        @media (max-width: 600px) {
            /* Force columns to stack */
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 auto !important;
                min-width: 100% !important;
            }
            
            /* Responsive Font Sizes */
            h1 { font-size: 1.8rem !important; }
            h2 { font-size: 1.5rem !important; }
            h3 { font-size: 1.3rem !important; }
            
            /* LaTeX Adjustment */
            .katex { font-size: 0.9em !important; }
        }

        /* Touch Targets (48px min-height) */
        .stButton > button {
            min_height: 48px;
            font-size: 16px;
        }
        .stSelectbox div[data-baseweb="select"] > div {
            min-height: 48px;
        }
        .stTextInput input, .stNumberInput input {
            min-height: 48px;
        }
        
        /* Mobile Logo Styling */
        .mobile-logo {
            text-align: center;
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #4CAF50; /* Example Brand Color */
            display: none;
        }
        @media (max-width: 600px) {
            .mobile-logo { display: block; }
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
