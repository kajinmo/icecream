import streamlit as st
from utils import load_data, get_unique_groups, get_ingredients_for_group, predict_rating

# Set page configuration to use the full width of the screen
st.set_page_config(layout="wide")

# Fixed selection rules for each group
SELECTION_RULES = {
    'colorants': 2,
    'fats_and_oils': 2,
    'flavors': 4,
    'dairy_and_alternatives': 3,
    'sweeteners': 2,
    'stabilizers_and_emulsifiers': 2,
    'acids_and_leavening_agents': 2,
    'proteins_and_enzymes': 2,
    'vitamins_and_minerals': 2,
    'preservatives_and_antioxidantes': 2, 
    'miscellaneous': 2
}

# Lista de marcas disponíveis
BRANDS = {
    "Haagen Dazs": "brand_HaagenDazs",
    "Breyers": "brand_Breyers",
    "Ben & Jerry's": "brand_BenJerrys",
    "Talenti": "brand_Talenti"
}

# Function to initialize session state for selected ingredients
def initialize_session_state():
    if 'selected_ingredients' not in st.session_state:
        st.session_state.selected_ingredients = {}
    
    # Initialize groups in session state
    for group in get_unique_groups(load_data()):
        if group not in st.session_state.selected_ingredients:
            st.session_state.selected_ingredients[group] = []
    
    # Initialize selected brand
    if 'selected_brand' not in st.session_state:
        st.session_state.selected_brand = None

# Function to handle ingredient selection with limits
def toggle_ingredient(group, ingredient):
    # If ingredient is already selected, remove it
    if ingredient in st.session_state.selected_ingredients[group]:
        st.session_state.selected_ingredients[group].remove(ingredient)
    # If ingredient is not selected and we haven't reached the limit, add it
    elif len(st.session_state.selected_ingredients[group]) < SELECTION_RULES.get(group, float("inf")):
        st.session_state.selected_ingredients[group].append(ingredient)
    # If we've reached the limit, show a warning
    else:
        limit = SELECTION_RULES.get(group, float("inf"))
        st.warning(f"You can only select up to {limit} ingredients from {group.replace('_', ' ').title()}")

# Function to reset all selections
def reset_selections():
    for group in st.session_state.selected_ingredients:
        st.session_state.selected_ingredients[group] = []
    st.session_state.selected_brand = None
    st.success("All selections have been reset!")
    st.rerun()  # Recarrega a aplicação para refletir as mudanças

# Function to create expandable sections for ingredient selection
def create_ingredient_selection(group, data):
    with st.expander(f"{group.replace('_', ' ').title()} (Max: {SELECTION_RULES.get(group, 'No limit')})"):
        group_ingredients = get_ingredients_for_group(data, group)
        
        # Show how many items are currently selected
        current_selections = len(st.session_state.selected_ingredients[group])
        max_selections = SELECTION_RULES.get(group, float("inf"))
        st.caption(f"Selected: {current_selections}/{max_selections}")
        
        # Create a grid layout for checkboxes
        cols = st.columns(3)  # Adjust number of columns as needed
        
        for i, ingredient in enumerate(group_ingredients):
            with cols[i % 3]:
                # Check if the ingredient is currently selected
                is_selected = ingredient in st.session_state.selected_ingredients[group]
                
                # Check if we're at the limit and this ingredient isn't already selected
                at_limit = current_selections >= max_selections and not is_selected
                
                # Create a checkbox for each ingredient
                if st.checkbox(
                    ingredient, 
                    value=is_selected,
                    key=f"cb_{group}_{ingredient}",
                    disabled=at_limit,
                    help=f"Select {ingredient} for your recipe"
                ):
                    if not is_selected:
                        toggle_ingredient(group, ingredient)
                else:
                    if is_selected:
                        toggle_ingredient(group, ingredient)

# Main function to run the app
def main():
    st.title("Industrial Ice Cream Ingredient Selector")
    
    # Initialize session state
    initialize_session_state()

    # Load the data
    data = load_data()

    # Split the page into two columns
    col1, col2 = st.columns([5, 2])  # Adjust the ratio as needed

    # Part 1: Filter Selection (Left Column)
    with col1:
        st.header("Select Filters")

        # Adicionar seleção de marca
        selected_brand_name = st.selectbox(
            "Select Ice Cream Brand",
            options=list(BRANDS.keys()),
            index=0,  # Define a primeira opção como padrão
            key="brand_select"
        )
        st.session_state.selected_brand = BRANDS[selected_brand_name]

        # Get unique groups
        groups = list(get_unique_groups(data))

        # Reorganizar grupos para exibir "flavors" primeiro
        if 'flavors' in groups:
            groups.remove('flavors')  # Remove "flavors" da lista original
            groups.insert(0, 'flavors')  # Adiciona "flavors" no início

        # Create expandable sections for each group
        for group in groups:
            create_ingredient_selection(group, data)

    # Part 2: Results Display (Right Column)
    with col2:
        st.image("https://cdn.prod.website-files.com/630a4d18e83aaa000bcd651e/6691780e4f5a682a2e3648c0_shutterstock_2429103279.jpg", use_container_width=True)

        st.header("Selected Ingredients")

        # Display selected ingredients
        total_selected = 0
        for group, ingredients in st.session_state.selected_ingredients.items():
            if ingredients:
                total_selected += len(ingredients)
                #st.subheader(group.replace('_', ' ').title())
                st.write(f"###### {group.replace('_', ' ').title()}")
                
                for ingredient in ingredients:
                    st.write(f"- {ingredient}")
        
        if total_selected == 0:
            st.write("No ingredients selected yet.")
        
        # Display selection count
        #st.subheader("Selection Summary")
        st.write(f"Total ingredients selected: {total_selected}")
        
        # Display selected brand
        #st.subheader("Selected Brand")
        st.write(f"Selected Brand: {selected_brand_name}")
        
        # Placeholder for future results (e.g., model output)
        st.subheader("Results")
        st.write("Results will be displayed here once the model is integrated. Make sure that at leat one flavor is selected")
        
        # Add a button to reset selections
        if st.button("Reset Selections"):
            reset_selections()

        # Make sure there is at least one flavor selected
        flavors_selected = len(st.session_state.selected_ingredients.get('flavors', [])) > 0

        # Add a button to process selections
        if st.button("Process Selections", disabled=not flavors_selected or total_selected == 0):
            st.success("Processing your selections...")

            # Add selected ingredients and brand to processing
            all_selected_ingredients = st.session_state.selected_ingredients
            selected_brand_column = st.session_state.selected_brand

            # Running the prediction
            predicted_rating = predict_rating(all_selected_ingredients, selected_brand_column)
            st.write(f"# The predicted rating for this ice cream is {predicted_rating}")


# Run the app
if __name__ == "__main__":
    main()