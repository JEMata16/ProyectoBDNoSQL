import streamlit as st
from mongo_utils import get_mongo_db
from autores import get_autores
from categorias import get_categorias
from editoriales import get_editoriales
from bson import ObjectId
import datetime


db = get_mongo_db()

# Function to create a new libro
def create_libro(author_id, title, category_ids, publication_date, publisher):
    from datetime import datetime
    # Convert date object to datetime object
    publication_date = datetime.combine(publication_date, datetime.min.time())

    # Save the data to the database
    libros_col = db['libros']
    libro_data = {
        'titulo': title,
        'autor': author_id,
        'categoria': category_ids,
        'publication_date': publication_date,
        'publisher': publisher
    }
    libros_col.insert_one(libro_data)

# Function to update an existing libro
def update_libro(book_id, author_id, title, category_ids, publication_date, publisher):
    from datetime import datetime
    # Convert date object to datetime object
    publication_date = datetime.combine(publication_date, datetime.min.time())

    # Save the updated data to the database
    libros_col = db['libros']
    libro_data = {
        'titulo': title,
        'autor': author_id,
        'categoria': category_ids,
        'publication_date': publication_date,
        'publisher': publisher
    }
    libros_col.update_one({'_id': book_id}, {'$set': libro_data})

# Function to update a libro with a form
def update_libro_form(book_id):
    libros_col = db['libros']
    row = libros_col.find_one({'_id': book_id})
    with st.form(key='update_libro_form'):
        author_id = st.selectbox('Select author:', get_autores())
        title = st.text_input('Title:', value=row['titulo'])
        category_ids = st.multiselect('Select categories:', get_categorias(), default=row['categoria'])
        publication_date = st.date_input('Publication Date:', value=row['publication_date'])
        publisher = st.selectbox('Select publisher:', get_editoriales(), index=get_editoriales().index(row['publisher']))
        if st.form_submit_button("Confirm Update"):
            # Update the libro when the button is clicked
            update_libro(book_id=book_id, author_id=author_id, title=title, category_ids=category_ids,
                         publication_date=publication_date, publisher=publisher)

# Function to delete an existing libro
def delete_libro(book_id):
    libros_col = db['libros']
    libro = libros_col.find_one({'_id': book_id})

    if libro:
        libros_col.delete_one({'_id': libro['_id']})
        print(f"Libro {book_id} deleted successfully.")
    else:
        print(f"Libro {book_id} not found.")

# Function to retrieve a list of libros
def get_libros():
    libros_col = db['libros']
    cursor = libros_col.find({})
    libros = [{'_id': libro['_id'], 'autor': libro['autor'], 'titulo': libro['titulo'],
               'categoria': libro['categoria'], 'publication_date': libro['publication_date'],
               'publisher': libro['publisher']} for libro in cursor]
    return libros


def librosApp():
    libro_operations = ['Create Libro', 'Update Libro', 'Delete Libro']
    operation = st.selectbox('Select operation:', libro_operations)

    if operation == 'Create Libro':
        # Collect the data for the new libro
        author_id = st.selectbox('Select author:', get_autores())
        title = st.text_input('Title:')
        category_ids = st.multiselect('Select categories:', get_categorias())
        publication_date = st.date_input('Publication Date:',min_value=datetime.datetime(1940, 5, 17))
        publisher = st.selectbox('Select publisher:', get_editoriales())

        create_libro_button = st.button("Confirm Creation")
        if create_libro_button:
            create_libro(author_id=author_id, title=title, category_ids=category_ids,
                         publication_date=publication_date, publisher=publisher)

    elif operation == 'Update Libro':
        # Retrieve the list of libros
        libros = get_libros()
        # Create a dropdown menu to select the libro to update
        libro_to_update = st.selectbox('Select libro to update:', libros)
        # Call the update_libro_form function with the selected libro
        update_libro_button = st.button("Get form")
        
        if update_libro_button:
            print(libro_to_update['_id'])
            update_libro_form(book_id=ObjectId(libro_to_update['_id']))

    elif operation == 'Delete Libro':
        # Retrieve the list of libros
        libros = get_libros()
        # Create a dropdown menu to select the libro to delete
        libro_to_delete = st.selectbox('Select libro to delete:', libros)
        # Call the delete_libro function with the selected libro
        delete_libro_button = st.button("Confirm Deletion")

        if delete_libro_button:
            delete_libro(book_id=libro_to_delete['_id'])
