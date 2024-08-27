import streamlit as st

from PIL import Image
import io
from dotenv import load_dotenv
from utils.llm_handler import get_response_from_llm
from utils.utils_function import detect_food

load_dotenv()


st.title("Food Calorie Calculator")

calculation_method = st.radio(
    "How would you like to calculate calories?", ("From Image", "Using Description")
)

if calculation_method == "From Image":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()

        if st.button("Analyze"):
            with st.spinner("Analyzing..."):
                food_items = detect_food(img_byte_arr)

            if food_items:
                st.subheader("Estimated Nutritional Information:")
                with st.spinner("Calculating nutritional information..."):
                    prompt = """
                    You are a nutritionist specializing in calorie estimation. Based on the following list of detected food items, provide an estimate of the total calories, along with a breakdown of macronutrients (protein, carbohydrates, and fats) if possible. Also, mention any assumptions made in the calculation.

                    Detected Food Items: {food_items}

                    Please format your response as follows:
                    Total Calories: [number] kcal
                    Protein: [number] g
                    Carbohydrates: [number] g
                    Fat: [number] g

                    Assumptions: [List any assumptions made about portion sizes or specific ingredients]

                    Additional Notes: [Any relevant nutritional information or warnings]
                    """

                    nutrition_info = get_response_from_llm(prompt)
                st.write(nutrition_info)
            else:
                st.warning("No food items were detected in the image.")


elif calculation_method == "Using Description":
    food_description = st.text_area("Enter food description:")
    if st.button("Calculate Calories"):
        if food_description:
            with st.spinner("Calculating..."):
                prompt = f"""
                Given the following food description, please provide an estimate of the total calories, 
                along with a breakdown of macronutrients (protein, carbohydrates, and fats) if possible. 
                Also, mention any assumptions made in the calculation.

                Food Description: {food_description}

                Please format your response as follows:
                Total Calories: [number] kcal
                Protein: [number] g
                Carbohydrates: [number] g
                Fat: [number] g
                
                Assumptions: [List any assumptions made]
                
                Additional Notes: [Any relevant nutritional information or warnings]
                """

                result = get_response_from_llm(food_description)
            st.write(result)
        else:
            st.warning("Please enter a food description.")
