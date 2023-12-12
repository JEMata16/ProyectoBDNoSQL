import streamlit as st
from mongo_utils import get_mongo_db
from libros import get_libros
from bson import ObjectId
import datetime
from datetime import date
import time

db = get_mongo_db()

# Function to create a new prestamo
def create_prestamo(user_id, book_id, loan_date, return_date):
    # Save the data to the database
    prestamos_col = db['prestamos']
    prestamo_data = {
        'user_id': user_id,
        'book_id': book_id,
        'loan_date': loan_date,
        'return_date': return_date
    }
    prestamos_col.insert_one(prestamo_data)

# Function to update an existing prestamo
def update_prestamo(id, user_id, book_id, loan_date, return_date):
    # Save the updated data to the database
    prestamos_col = db['prestamos']
    prestamo_data = {
        'user_id': user_id,
        'book_id': book_id,
        'loan_date': loan_date,
        'return_date': return_date
    }
    prestamos_col.update_one({'_id': id}, {'$set': prestamo_data})

# Function to update a prestamo with a form
def update_prestamo_form(prestamo_id):
    prestamos_col = db['prestamos']
    row = prestamos_col.find_one({'_id': prestamo_id})
    with st.form(key='update_prestamo_form'):
        user_id = st.session_state.usuario 
        book_id = st.selectbox('Select book:', get_libros())
        loan_date = st.date_input('Loan Date:', value=datetime.datetime.strptime(row['loan_date'], '%Y-%m-%d').date(), min_value=date.today())
        return_date = st.date_input('Return Date:', value=datetime.datetime.strptime(row['return_date'], '%Y-%m-%d').date(), min_value=date.today())
        if st.form_submit_button("Confirm Update"):
            # Update the prestamo when the button is clicked
            update_prestamo(id=row['_id'], user_id=user_id, book_id=book_id, loan_date=loan_date.isoformat, return_date=return_date.isoformat)

# Function to delete an existing prestamo
def delete_prestamo(prestamo_id):
    prestamos_col = db['prestamos']
    prestamo = prestamos_col.find_one({'_id': prestamo_id})

    if prestamo:
        prestamos_col.delete_one({'_id': prestamo['_id']})
        print(f"Prestamo {prestamo_id} deleted successfully.")
    else:
        print(f"Prestamo {prestamo_id} not found.")

# Function to retrieve a list of prestamos
def get_prestamos():
    prestamos_col = db['prestamos']
    cursor = prestamos_col.find({})
    prestamos = [{'_id': prestamo['_id'], 'user_id': prestamo['user_id'], 'book_id': prestamo['book_id'],
                  'loan_date': prestamo['loan_date'], 'return_date': prestamo['return_date']} for prestamo in cursor]
    return prestamos


def prestamosApp():
    prestamo_operations = ['Create Prestamo', 'Update Prestamo', 'Delete Prestamo']
    operation = st.selectbox('Select operation:', prestamo_operations)
    
    if operation == 'Create Prestamo':
        # Collect the data for the new prestamo
        today = date.today()
        user_id = st.session_state.usuario 
        book_id = st.selectbox('Select book:', get_libros())
        loan_date = st.date_input('Loan Date:', min_value=today)
        return_date = st.date_input('Return Date:')
        
        create_prestamo_button = st.button("Confirm Creation")
        if create_prestamo_button:
            create_prestamo(user_id=user_id, book_id=book_id, loan_date=loan_date.isoformat(), return_date=return_date.isoformat())
    
    elif operation == 'Update Prestamo':
        # Retrieve the list of prestamos
        prestamos = get_prestamos()
        # Create a dropdown menu to select the prestamo to update
        prestamo_to_update = st.selectbox('Select prestamo to update:', prestamos)
        # Call the update_prestamo_form function with the selected prestamo
        update_prestamo_button = st.button("Get form")
        
        if update_prestamo_button:
            print(ObjectId(prestamo_to_update['_id']))
            update_prestamo_form(prestamo_id=ObjectId(prestamo_to_update['_id']))
    
    elif operation == 'Delete Prestamo':
        # Retrieve the list of prestamos
        prestamos = get_prestamos()
        # Create a dropdown menu to select the prestamo to delete
        prestamo_to_delete = st.selectbox('Select prestamo to delete:', prestamos)
        # Call the delete_prestamo function with the selected prestamo
        delete_prestamo_button = st.button("Confirm Deletion")
        
        if delete_prestamo_button:
            delete_prestamo(prestamo_id=prestamo_to_delete['_id'])
