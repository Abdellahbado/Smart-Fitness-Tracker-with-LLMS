import streamlit as st
from user_profile import display_user_profile

def check_authentication():
    return 'user' in st.session_state and st.session_state.user is not None

def main():
    st.set_page_config(page_title="GymAI Assistant", page_icon="💪", layout="wide")
    
    if not check_authentication():
        st.warning("Please sign in or sign up to access GymAI Assistant.")
        if st.button("Go to Sign In / Sign Up"):
            st.switch_page("pages/Auth.py")
        return

    name, age, weight, height = display_user_profile()
    st.title("Welcome to GymAI Assistant")
    st.subheader("Your AI-powered fitness companion")

    # Main content
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(
            """
        GymAI Assistant is your personal AI-powered gym companion. 
        Whether you're a beginner or a seasoned athlete, we're here to help you 
        achieve your fitness goals.
        """
        )
        st.button("Get Started")
        # Feature highlights
        st.header("Key Features")
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("🏋️ AI Workout Planner")
            st.write(
                "Get personalized workout plans tailored to your goals and fitness level."
            )
            if st.button("Go to Workout Planner"):
                st.switch_page("pages/Workout_Planner.py")
            st.subheader("🍎 Nutrition Guidance")
            st.write("Receive AI-driven meal plans and nutritional advice.")
            if st.button("Go to Nutrition Guide"):
                st.switch_page("pages/Nutrition_Guide.py")
        with col4:
            st.subheader("📊 Progress Tracking")
            st.write("Visualize your fitness journey with advanced analytics.")
            if st.button("Go to Progress Tracker"):
                st.switch_page("pages/Progress_Tracker.py")
            st.subheader("🤖 Virtual Trainer")
            st.write("Get 24/7 support from our AI-powered virtual trainer.")
            if st.button("Go to Virtual Trainer"):
                st.switch_page("pages/Virtual_Trainer.py")
    with col2:
        st.image(
            "Fitness Master BB.jpg",
            caption="Achieve your fitness goals with AI",
            use_column_width=True,
        )
    # Footer
    st.markdown("---")
    st.write("© 2024 GymAI Assistant. All rights reserved.")

if __name__ == "__main__":
    main()