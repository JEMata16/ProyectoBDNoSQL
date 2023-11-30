import streamlit as st
from mongo_utils import get_mongo_db

db = get_mongo_db()

# Function to create a new editorial
def create_editorial(name, location):
    # Save the data to the database
    editoriales_col = db['editoriales']
    editorial_data = {
        'name': name,
        'location': location
    }
    editoriales_col.insert_one(editorial_data)

# Function to update an existing editorial
def update_editorial(id, name, location):
    # Save the updated data to the database
    editoriales_col = db['editoriales']
    editorial_data = {
        'name': name,
        'location': location
    }
    editoriales_col.update_one({'_id': id}, {'$set': editorial_data})

# Function to update an editorial with a form
def update_editorial_form(editorial):
    editoriales_col = db['editoriales']
    row = editoriales_col.find_one({'name': editorial})
    name = st.text_input('Name:', value=row['name'])
    location = st.text_input('Location:', value=row['location'])
    update_editorial_button = st.button("Confirm Update")
    if update_editorial_button:
        update_editorial(row['_id'], name=name, location=location)

# Function to delete an existing editorial
def delete_editorial(row):
    editoriales_col = db['editoriales']
    editorial = editoriales_col.find_one({'name': row})

    if editorial:
        editoriales_col.delete_one({'_id': editorial['_id']})
        print(f"Editorial {row} deleted successfully.")
    else:
        print(f"Editorial {row} not found.")

# Function to retrieve a list of editoriales
def get_editoriales():
    editoriales_col = db['editoriales']
    cursor = editoriales_col.find({})
    editoriales = [editorial['name'] for editorial in cursor]
    return editoriales

def editApp():
    editoriales_operations = ['Create Editorial', 'Update Editorial', 'Delete Editorial']
    operation = st.selectbox('Select operation:', editoriales_operations)

    if operation == 'Create Editorial':
        # Collect the data for the new editorial
        name = st.text_input('Name:')
        location = st.text_input('Location:')
        create_editorial_button = st.button("Confirm Creation")

        if create_editorial_button:
            create_editorial(name=name, location=location)
    elif operation == 'Update Editorial':
        # Retrieve the list of editoriales
        editoriales = get_editoriales()

        # Create a dropdown menu to select the editorial to update
        editorial_to_update = st.selectbox('Select editorial to update:', editoriales)

        # Call the update_editorial_form function with the selected editorial
        update_editorial_button = st.button("Get form")

        if update_editorial_button:
            update_editorial_form(editorial_to_update)
    elif operation == 'Delete Editorial':
        # Retrieve the list of editoriales
        editoriales = get_editoriales()

        # Create a dropdown menu to select the editorial to delete
        editorial_to_delete = st.selectbox('Select editorial to delete:', editoriales)

        # Call the delete_editorial function with the selected editorial
        delete_editorial_button = st.button("Confirm Deletion")

        if delete_editorial_button:
            delete_editorial(editorial_to_delete)