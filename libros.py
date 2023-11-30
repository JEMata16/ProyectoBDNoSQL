import streamlit as st
from mongo_utils import getAutores

def add_libros():
    libro = st.text_area("Agrega el nombre del libro:")
    autores = st.selectbox("Elige el autor del libro", getAutores())

    #  if st.button(f"Escribe tu reseña para el libro: {row['titulo']}"):
    #         # Logic to handle making resena for the selected book
    #         user_id = get_userByName(st.session_state['usuario'])
    #         comentario = st.text_area(f"Comentario: {row['_id']}")

    #         # Save the 'resena' and user information to the database
    #         resenas_col = db['resenas']
    #         resena_data = {
    #             'book_id': row['_id'],
    #             'user_id': user_id['_id'],
    #             'content': comentario
    #         }
    #         resenas_col.insert_one(resena_data)
