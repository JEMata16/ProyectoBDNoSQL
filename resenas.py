import streamlit as st
from mongo_utils import get_mongo_db
from libros import get_libros
from bson import ObjectId

db = get_mongo_db()

# Function to create a new reseña
def create_resena(user_id, book_id, rating, comment):
    # Save the data to the database
    resenas_col = db['resenas']
    resena_data = {
        'user_id': user_id,
        'book_id': book_id,
        'rating': rating,
        'comment': comment
    }
    resenas_col.insert_one(resena_data)

# Function to update an existing reseña
def update_resena(id, user_id, book_id, rating, comment):
    print('HOLAA')
    # Save the updated data to the database
    resenas_col = db['resenas']
    resena_data = {
        'user_id': user_id,
        'book_id': book_id,
        'rating': rating,
        'comment': comment
    }
    resenas_col.update_one({'_id': id}, {'$set': resena_data})

# Function to update a reseña with a form
def update_resena_form(resena_id):
    resenas_col = db['resenas']
    row = resenas_col.find_one({'_id': resena_id})
    print(row['_id'])
    with st.form(key='update_resena_form'):
        user_id = st.session_state.usuario  
        book_id = st.selectbox('Select book:', get_libros())
        rating = st.slider('Rating:', 1, 5, value=row['rating'])
        comment = st.text_area('Comment:', value=row['comment'])
        if st.form_submit_button("Confirm Update"):
            # Update the reseña when the button is clicked
            update_resena(id=row['_id'], user_id=user_id, book_id=book_id, rating=rating, comment=comment)

# Function to delete an existing reseña
def delete_resena(resena_id):
    resenas_col = db['resenas']
    resena = resenas_col.find_one({'_id': resena_id})

    if resena:
        resenas_col.delete_one({'_id': resena['_id']})
        print(f"Reseña {resena_id} deleted successfully.")
    else:
        print(f"Reseña {resena_id} not found.")

# Function to retrieve a list of resenas
def get_resenas():
    resenas_col = db['resenas']
    cursor = resenas_col.find({})
    resenas = [{'_id': resena['_id'], 'user_id': resena['user_id'], 'book_id': resena['book_id'], 'rating': resena['rating'], 'comment': resena['comment']} for resena in cursor]
    return resenas


def resenasApp():
    resena_operations = ['Create Reseña', 'Update Reseña', 'Delete Reseña']
    operation = st.selectbox('Select operation:', resena_operations)
    
    if operation == 'Create Reseña':
        # Collect the data for the new reseña
        user_id = st.session_state.usuario  # Assuming user_id is stored in the Streamlit session state
        book_id = st.selectbox('Select book:', get_libros())  # Assuming get_libros() returns a list of libros
        rating = st.slider('Rating:', 1, 5)
        comment = st.text_area('Comment:')
        
        create_resena_button = st.button("Confirm Creation")
        if create_resena_button:
            create_resena(user_id=user_id, book_id=book_id, rating=rating, comment=comment)
    
    elif operation == 'Update Reseña':
        # Retrieve the list of resenas
        resenas = get_resenas()
        # Create a dropdown menu to select the reseña to update
        resena_to_update = st.selectbox('Select reseña to update:', resenas)
        # Call the update_resena_form function with the selected reseña
        update_resena_button = st.button("Get form")
        
        if update_resena_button:
            update_resena_form(resena_id=ObjectId(resena_to_update['_id']))
    
    elif operation == 'Delete Reseña':
        # Retrieve the list of resenas
        resenas = get_resenas()
        # Create a dropdown menu to select the reseña to delete
        resena_to_delete = st.selectbox('Select reseña to delete:', resenas)
        # Call the delete_resena function with the selected reseña
        delete_resena_button = st.button("Confirm Deletion")
        
        if delete_resena_button:
            delete_resena(resena_id=resena_to_delete['_id'])
