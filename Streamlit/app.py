import streamlit as st

# Getting Started
st.markdown(
    """
    <style>
    .centered-text {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 70vh;
        font-size: 2em;
        font-weight: bold;
        animation: slide-in-bottom 1s ease-out 0s both;
    }
    .slide-out {
        animation: slide-out-top 2s ease-out forwards;
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
        animation: slide-out-top 2s ease-out forwards;
    }
    /* Hide the overlay once clicked */
    #go:checked + label.click-overlay { display: none; }
    </style>
    """,
    unsafe_allow_html=True
)

# Show animated text
st.markdown(
    '''
    <div id="anim-root">
      <input type="checkbox" id="go" class="screen-toggle">
      <label for="go" class="click-overlay" aria-label="Click to continue"></label>
      <div id="anim-container" class="centered-text">Let\'s get started</div>
    </div>
    ''',
    unsafe_allow_html=True
)