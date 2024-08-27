# user_profile.py

import streamlit as st
import json
import os

USER_PROFILES_FILE = "data/user_profiles.json"

def load_user_profile(username):
    if os.path.exists(USER_PROFILES_FILE):
        with open(USER_PROFILES_FILE, "r") as f:
            all_profiles = json.load(f)
            return all_profiles.get(username, {})
    return {}

def save_user_profile(username, data):
    all_profiles = {}
    if os.path.exists(USER_PROFILES_FILE):
        with open(USER_PROFILES_FILE, "r") as f:
            all_profiles = json.load(f)
    
    all_profiles[username] = data
    
    with open(USER_PROFILES_FILE, "w") as f:
        json.dump(all_profiles, f)

def display_user_profile():
    st.sidebar.header("User Profile")

    # Check if user is logged in
    if "user" not in st.session_state:
        st.sidebar.warning("Please log in to access your profile.")
        return None, None, None, None

    username = st.session_state.user
    user_profile = load_user_profile(username)

    # Use session state to persist user data across pages
    if "name" not in st.session_state:
        st.session_state.name = user_profile.get("name", "")
    if "age" not in st.session_state:
        st.session_state.age = user_profile.get("age", 25)
    if "weight" not in st.session_state:
        st.session_state.weight = user_profile.get("weight", 70.0)
    if "height" not in st.session_state:
        st.session_state.height = user_profile.get("height", 170.0)

    st.session_state.name = st.sidebar.text_input(
        "Your Name", value=st.session_state.name
    )
    st.session_state.age = st.sidebar.number_input(
        "Your Age", min_value=1, max_value=120, value=st.session_state.age
    )
    st.session_state.weight = st.sidebar.number_input(
        "Your Weight (kg)", min_value=1.0, value=st.session_state.weight
    )
    st.session_state.height = st.sidebar.number_input(
        "Your Height (cm)", min_value=1.0, value=st.session_state.height
    )

    # Calculate BMI
    if st.session_state.weight > 0 and st.session_state.height > 0:
        bmi = st.session_state.weight / ((st.session_state.height / 100) ** 2)
        st.sidebar.write(f"Your BMI: {bmi:.2f}")

    # Save user profile
    if st.sidebar.button("Save Profile"):
        user_profile = {
            "name": st.session_state.name,
            "age": st.session_state.age,
            "weight": st.session_state.weight,
            "height": st.session_state.height
        }
        save_user_profile(username, user_profile)
        st.sidebar.success("Profile saved successfully!")

    return (
        st.session_state.name,
        st.session_state.age,
        st.session_state.weight,
        st.session_state.height,
    )