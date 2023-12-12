import streamlit as st
from mongo_utils import get_mongo_db
from libros import get_libros
from bson import ObjectId
from datetime import datetime

db = get_mongo_db()

# Function to create a new reserva
def create_reserva(user_id, book_id, reservation_date):
    # Convert date object to datetime object
    reservation_date = datetime.combine(reservation_date, datetime.min.time())

    # Save the data to the database
    reservas_col = db['reservas']
    reserva_data = {
        'user_id': user_id,
        'book_id': book_id,
        'reservation_date': reservation_date
    }
    reservas_col.insert_one(reserva_data)

# Function to update an existing reserva
def update_reserva(reservation_id, user_id, book_id, reservation_date):
    # Convert date object to datetime object
    reservation_date = datetime.combine(reservation_date, datetime.min.time())

    # Save the updated data to the database
    reservas_col = db['reservas']
    reserva_data = {
        'user_id': user_id,
        'book_id': book_id,
        'reservation_date': reservation_date
    }
    reservas_col.update_one({'_id': reservation_id}, {'$set': reserva_data})

# Function to update a reserva with a form
def update_reserva_form(reservation_id):
    reservas_col = db['reservas']
    row = reservas_col.find_one({'_id': reservation_id})
    with st.form(key='update_reserva_form'):
        user_id = st.session_state.usuario
        book_id = st.selectbox('Select book:', get_libros())
        reservation_date = st.date_input('Reservation Date:', value=row['reservation_date'])
        if st.form_submit_button("Confirm Update"):
            # Update the reserva when the button is clicked
            update_reserva(reservation_id=reservation_id, user_id=user_id, book_id=book_id, reservation_date=reservation_date)

# Function to delete an existing reserva
def delete_reserva(reservation_id):
    reservas_col = db['reservas']
    reserva = reservas_col.find_one({'_id': reservation_id})

    if reserva:
        reservas_col.delete_one({'_id': reserva['_id']})
        print(f"Reserva {reservation_id} deleted successfully.")
    else:
        print(f"Reserva {reservation_id} not found.")

# Function to retrieve a list of reservas
def get_reservas():
    reservas_col = db['reservas']
    cursor = reservas_col.find({})
    reservas = [{'_id': reserva['_id'], 'user_id': reserva['user_id'], 'book_id': reserva['book_id'],
                 'reservation_date': reserva['reservation_date']} for reserva in cursor]
    return reservas


def reservasApp():
    reserva_operations = ['Create Reserva', 'Update Reserva', 'Delete Reserva']
    operation = st.selectbox('Select operation:', reserva_operations)

    if operation == 'Create Reserva':
        # Collect the data for the new reserva
        user_id = st.session_state.usuario
        book_id = st.selectbox('Select book:', get_libros())
        reservation_date = st.date_input('Reservation Date:')
        
        create_reserva_button = st.button("Confirm Creation")
        if create_reserva_button:
            create_reserva(user_id=user_id, book_id=book_id, reservation_date=reservation_date)

    elif operation == 'Update Reserva':
        # Retrieve the list of reservas
        reservas = get_reservas()
        # Create a dropdown menu to select the reserva to update
        reserva_to_update = st.selectbox('Select reserva to update:', reservas)
        # Call the update_reserva_form function with the selected reserva
        update_reserva_button = st.button("Get form")

        if update_reserva_button:
            update_reserva_form(reservation_id=ObjectId(reserva_to_update['_id']))

    elif operation == 'Delete Reserva':
        # Retrieve the list of reservas
        reservas = get_reservas()
        # Create a dropdown menu to select the reserva to delete
        reserva_to_delete = st.selectbox('Select reserva to delete:', reservas)
        # Call the delete_reserva function with the selected reserva
        delete_reserva_button = st.button("Confirm Deletion")

        if delete_reserva_button:
            delete_reserva(reservation_id=reserva_to_delete['_id'])
