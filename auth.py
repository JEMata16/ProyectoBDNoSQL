import streamlit as st
from mongo_utils import  get_userByName, insertNewUser


def loginPage():

    st.sidebar.empty().title('Login/Register')
    username_input = st.sidebar.text_input('Username')
    password_input = st.sidebar.text_input('Password', type='password')

    col1,col2,col3= st.sidebar.columns(3)
    if col2.button('Login') and username_input and password_input:
        login(username_input=username_input, password_input=password_input)
    elif col1.button('Register'):
        register(username_input, password_input)


def login(username_input, password_input):
    if username_input and password_input:
        user_data = get_userByName(username_input)
        
        if user_data and user_data['password'] == password_input:
            st.sidebar.success('Login successful!')
            st.session_state.usuario = user_data['username']
            return True
        else:
            st.sidebar.error('Invalid username or password')
            return False
    else:
        return False


def logout():
    if 'usuario' in st.session_state:
        st.sidebar.write(f'Logged in as {st.session_state.usuario}')
        if st.sidebar.button('Logout'):
            st.session_state.pop('usuario')


def register(username_input, password_input):
    user_data = get_userByName(username_input)
    if(user_data['username'] == username_input):
        st.sidebar.error("Ya éxiste un usuario con ese nombre, intentalo de nuevo")
    else:
        insertNewUser( user_id=username_input, user_pass=password_input)
    
