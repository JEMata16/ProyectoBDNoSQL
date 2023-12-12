from pymongo import MongoClient
import streamlit as st
from bson import ObjectId


conn = st.secrets["mongo"]["connection_string"]
client = MongoClient(conn)
db = client['Biblioteca']
libros_col = db['libros']

book_id_to_update = ObjectId("6577a9aff673ea24e95bac14")


original_book = libros_col.find_one({'_id': book_id_to_update})
print("Libro original:", original_book)


new_title = "Libro actualizado"


libros_col.update_one({'_id': book_id_to_update}, {'$set': {'titulo': new_title}})

updated_book = libros_col.find_one({'_id': book_id_to_update})
print("Updated Book:", updated_book)


client.close()
