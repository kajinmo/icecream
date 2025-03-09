import joblib
import numpy as np
import os
import pandas as pd
import numpy as np


# Get the current code directory
project_dir = os.path.abspath('')  # This 
# Change the working directory
os.chdir(project_dir)
ingredients_dir = os.path.join(project_dir, 'data', 'intermediate')
models_dir = os.path.join(project_dir, 'data', 'model')



######### Ingredient group functions #########
# Load the unique ingredients CSV
def load_data():
    return pd.read_csv(os.path.join(ingredients_dir, 'unique_ingredients.csv'))

# Get unique groups from the data
def get_unique_groups(data):
    return data['classification'].unique()

# Get ingredients for a specific group
def get_ingredients_for_group(data, group):
    return data[data['classification'] == group]['ingredient'].tolist()



######### Model functions #########
# append brand to ing dicsts

# Extract all items into a single list
def convert_dict_to_list(ingredients_dict, selected_brand_column):
    present_ingredients_list = []
    for ingredients in ingredients_dict.values():
        present_ingredients_list.extend(ingredients)
        present_ingredients_list.append(selected_brand_column)
    return present_ingredients_list

# Load the model and scaler
def load_model():
    model = joblib.load(os.path.join(models_dir, 'best_svr_model.pkl'))
    model_columns = joblib.load(os.path.join(models_dir, 'colunas_modelo.joblib'))
    return model, model_columns

# Create an array which represents the selected ingredients
def ingredients_list_to_array(present_ingredients_list, model_columns):
    bool_present_ingredients_list = []
    for coluna in model_columns:
        if coluna in present_ingredients_list:
            bool_present_ingredients_list.append(1)
        else:
            bool_present_ingredients_list.append(0)
    return np.array(bool_present_ingredients_list).reshape(1, -1)

# Runs prediction model
def run_model(bool_array, model):
    pred = model.predict(bool_array)
    return pred[0]

def correct_model(pred_rating):
    # Define the desired range
    min_rating = 3
    max_rating = 4.81
    average_rating = 4.45

    # Adjust the rating based on the difference from 4.35
    dif = pred_rating - average_rating

    if pred_rating < average_rating:
        # Scale down the difference and add to the original rating
        corrected_rating = (dif * average_rating * 6.5) + average_rating  # Adjust the scaling factor as needed
    else:
        # Scale up the difference and add to the original rating
        corrected_rating = (dif * average_rating * 4) + average_rating  # Adjust the scaling factor as needed

    print(f'pred: {pred_rating} adj:{corrected_rating}')
    # Ensure the corrected rating stays within the desired range
    if corrected_rating < min_rating:
        corrected_rating = min_rating
    elif corrected_rating > max_rating:
        corrected_rating = max_rating
    
    return round(corrected_rating, 2)

def predict_rating(dict_of_selected_ingredients, selected_brand_column):
    present_ingredients_list = convert_dict_to_list(dict_of_selected_ingredients, selected_brand_column)
    model, model_columns = load_model()
    bool_array = ingredients_list_to_array(present_ingredients_list, model_columns)
    pred_rating = run_model(bool_array, model)
    pred_rating = correct_model(pred_rating)
    return pred_rating