# Ice Cream Dataset Project

This project aims to predict ice cream ratings based on brand, flavor, and ingredient lists using a linear regression model. It was initially started in 2021 and has since been refactored and improved with better software engineering practices, advanced modeling techniques, and deployment capabilities.

<p align="center">
  <img src="https://user-images.githubusercontent.com/74104562/214484820-63a043dd-6d17-45a1-b871-8e66f2d12e3e.png" alt="image">
</p>

## Project Structure
```plaintext
ice-cream-rating-prediction/
├── notebooks/              # Contains Jupyter notebooks with exploratory data analysis (EDA), model development, and results.
├── front/                  # Contains the files for the Streamlit app.
├── render.yaml             # Blueprint for deploying the Streamlit app on Render.
├── pyproject.toml          # Configuration file used by uv lib.
├── requirements.txt        # List of dependencies for the project (used by render).
└── README.md               # This file.
```

## About the dataset
The database used was found on the Kaggle platform, which contains 14.669 reviews and details of 241 flavors from four ice cream brands: Ben&Jerry's, Breyers, Häagen-Dazs and Talenti.

## Input files:
- `products.csv`: descriptive information about each ice cream flavor: flavor name, description, average rating, and ingredient list.
- `reviews.csv`: all the reviews used to calculate the average score of the previous dataset


## Notebooks
The `notebooks/` folder contains all the Jupyter notebooks used for:
- Exploratory data analysis (EDA) (`notebook/icecream-p1-eda.ipynb`): Understanding the dataset, identifying patterns, and exploring relationships between features.
- Data processing and cleaning (`notebook/icecream-p2-ingredients.ipynb`): to generate ingredients list.
- Model Development (`notebook/icecream-p3-model.ipynb`): Building and evaluating the linear regression model, including feature selection, k-fold cross-validation, and hyperparameter tuning.


## Streamlit App
The `front/` folder contains the files for the Streamlit app, which provides an interactive interface to:
- Input ice cream details (brand, flavor, ingredients).
- Predict the ice cream rating based on the trained model.

<br>

----

## Setup Instructions

### Prerequisites

Ensure you have the following installed:

- Python (version 3.12 recommended)
- uv (install using `pipx install uv` or `pip install uv`)
- Visual Studio Code

<br>

1. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

<br>

2. Create a venv and install dependencies with uv
```bash
uv sync
```

<br>

3. Activate the Virtual Environment
```bash
source .venv/Scripts/activate
```

<br>

4. Open in VSCode
```bash
code .
```

<br>

5. Configure VSCode to Use the Virtual Environment

- Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on macOS).
- Search for "`Python: Select Interpreter`".
- Choose the interpreter inside `.venv` (e.g., .venv/bin/python or .venv\Scripts\python.exe).

<br>

5. Run streamlit app
```bash
streamlit run front/main.py
```
<br>

## Deployment on Render (optional)

The project is deployed using Render. The render.yaml file serves as the blueprint for deploying the Streamlit app. To deploy:
- Push the project to your GitHub repository.
- Connect the repository to Render and use the render.yaml file for deployment configuration:
  - In `Render Dashboard` > `Blueprints` > `New Blueprint Instance` > `Connect a repositor` > Select `render.yaml`

