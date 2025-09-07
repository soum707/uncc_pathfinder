import streamlit as st

industries = [
    "Technology",
    "Healthcare",
    "Finance",
    "Education",
    "Manufacturing",
    "Retail",
    "Energy",
    "Transportation",
    "Entertainment",
    "Agriculture",
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
        pointer-events: auto;
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

    /* Tiles grid */
    #tiles {
        position: absolute;
        inset: 0;
        top: 15vh;               /* leaves space for the moved header + subheading */
        box-sizing: border-box;
        padding: 2vh 5vw 5vh;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 14px;
        opacity: 0;              /* hidden until click */
        pointer-events: none;
    }
    /* Show tiles after click */
    #go:checked ~ #tiles {
        opacity: 1;
        pointer-events: auto;
        animation: fade-in 0.8s ease 5.4s both; /* after header moves + subheading fades */
        z-index: 1;
    }
    /* Individual tile */
    .tile {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 14px 12px;
        border-radius: 10px;
        border: 1px solid rgba(0,0,0,0.15);
        background: rgba(255,255,255,0.75);
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        cursor: pointer;
        user-select: none;
        transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease, background .12s ease;
    }
    .tile:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(0,0,0,0.08); }

    /* Use checkbox to track selection */
    .tile input { display: none; }
    .tile span { display: block; }
    .tile input:checked + span {
        background: rgba(76, 175, 80, 0.10);
        border: 1px solid rgba(76, 175, 80, 0.45);
        box-shadow: 0 0 0 2px rgba(76,175,80,0.15) inset;
        border-radius: 8px;
        padding: 4px 2px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Build tiles HTML
tiles_html = "\n".join([
    f'<label class="tile"><input type="checkbox" name="industry" value="{name}"><span>{name}</span></label>'
    for name in industries
])

# Show animated text
st.markdown(
    f'''
    <div id="anim-root">
      <input type="checkbox" id="go" class="screen-toggle">
      <label for="go" class="click-overlay" aria-label="Click to continue"></label>
      <div id="anim-container" class="centered-text">Let\'s get started</div>
      <div id="next-text">What are you into?</div>
      <div id="sub-heading">Choose an area of interest to begin</div>
      <div id="tiles">{tiles_html}</div>
    </div>
    ''',
    unsafe_allow_html=True
)