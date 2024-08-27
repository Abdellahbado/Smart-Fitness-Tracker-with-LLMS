from data.user_data_manager import load_workout_plan, save_workout_plan
import streamlit as st
from user_profile import display_user_profile
from utils.llm_handler import get_response_from_llm
import datetime
from dotenv import load_dotenv
from utils.utils_function import search_youtube_videos


load_dotenv()

st.title("Workout Planner")


if "user" not in st.session_state:
    st.warning("Please log in to access your Personalized Workout.")
else:
    name, age, weight, height = display_user_profile()
    username = st.session_state.user

    if "workout_plan" not in st.session_state:
        st.session_state.workout_plan = None

    if "past_workout_plans" not in st.session_state:
        st.session_state.past_workout_plans = None

    if "video_links" not in st.session_state:
        st.session_state.video_links = None

    # Personalized greeting
    if name:
        st.write(f"Hello, {name}! Let's plan your workout.")

    MAX_RESULTS = 3

    if "save_status" not in st.session_state:
        st.session_state.save_status = None

    # User preferences
    location = st.radio("Where do you work out?", ("At home", "At the gym"))

    if location == "At home":
        equipment = st.multiselect(
            "What equipment do you have?",
            [
                "Dumbbells",
                "Yoga mat",
                "Resistance band",
                "Pull-up bar",
                "Kettlebell",
                "None",
            ],
        )
    else:
        equipment = ["Full gym equipment"]

    fitness_level = st.selectbox(
        "Fitness level", ("Beginner", "Intermediate", "Advanced")
    )

    goals = st.multiselect(
        "Workout goals",
        [
            "Strength training",
            "Cardio",
            "Flexibility",
            "Weight loss",
            "Muscle gain",
            "Endurance",
        ],
    )

    body_part = st.selectbox(
        "Target body part",
        ["Chest", "Back", "Legs", "Arms", "Abs", "Shoulders", "Full body"],
    )

    duration = st.slider("Workout duration (minutes)", 15, 120, 45, step=5)
    frequency = st.number_input("Workouts per week", min_value=1, max_value=7, value=3)
    col1, col2 = st.columns(2)
    workout_plan = None
    with col1:
        if st.button("Generate Workout Plan"):
            human_input = f"""Generate a detailed workout plan for a {fitness_level} level person who works out {location.lower()} with: {', '.join(equipment)}. 
            Goals: {', '.join(goals)}. Target: {body_part}.
            Duration: {duration} minutes, {frequency} times per week.
            Include warm-up, main exercises with sets, reps, and rest periods, and cool-down."""

            workout_plan = get_response_from_llm(human_input)
            st.session_state.save_status = None
            st.session_state.workout_plan = workout_plan
            st.session_state.viewing_past_workouts = False

            # Split the response into workout plan and video title
            prompt = f"""give me one precise title for youtube video for this workout plan : for a {fitness_level} level person who works out {location.lower()} with: {', '.join(equipment)}. 
            Goals: {', '.join(goals)}. Target: {body_part}.
            Duration: {duration} minutes, {frequency} times per week.
            Include warm-up, main exercises with sets, reps, and rest periods, and cool-down."""

            video_title = get_response_from_llm(prompt)
            print("video title", video_title)

            # Search for YouTube video
            st.session_state.video_links = search_youtube_videos(
                video_title.strip(), max_results=MAX_RESULTS
            )

    with col2:
        if st.button("View Past Workout Plans"):
            st.session_state.past_workout_plans = load_workout_plan(username)
            print("past workout plans", st.session_state.past_workout_plans)
            st.session_state.viewing_past_workouts = True

    # Display past workout plans
    if st.session_state.get("viewing_past_workouts", False):
        st.subheader("Your Past Workout Plans")
        if st.session_state.past_workout_plans:
            for i, workout_dict in enumerate(st.session_state.past_workout_plans):
                workout_plan = workout_dict.get("workout", "")
                st.write(f"Workout Plan {i + 1}")
                st.write(workout_plan)
                st.write("---")

        else:
            st.write("No past workout plans found.")

        if st.button("Return to Generated Workout"):
            st.session_state.viewing_past_workouts = False
    else:
        if st.session_state.get("workout_plan"):
            st.subheader("Your Personalized Workout Plan")
            st.write(st.session_state.workout_plan)

            if st.session_state.video_links:
                st.subheader("Recommended Videos")
                cols = st.columns(MAX_RESULTS)  # Create 3 columns
                for i, video_link in enumerate(st.session_state.video_links):
                    with cols[i]:
                        st.video(video_link)

            if st.session_state.save_status is None:
                if st.button("Save Workout Plan"):
                    updated_workout = {"workout": st.session_state.workout_plan}
                    save_workout_plan(username, updated_workout)
                    st.session_state.save_status = (
                        "Personalized workout saved successfully!"
                    )

            if st.session_state.save_status:
                st.success(st.session_state.save_status)
    # New feature: Exercise Library
    st.subheader("Exercise Library")
    exercise_type = st.selectbox(
        "Choose exercise type", ["Strength", "Cardio", "Flexibility"]
    )
    if st.button("Get Exercise Ideas"):
        exercise_ideas = get_response_from_llm(
            f"Provide 5 {exercise_type} exercises with brief descriptions."
        )
        st.write(exercise_ideas)

        # Search for a general video about the exercise type
        st.subheader(f"Learn More About {exercise_type} Exercises")
        video_links = search_youtube_videos(
            f"Best {exercise_type} exercises tutorial", max_results=MAX_RESULTS
        )
        if video_links:
            st.subheader("Recommended Videos")
            cols = st.columns(MAX_RESULTS)  # Create 3 columns
            for i, video_link in enumerate(video_links):
                with cols[i]:
                    st.video(video_link)
        else:
            st.write("No relevant videos found.")
