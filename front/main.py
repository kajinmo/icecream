import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Defining paths
notebook_dir = os.path.abspath('')  # This gets the current notebook path
models_path = os.path.join(notebook_dir, 'data', 'model')
ice_cream_model_joblib = os.path.join(models_path, 'ice_cream_model_pipeline.joblib')
ice_cream_brands_pickle = os.path.join(models_path, 'ice_cream_brands.pkl')
common_ingredients_pickle = os.path.join(models_path, 'common_ingredients.pkl')

# Set page configuration
st.set_page_config(
    page_title="Ice Cream Rating Predictor",
    page_icon="🍦",
    layout="wide"
)

# Load the saved model and supporting files
@st.cache_resource
def load_model():
    model = joblib.load(ice_cream_model_joblib)
    with open(ice_cream_brands_pickle, 'rb') as f:
        brands = pickle.load(f)
    with open(common_ingredients_pickle, 'rb') as f:
        ingredients = pickle.load(f)
    return model, brands, ingredients

# Main function to predict rating
def predict_ice_cream_rating(brand, ingredients_list):
    # Convert ingredients list to string format expected by model
    ingredients_str = ', '.join(ingredients_list)
    
    # Create a DataFrame with the input data
    input_data = pd.DataFrame({
        'brand': [brand],
        'ingredients_cleaned': [ingredients_str]
    })
    
    # Use the pipeline to make a prediction
    prediction = model.predict(input_data)[0]
    return prediction

# UI Functions
def create_ingredient_selector(common_ingredients):
    # Multi-select with autocomplete for ingredients
    selected_ingredients = st.multiselect(
        "Select or type ingredients:",
        options=common_ingredients,
        default=[],
        key="ingredient_selector"
    )
    
    # Custom ingredient input
    custom_ingredient = st.text_input("Add a custom ingredient (press Enter to add):")
    if custom_ingredient and st.button("Add Ingredient"):
        if custom_ingredient not in selected_ingredients:
            selected_ingredients.append(custom_ingredient)
            st.session_state.ingredient_selector = selected_ingredients
    
    return selected_ingredients

# Load model and data
try:
    model, brands, common_ingredients = load_model()
    model_loaded = True
except Exception as e:
    st.error(f"Error loading model: {e}")
    model_loaded = False

# App title and description
st.title("🍦 Ice Cream Rating Predictor")
st.markdown("""
Use this app to predict how highly an ice cream would be rated based on its ingredients and brand.
Select ingredients from the list or add your own custom ingredients!
""")

# Create sidebar for inputs
with st.sidebar:
    st.header("Ice Cream Details")
    
    # Brand selection
    if model_loaded:
        brand = st.selectbox("Select Brand:", brands)
    else:
        brand = st.selectbox("Select Brand:", ["Talenti", "Häagen-Dazs", "Ben & Jerry's"])
    
    # Ingredients selection
    st.subheader("Ingredients")
    if model_loaded:
        ingredients = create_ingredient_selector(common_ingredients)
    else:
        ingredients = create_ingredient_selector(["milk", "sugar", "cream", "vanilla", "chocolate"])
    
    # Make prediction button
    predict_button = st.button("Predict Rating", type="primary")

# Main content area
if predict_button and model_loaded and ingredients:
    # Show ingredients summary
    st.subheader("Your Ice Cream Recipe")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write(f"**Brand:** {brand}")
        st.write(f"**Number of ingredients:** {len(ingredients)}")
    
    with col2:
        st.write("**Ingredients:**")
        st.write(", ".join(ingredients))
    
    # Make prediction
    predicted_rating = predict_ice_cream_rating(brand, ingredients)
    
    # Display the rating
    st.subheader("Predicted Rating")
    
    # Create columns for rating visualization
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Display the numeric rating
        st.metric("Predicted Rating", f"{predicted_rating:.2f}/5.0")
        
        # Add emojis based on rating
        if predicted_rating >= 4.5:
            st.markdown("### 😍 Excellent!")
        elif predicted_rating >= 4.0:
            st.markdown("### 😊 Very Good!")
        elif predicted_rating >= 3.5:
            st.markdown("### 🙂 Good")
        elif predicted_rating >= 3.0:
            st.markdown("### 😐 Average")
        else:
            st.markdown("### 😕 Below Average")
    
    with col2:
        # Create a gauge chart for the rating
        fig, ax = plt.subplots(figsize=(10, 2))
        
        # Rating gauge
        ax.barh(0, 5, color='lightgray', height=0.3)
        ax.barh(0, predicted_rating, color='#FF9F1C', height=0.3)
        
        # Add scale markings
        for i in range(1, 6):
            ax.axvline(i, color='white', linestyle='-', alpha=0.3)
            ax.text(i, -0.2, str(i), ha='center', va='center')
        
        # Remove axes
        ax.set_yticks([])
        ax.set_xlim(0, 5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        
        st.pyplot(fig)
    
    # Add some analysis
    st.subheader("What contributes to this rating?")
    
    # This is a simplified analysis - in a complete app, you could use SHAP values or other
    # techniques to show ingredient contributions to the prediction
    st.write("""
    The prediction is based on the patterns learned from training data. Here are some general insights:
    
    - Premium ingredients like vanilla bean, real fruit, and high-quality chocolate tend to correlate with higher ratings
    - The number of ingredients can impact ratings (sometimes simpler is better)
    - Certain brands have established reputations that influence expectations
    """)
    
    # Provide suggestions
    st.subheader("Want to improve the rating?")
    st.write("Try these modifications:")
    
    # These are general suggestions - in a real app, these would be based on model insights
    if "vanilla extract" in ingredients:
        st.write("- Try using vanilla bean instead of vanilla extract")
    
    if "chocolate" in ingredients and "cocoa" not in ingredients:
        st.write("- Add cocoa powder to enhance the chocolate flavor")
    
    if len(ingredients) > 10:
        st.write("- Consider simplifying the recipe - too many ingredients can overwhelm the flavor")

elif predict_button and not ingredients:
    st.warning("Please select at least one ingredient")

# Show instructions if no prediction has been made
if not predict_button or not model_loaded:
    st.info("👈 Select a brand and ingredients on the sidebar, then click 'Predict Rating'")
    
    # Display sample data if model is loaded
    if model_loaded:
        st.subheader("Sample Predictions")
        
        # Create sample data for demonstration
        sample_data = [
            ("Häagen-Dazs", ["cream", "milk", "sugar", "egg yolks", "vanilla bean"]),
            ("Ben & Jerry's", ["cream", "milk", "sugar", "egg yolks", "chocolate", "cookie dough"]),
            ("Talenti", ["milk", "sugar", "cream", "coffee", "chocolate"])
        ]
        
        # Show sample ratings
        for sample_brand, sample_ingredients in sample_data:
            sample_rating = predict_ice_cream_rating(sample_brand, sample_ingredients)
            st.write(f"**{sample_brand}** with {', '.join(sample_ingredients)}: **{sample_rating:.2f}/5.0**")

# Add footer
st.markdown("---")
st.markdown("🍦 Ice Cream Rating Predictor - Machine Learning Model")