import streamlit as st
from user_profile import display_user_profile
from utils.llm_handler import get_response_from_llm


st.title("Virtual Trainer")


if "user" not in st.session_state:
    st.warning("Please log in to access your Personalized Workout.")
else:

    name, age, weight, height = display_user_profile()

    # User's current status
    st.subheader("Your Current Status")
    mood = st.select_slider(
        "How are you feeling today?",
        options=["Terrible", "Bad", "Okay", "Good", "Great"],
    )
    energy = st.select_slider(
        "Energy level", options=["Very Low", "Low", "Medium", "High", "Very High"]
    )
    soreness = st.multiselect(
        "Any sore body parts?",
        ["None", "Arms", "Legs", "Back", "Chest", "Shoulders", "Core"],
    )

    # Workout preferences
    st.subheader("Today's Workout Preferences")
    duration = st.slider("Available time (minutes)", 15, 120, 45, step=5)
    intensity = st.select_slider(
        "Preferred intensity",
        options=["Very Low", "Low", "Medium", "High", "Very High"],
    )
    focus = st.selectbox(
        "What would you like to focus on?",
        ["Strength", "Cardio", "Flexibility", "Recovery"],
    )

    if st.button("Get Personalized Workout"):
        workout_input = f"""Create a personalized {duration}-minute {focus.lower()} workout.
        User is feeling {mood.lower()} with {energy.lower()} energy.
        Sore body parts: {', '.join(soreness) if soreness != ['None'] else 'None'}.
        Preferred intensity: {intensity}.
        Include warm-up, main exercises, and cool-down."""

        personalized_workout = get_response_from_llm(workout_input)
        st.subheader("Your Personalized Workout")
        st.write(personalized_workout)

    # Exercise form check
    st.subheader("Exercise Form Check")
    exercise = st.text_input("Enter an exercise name")
    if exercise and st.button("Get Form Tips"):
        form_tips = get_response_from_llm(
            f"Provide detailed form tips for performing {exercise} correctly and safely."
        )
        st.write(form_tips)

    # Injury prevention advice
    st.subheader("Injury Prevention")
    activity = st.text_input("Enter a fitness activity")
    if activity and st.button("Get Injury Prevention Tips"):
        prevention_tips = get_response_from_llm(
            f"Provide injury prevention tips for {activity}."
        )
        st.write(prevention_tips)

    # Recovery advice
    st.subheader("Recovery Advice")
    if st.button("Get Recovery Tips"):
        recovery_tips = get_response_from_llm(
            "Provide general tips for optimal workout recovery and muscle repair."
        )
        st.write(recovery_tips)
