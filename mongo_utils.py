from pymongo import MongoClient
import streamlit as st

# Connect to MongoDB
def get_mongo_db():
    conn = st.secrets["mongo"]["connection_string"]
    client = MongoClient(conn)
    db = client['Biblioteca']
    return db

def get_userByName(user_id):
    db = get_mongo_db()
    users_col = db['usuarios']
    user_data = users_col.find_one({'username': user_id})
    if user_data:
        return user_data
    return None

def get_userById(user_id):
    db = get_mongo_db()
    users_col = db['usuarios']
    user_data = users_col.find_one({'_id': user_id})
    if user_data:
        return user_data
    return None

def insertNewUser(user_id, user_pass):
    db = get_mongo_db()
    users_col = db['usuarios']
    users_col.insert_one({'username': user_id, 'password': user_pass})



