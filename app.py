import streamlit as st
import pandas as pd
from mongo_utils import get_mongo_db
from auth import loginPage
from flask import session
from autores import autApp
from categorias import catApp
from editoriales import editApp


# Initialize Streamlit
config = st.set_page_config(page_title='Biblioteca', layout='wide')


# Function to fetch data from MongoDB and convert it to a DataFrame
def fetch_data(collection):
    cursor = collection.find({})
    data = list(cursor)
    df = pd.DataFrame(data)
    return df


if loginPage() == True or 'usuario' in st.session_state:
    selected_collection = st.sidebar.selectbox('Select Collection', ['libros', 'autores', 'usuarios', 'prestamos', 'resenas', 'categorias', 'editoriales', 'reservas'])
    db = get_mongo_db()  
    if selected_collection == 'libros':
        df = fetch_data(db['libros'])
    elif selected_collection == 'autores':
        df = fetch_data(db['autores'])
    elif selected_collection == 'usuarios':
        df = fetch_data(db['usuarios'])
    elif selected_collection == 'prestamos':
        df = fetch_data(db['prestamos'])
    elif selected_collection == 'resenas':
        df = fetch_data(db['resenas'])
    elif selected_collection == 'categorias':
        df = fetch_data(db['categorias'])
    elif selected_collection == 'editoriales':
        df = fetch_data(db['editoriales'])
    elif selected_collection == 'reservas':
        df = fetch_data(db['reservas'])
    st.title(f"{selected_collection.capitalize()}")

    # Display the DataFrame

    st.write(df)

    # Additional functionality can be added based on the selected collection
    if selected_collection == 'libros':
        st.sidebar.empty()
        
        col1, col2, col3 = st.columns(3)
    
        if col1.button("Agregar una reseña"):
            add_libros()
        elif col2.button("Agregar un libro"):
            pass
        elif col3.button("Reservar un libro"):
            pass
        pass

    elif selected_collection == 'autores':
        autApp()
    elif selected_collection == 'categorias':
        catApp()
    elif selected_collection == 'editoriales':
        editApp()

