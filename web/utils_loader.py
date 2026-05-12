import time
import streamlit as st


def mostrar_loader(segundos=1):
    loader = st.empty()

    loader.markdown("""
    <style>
    .loader-screen {
        position: fixed;
        inset: 0;
        background: #000000;
        z-index: 999999;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }

    .loader-logo {
        color: white;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: 4px;
        font-family: "Century Gothic", "Montserrat", "Segoe UI", Arial, sans-serif;
        text-shadow: 0 0 20px rgba(255,255,255,0.35);
    }

    .loader-dots::after {
        content: "";
        animation: dots 1.2s infinite;
    }

    @keyframes dots {
        0% { content: ""; }
        25% { content: "."; }
        50% { content: ". ."; }
        75% { content: ". . ."; }
        100% { content: ""; }
    }

    .loader-text {
        margin-top: 14px;
        color: rgba(255,255,255,0.65);
        font-size: 14px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    </style>

    <div class="loader-screen">
        <div class="loader-logo">NOVA MUSIC★<span class="loader-dots"></span></div>
        <div class="loader-text">Cargando página</div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(segundos)
    return loader