import streamlit as st

industries = [

    "Manufacturing",
    "Industrial Engineering",
    "Technology",
    "Healthcare & Medical Services",
    "Education & Training",
    "Finance & Banking",
    "Insurance",
    "Retail & E-commerce",
    "Hospitality & Tourism",
    "Transportation & Logistics",
    "Real Estate",
    "Legal Services",
    "Media & Entertainment",
    "Telecommunications",
    "Public Services & Government",
    "Defense & Security",
    "Professional Services",

    # Quaternary Industries
    "Research & Development",
    "Information Services",
    "Data Science & Analytics",
    "Artificial Intelligence & Machine Learning",
    "Biotechnology",
    "Environmental Science & Sustainability",
    "Consulting Services"
]

# Getting Started
st.markdown(
    """
    <style>
    #anim-root { position: relative; height: 80vh; overflow: hidden; }
    html, body, .stApp { height: 98%; overflow: hidden; }
    .main .block-container { padding-top: 0; padding-bottom: 0; }
    .centered-text {
        position: absolute;
        inset: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 2em;
        font-weight: bold;
        z-index: 1;
        animation: slide-in-bottom 2s ease-out 0s both;
    }
    .slide-out {
        animation: slide-out-top 2s ease-out 2s forwards;
    }
    @keyframes slide-in-bottom {
        0% {
            transform: translateY(1000px);
            opacity: 0;
        }
        100% {
            transform: translateY(0);
            opacity: 1;
        }
    }
    @keyframes slide-out-top {
        0% {
            transform: translateY(0);
            opacity: 1;
        }
        100% {
            transform: translateY(-1000px);
            opacity: 0;
         }
    }
    @keyframes move-to-top {
        0%   { transform: translateY(0); }
        100% { transform: translateY(-35vh); }
    }
    .screen-toggle { display: none; }
    .click-overlay {
        position: fixed;
        inset: 0;
        cursor: pointer;
        z-index: 5;
        background: transparent;
    }
    /* When clicked, trigger the slide-out animation */
    #go:checked ~ #anim-container {
        animation: slide-out-top 3s ease-out forwards;
    }
    /* Hide the overlay once clicked */
    #go:checked + label.click-overlay { display: none; }
    #next-text {
        position: absolute;
        inset: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.8em;
        font-weight: bold;
        z-index: 1;
        /* Start off-screen (bottom) and invisible until click */
        opacity: 0;
        transform: translateY(1000px);
        pointer-events: none;
    }
    #go:checked ~ #next-text {
        animation: 
            slide-in-bottom 3s 0.2s both,
            move-to-top 1s ease-out 4s forwards;
        pointer-events: none;
        z-index: 2;
    }
    #sub-heading {
        position: absolute;
        top: 8vh;
        width: 100%;
        text-align: center;
        font-size: 1.2em;
        font-weight: normal;
        opacity: 0;
        pointer-events: none;
    }
    #go:checked ~ #sub-heading {
        animation: fade-in 1.2s cubic-bezier(0.390, 0.575, 0.565, 1.000) 5.4s both;
        pointer-events: auto;
        z-index: 2;
    }
    @keyframes fade-in {
      0% { opacity: 0; }
      100% { opacity: 1; }
    }

    /* Style Streamlit-native checkboxes as tiles */
    .stApp [data-testid="stVerticalBlock"]:has(#tiles-start) [data-testid="stCheckbox"] {
        border: 1px solid rgba(0,0,0,0.15);
        border-radius: 10px;
        padding: 14px 12px;
        background: rgba(255,255,255,0.75);
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease, background .12s ease;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        transform: translateY(-620px);
    }
    
    .stApp [data-testid="stVerticalBlock"]:has(#tiles-start) [data-testid="stCheckbox"] label {
        width: 100%;
        display: flex;
        justify-content: center;
    }
    .stApp [data-testid="stVerticalBlock"]:has(#tiles-start) [data-testid="stCheckbox"]:hover {
        transform: translateY(-620px) scale(1.03);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-color: rgba(0,0,0,0.25);
        background: rgba(255,255,255,0.85);
        cursor: pointer;
    }
    .stApp [data-testid="stVerticalBlock"]:has(#tiles-start) [data-testid="stCheckbox"]:has(input:checked) {
        outline: 2px solid rgba(76,175,80,0.45);
        outline-offset: 2px;
        border-radius: 8px;
    }

    /* --- Fade-in control for native Streamlit checkboxes (tiles) --- */
    /* Hide tiles by default */
    [data-testid="stCheckbox"] {
        opacity: 0;
        pointer-events: none;
    }
    /* When the hidden #go checkbox is checked, fade tiles in */
    .stApp:has(#go:checked) [data-testid="stCheckbox"] {
        animation: fade-in 0.8s cubic-bezier(0.390, 0.575, 0.565, 1.000) 5.4s both;
        pointer-events: auto;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '''
    <div id="anim-root">
      <input type="checkbox" id="go" class="screen-toggle">
      <label for="go" class="click-overlay" aria-label="Click to continue"></label>
      <div id="anim-container" class="centered-text">Let\'s get started</div>
      <div id="next-text">What are you into?</div>
      <div id="sub-heading">Choose an area of interest to begin</div>
      <div id="tiles-start"></div>
    ''',
    unsafe_allow_html=True
)

# Initialize selection state
if 'industries_selected' not in st.session_state:
    st.session_state['industries_selected'] = []

# Render tiles as native checkboxes in a grid
NUM_COLS = 4
cols = st.columns(NUM_COLS)
for i, name in enumerate(industries):
    with cols[i % NUM_COLS]:
        checked = st.checkbox(name, key=f"industry_{i}")

# Collect selections into session state
selected = [name for i, name in enumerate(industries) if st.session_state.get(f"industry_{i}")]
st.session_state['industries_selected'] = selected

st.markdown(
    '''
    </div>
    ''',
    unsafe_allow_html=True
)