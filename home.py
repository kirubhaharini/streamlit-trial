import streamlit as st

def app():
    st.title('Home')

    st.write('This is the `home page` of this multi-page app.')

    st.write('In this app, we will be building a simple classification model using the Iris dataset.')
    hashtag_filter = st.sidebar.multiselect(
    'Select hashtag',
    options=['1','3']
)