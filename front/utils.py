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


# Load the unique ingredients CSV
def load_data():
    return pd.read_csv(os.path.join(ingredients_dir, 'unique_ingredients.csv'))

# Get unique groups from the data
def get_unique_groups(data):
    return data['classification'].unique()

# Get ingredients for a specific group
def get_ingredients_for_group(data, group):
    return data[data['classification'] == group]['ingredient'].tolist()











# Load the model and scaler
def load_model():
    model = joblib.load(os.path.join(models_dir, 'best_svr_model.pkl'))
    model_columns = joblib.load(os.path.join(models_dir, 'colunas_modelo.joblib'))
    return model, model_columns

def ingredients_list_to_array(present_ingredients_list, model_columns):
    # Criar um array que representa a presença dos ingredientes
    bool_present_ingredients_list = [1 if coluna in present_ingredients_list else 0 for coluna in model_columns]
    bool_array = np.array(bool_present_ingredients_list).reshape(1, -1)
    return bool_array

def predict_rating(present_ingredients_list):
    model, model_columns = load_model()
    bool_array = ingredients_list_to_array(present_ingredients_list, model_columns)
    pred = model.predict(bool_array)
    return pred