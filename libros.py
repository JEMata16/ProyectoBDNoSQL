import streamlit as st
from mongo_utils import get_mongo_db
db = get_mongo_db()

def get_libros():
    libros_col = db['libros']
    cursor = libros_col.find({})
    libros = [libro['titulo'] for libro in cursor]
    return libros

