import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os
from user_profile import display_user_profile
from utils.utils_function import load_progress_data, save_progress_data


st.title("Progress Tracking")

if "user" not in st.session_state:
    st.warning("Please log in to access the Progress Tracker.")
else:
    username = st.session_state.user
    name, age, weight, height = display_user_profile()

    # Load progress data for the current user
    if "progress_data" not in st.session_state:
        st.session_state.progress_data = load_progress_data(username)

    # Input form for progress data
    st.subheader("Log Your Progress")
    date = st.date_input("Date", datetime.now())
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
    body_fat = st.number_input("Body Fat %", min_value=0.0, max_value=100.0, step=0.1)
    muscle_mass = st.number_input("Muscle Mass (kg)", min_value=0.0, step=0.1)
    notes = st.text_area("Notes")

    if st.button("Save Progress"):
        new_data = pd.DataFrame(
            {
                "Date": [date],
                "Weight": [weight],
                "Body Fat %": [body_fat],
                "Muscle Mass": [muscle_mass],
                "Notes": [notes],
            }
        )
        st.session_state.progress_data = pd.concat(
            [st.session_state.progress_data, new_data], ignore_index=True
        )
        save_progress_data(username, st.session_state.progress_data)
        st.success("Progress saved successfully!")

    # Display progress data
    st.subheader("Your Progress")
    st.dataframe(st.session_state.progress_data)

    # Visualize progress
    st.subheader("Progress Visualization")
    if not st.session_state.progress_data.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(
            st.session_state.progress_data["Date"],
            st.session_state.progress_data["Weight"],
            label="Weight",
        )
        ax.plot(
            st.session_state.progress_data["Date"],
            st.session_state.progress_data["Body Fat %"],
            label="Body Fat %",
        )
        ax.plot(
            st.session_state.progress_data["Date"],
            st.session_state.progress_data["Muscle Mass"],
            label="Muscle Mass",
        )
        ax.legend()
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        ax.set_title("Progress Over Time")
        st.pyplot(fig)

    # Goal setting
    st.subheader("Set Goals")
    goal_type = st.selectbox("Goal Type", ["Weight", "Body Fat %", "Muscle Mass"])
    goal_value = st.number_input(f"Target {goal_type}", min_value=0.0, step=0.1)
    goal_date = st.date_input("Target Date", datetime.now())

    if st.button("Set Goal"):
        st.success(f"Goal set: Reach {goal_value} {goal_type} by {goal_date}")

    # Progress analysis
    if st.button("Analyze Progress"):
        from utils.llm_handler import get_response_from_llm

        progress_summary = st.session_state.progress_data.to_string()
        analysis = get_response_from_llm(
            f"Analyze this fitness progress data and provide insights:\n{progress_summary}"
        )
        st.write(analysis)
