# Ice Cream Dataset Project

This project was divided into four parts, whose purpose is to perform detailed analysis and modeling of an ice cream estimation dataset.

<p align="center">
  <img src="https://user-images.githubusercontent.com/74104562/214484820-63a043dd-6d17-45a1-b871-8e66f2d12e3e.png" alt="image">
</p>

## About the dataset
The database used was found on the Kaggle platform, which contains details and estimates of 241 flavors from four ice cream brands: Ben&Jerry's, Breyers, Häagen-Dazs and Talenti.

## Input files:
- 'products.csv': descriptive information about each ice cream flavor: flavor name, description, average rating, and ingredient list.
- 'reviews.csv': all the reviews used to calculate the average score of the previous dataset


## project planning
- Part 1: exploratory data analysis (icecream-p1-eda.ipynb)

- Part 2: data processing and cleaning to generate ingredients list(icecream-p2-ingredients.ipynb)

- Part 3: hypothesis testing and modeling with linear regression

- Part 4: modeling with multiple correspondence analysis (MCA) (coming soon)



----

## Prerequisites

Ensure you have the following installed:

- Python (version 3.12 recommended)
- uv (install using `pipx install uv` or `pip install uv`)
- Visual Studio Code



## Setup Instructions

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