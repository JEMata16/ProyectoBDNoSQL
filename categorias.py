import streamlit as st
from mongo_utils import get_mongo_db

db = get_mongo_db()

# Function to create a new categoria
def create_categoria(name):
    # Save the data to the database
    categorias_col = db['categorias']
    categoria_data = {
        'name': name
    }
    categorias_col.insert_one(categoria_data)

# Function to update an existing categoria
def update_categoria(id, name):
    # Save the updated data to the database
    categorias_col = db['categorias']
    categoria_data = {
        'name': name
    }
    categorias_col.update_one({'_id': id}, {'$set': categoria_data})

# Function to update a categoria with a form
def update_categoria_form(categoria):
    categorias_col = db['categorias']
    row = categorias_col.find_one({'name': categoria})
    name = st.text_input('Name:', value=row['name'])
    update_categoria_button = st.button("Confirm Update")
    if update_categoria_button:
        update_categoria(row['_id'], name=name)

# Function to delete an existing categoria
def delete_categoria(row):
    categorias_col = db['categorias']
    categoria = categorias_col.find_one({'name': row})

    if categoria:
        categorias_col.delete_one({'_id': categoria['_id']})
        print(f"Categoria {row} deleted successfully.")
    else:
        print(f"Categoria {row} not found.")

# Function to retrieve a list of categorias
def get_categorias():
    categorias_col = db['categorias']
    cursor = categorias_col.find({})
    categorias = [categoria['name'] for categoria in cursor]
    return categorias

def catApp():
    cat_operations = ['Create Categoria', 'Update Categoria', 'Delete Categoria']
    operation = st.selectbox('Select operation:', cat_operations)
    if operation == 'Create Categoria':
        # Collect the data for the new categoria
        name = st.text_input('Name:')
        create_categoria_button = st.button("Confirm Creation")
        if create_categoria_button:
            create_categoria(name=name)
    elif operation == 'Update Categoria':
        # Retrieve the list of categorias
        categorias = get_categorias()
        # Create a dropdown menu to select the categoria to update
        categoria_to_update = st.selectbox('Select categoria to update:', categorias)
        # Call the update_categoria function with the selected categoria
        update_categoria_button = st.button("Get form")
        if update_categoria_button:
            update_categoria_form(categoria=categoria_to_update)
    elif operation == 'Delete Categoria':
        # Retrieve the list of categorias
        categorias = get_categorias()
        # Create a dropdown menu to select the categoria to delete
        categoria_to_delete = st.selectbox('Select categoria to delete:', categorias)
        # Call the delete_categoria function with the selected categoria
        delete_categoria_button = st.button("Confirm Deletion")
        if delete_categoria_button:
            delete_categoria(categoria_to_delete)