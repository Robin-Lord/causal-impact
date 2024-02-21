import streamlit as st
from helpers import pandas_helpers as pdh
import pandas as pd

def add_accordion():
    # File uploader
    upload_expander = st.expander(label = "Upload file", expanded=st.session_state.step == "upload")
    with upload_expander:
        if st.session_state.uploaded_file == None:
            st.session_state.uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            st.session_state.data_checked = False
        else:
            st.write(f"Uploaded file: {st.session_state.uploaded_file}")


def display_uploaded_file():


        # Reset upload section
    if st.session_state.step == "upload":
        st.session_state.step = "columns"

    
        # Read file
        data = pd.read_csv(st.session_state.uploaded_file)

        # Check it has the right columns
        pdh.check_columns(data)

        st.session_state.file_data = data

        print(st.session_state)

        st.experimental_rerun()
    
    data_display_expander = st.expander(label = "Data preview", expanded=st.session_state.step == "columns")
    with data_display_expander:
        # Read and display the data
        data = st.session_state.file_data
        st.write("""### Example top and bottom rows of your CSV:
    Use these to make sure everything looks right.             

    *First 5rows:*
                """)
        st.write(data.head())
        st.write("*Last 5 rows:*")
        st.write(data.tail())