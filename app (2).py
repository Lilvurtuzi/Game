
import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from sympy.abc import x
from streamlit.components.v1 import html
from utils import generate_function, get_features, graph_function
from leaderboard import load_leaderboard, save_leaderboard

st.set_page_config(page_title="Rational Function Rumble", layout="centered")
LEADERBOARD_FILE = "leaderboard.csv"

st.title("🎮 Rational Function Rumble")
player = st.text_input("Enter your name:", "")
difficulty = st.selectbox("Choose difficulty level:", ["Easy", "Medium", "Hard"])

if player:
    challenge_expr = generate_function(difficulty)
    st.write(f"**Challenge Rational Function:** `{sp.pretty(challenge_expr)}`")
    graph_function(challenge_expr)
    st.warning("⏱️ You have 30 seconds to answer below!")

    start_time = time.time()

    with st.form("challenge_form"):
        x_guess = st.text_input("X-intercepts (comma separated):")
        y_guess = st.text_input("Y-intercept:")
        holes_guess = st.text_input("Holes (e.g., -1,2):")
        asymptotes_guess = st.text_input("Vertical Asymptotes (comma separated):")
        submit_btn = st.form_submit_button("Submit Answers")

    time_elapsed = time.time() - start_time

    if submit_btn:
        if time_elapsed > 30:
            st.error("⏰ Time’s up! You scored 0.")
            html("<audio autoplay><source src='https://www.soundjay.com/button/beep-10.mp3'></audio>", height=0)
            score = 0
        else:
            actual = get_features(challenge_expr)

            def parse_list(text):
                try:
                    return sorted([float(i.strip()) for i in text.split(",") if i.strip()])
                except:
                    return []

            score = 0
            user_x = parse_list(x_guess)
            user_asymptotes = parse_list(asymptotes_guess)

            if set(np.round(user_x, 1)) == set(np.round(actual["x_intercepts"], 1)):
                score += 30
            if np.isclose(float(y_guess), actual["y_intercept"], atol=1):
                score += 20
            if set(np.round(user_asymptotes, 1)) == set(np.round(actual["asymptotes"], 1)):
                score += 30
            if holes_guess:
                score += 10

            st.metric("Your Score", score)

            if score >= 70:
                st.success("🎉 Great job!")
                html("""<script>document.body.innerHTML += `<canvas id='confetti'></canvas>`;</script>
                       <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
                       <script>confetti()</script>""", height=0)
                html(f"<audio autoplay><source src='https://www.soundjay.com/button/beep-07.mp3'></audio>", height=0)
            else:
                st.info("Good effort!")
                html(f"<audio autoplay><source src='https://www.soundjay.com/button/beep-01a.mp3'></audio>", height=0)

        if st.button("Save Score"):
            df = load_leaderboard()
            df.loc[len(df)] = [player, score]
            save_leaderboard(df)
            st.success("Saved!")

st.subheader("🏆 Leaderboard")
df = load_leaderboard()
if not df.empty:
    st.dataframe(df.sort_values(by="Score", ascending=False))
