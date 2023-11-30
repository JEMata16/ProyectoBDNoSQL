import streamlit as st
from mongo_utils import get_mongo_db
import datetime

db = get_mongo_db()

def create_autor(name,birth_date,nationality):
        # Save the data to the database
        autores_col = db['autores']
        autor_data = {
            'name': name,
            'birth_date': birth_date,
            'nationality':nationality
        }
        autores_col.insert_one(autor_data)

    # Function to update an existing autor
def update_autor(id, name, birth_date, nationality):
    # Save the updated data to the database
    autores_col = db['autores']
    autor_data = {
        'name': name,
        'birth_date': birth_date,
        'nationality':nationality
    }
    autores_col.update_one({'_id': id}, {'$set': autor_data})

def update_form(autor):
    autores_col = db['autores']
    row = autores_col.find_one({'name': autor})
    name = st.text_input('Name:', value=row['name'])
    birth = st.date_input('Birth date:', value=datetime.datetime.strptime(row['birth_date'],  '%Y-%m-%d').date(),min_value=datetime.datetime(1940, 5, 17))
    nationality = st.text_input('Nationality:', value=row['nationality'])
    update_autor_button = st.button("Confirm Update")
    if update_autor_button:
         update_autor(row['_id'], name=name, birth_date=birth, nationality=nationality)

# Function to delete an existing autor
def delete_autor(row):
    autores_col = db['autores']
    autor = autores_col.find_one({'name': row})

    if autor:
        autores_col.delete_one({'_id': autor['_id']})
        print(f"Author {row} deleted successfully.")
    else:
        print(f"Author {row} not found.")

def get_autores():
    autores_col = db['autores']
    cursor = autores_col.find({})
    autores = [autor['name'] for autor in cursor]
    return autores

def autApp():
    autor_operations = ['Create Autor', 'Update Autor', 'Delete Autor']
    operation = st.selectbox('Select operation:', autor_operations)
    if operation == 'Create Autor':
        # Collect the data for the new autor
        name = st.text_input('Name:')
        birth = st.date_input('Birth date:',min_value=datetime.datetime(1940, 5, 17))
        nationality = st.text_input("Nationality:")
        create_autor_button = st.button("Confirm Creation")
        if create_autor_button:
            create_autor(name=name, birth_date=birth.isoformat(), nationality=nationality)
    elif operation == 'Update Autor':
        # Retrieve the list of autores
        autores = get_autores()
        # Create a dropdown menu to select the autor to update
        autor_to_update = st.selectbox('Select autor to update:', autores)
        # Call the update_autor function with the selected autor
        update_autor_button = st.button("Get form")
        if update_autor_button:
            update_form(autor_to_update)
    elif operation == 'Delete Autor':
        # Retrieve the list of autores
        autores = get_autores()
        # Create a dropdown menu to select the autor to delete
        autor_to_delete = st.selectbox('Select autor to delete:', autores)
        # Call the delete_autor function with the selected autor
        delete_autor_button = st.button("Confirm Deletion")
        if delete_autor_button:
            delete_autor(autor_to_delete)