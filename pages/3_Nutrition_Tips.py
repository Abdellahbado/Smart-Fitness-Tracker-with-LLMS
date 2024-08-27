import streamlit as st
from user_profile import display_user_profile
from utils.llm_handler import get_response_from_llm

st.title("Nutrition Guidance")

if "user" not in st.session_state:
    st.warning("Please log in to access your Personalized Workout.")

else:
    name, age, weight, height = display_user_profile()

    # Dietary preferences
    diet_type = st.selectbox(
        "Dietary preference",
        ["No restrictions", "Vegetarian", "Vegan", "Keto", "Paleo", "Mediterranean"],
    )

    goals = st.multiselect(
        "Nutrition goals",
        [
            "Weight loss",
            "Muscle gain",
            "Maintenance",
            "Improved energy",
            "Better digestion",
        ],
    )

    allergies = st.multiselect(
        "Food allergies or intolerances",
        ["None", "Dairy", "Gluten", "Nuts", "Soy", "Eggs", "Fish"],
    )

    if st.button("Get Nutrition Plan"):
        bmi = weight / ((height / 100) ** 2)
        nutrition_input = f"""Create a nutrition plan for a {age}-year-old {gender.lower()} with BMI {bmi:.1f}.
        Dietary preference: {diet_type}. Goals: {', '.join(goals)}. 
        Allergies/intolerances: {', '.join(allergies) if allergies != ['None'] else 'None'}.
        Include daily calorie target, macronutrient breakdown, and a sample meal plan."""

        nutrition_plan = get_response_from_llm(nutrition_input)
        st.subheader("Your Personalized Nutrition Plan")
        st.write(nutrition_plan)

    # New feature: Recipe Suggestion
    st.subheader("Healthy Recipe Suggestion")
    cuisine = st.selectbox(
        "Choose cuisine type",
        ["Mediterranean", "Asian", "Mexican", "Italian", "American"],
    )
    if st.button("Get Recipe Idea"):
        recipe = get_response_from_llm(
            f"Suggest a healthy {cuisine} recipe that aligns with a {diet_type} diet."
        )
        st.write(recipe)

    # New feature: Nutrition FAQ
    st.subheader("Nutrition FAQ")
    nutrition_question = st.text_input("Ask a nutrition question")
    if nutrition_question and st.button("Get Answer"):
        answer = get_response_from_llm(
            f"Answer this nutrition question: {nutrition_question}"
        )
        st.write(answer)
