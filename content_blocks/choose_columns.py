import streamlit as st
from helpers import pandas_helpers as pdh, st_helpers as sth

def show_column_choosers():
    data = st.session_state.file_data


    # Logic for choosing columns
    if "date_col_index" not in locals():
        # Only set these if needed to avoid dropdown update issues
        (
            default_date_col, 
            date_col_index,
            target_metrics_options, 
            default_target_metric_col, 
            target_metric_col_index,
            regressor_options, 
            default_regressor_cols,
            ) = pdh.choose_columns(df = st.session_state.file_data) 
        

    # Show column choosers
    columns_expander = st.expander(label= "Select columns", expanded=st.session_state.step == "columns")

    with columns_expander:
        # Selection for Date column
        st.session_state.date_col = st.selectbox("""Select the Date column (by default will select any column called 'Date'):""", 
                                        options=data.columns, 
                                        index=date_col_index, 
                                        disabled=st.session_state.step != "columns"
                                        )
        
        date_col = st.session_state.date_col

        # Selection for Target Metric column
        st.session_state.target_metric_col = st.selectbox("Select the Target Metric column:", 
                                        options=target_metrics_options, 
                                        index= target_metric_col_index, 
                                        disabled=st.session_state.step != "columns"
                                        )
        
        target_metric_col = st.session_state.target_metric_col

        # Selection for Regressor columns
        st.session_state.regressor_col_list = st.multiselect("Select Regressor columns:", 
                                        options=regressor_options,
                                        default=default_regressor_cols, 
                                        disabled=st.session_state.step != "columns"
                                        )
        
        regressor_cols = st.session_state.regressor_col_list

        
        # Could include holidays here but not going to worry about that level of complexity right now

        
        # Force state update to flush through change 
        # (streamlit seems to need a second) update
        if (
            st.session_state.date_col != default_date_col
            or 
            st.session_state.target_metric_col != default_target_metric_col
            or 
            st.session_state.regressor_col_list != default_regressor_cols
            ):

            print(f"""
st.session_state.date_col != default_date_col: {st.session_state.date_col != default_date_col}
st.session_state.target_metric_col != default_target_metric_col: {st.session_state.target_metric_col != default_target_metric_col}
st.session_state.regressor_col_list != default_regressor_cols: {st.session_state.regressor_col_list != default_regressor_cols}
""")
            st.experimental_rerun()


        # Display chosen categories
        st.write("You categorized the columns as follows:")
        st.write(f"Date column: {date_col}")
        st.write(f"Target Metric column: {target_metric_col}")
        st.write(f"Regressor columns: {', '.join(regressor_cols) if regressor_cols else 'None'}")

        # Display button to submit data
        user_clicks_submit = st.button("Submit")
        if user_clicks_submit:
            if regressor_cols ==[]:
                st.warning('You need to include at least one regressor column. Please add one and try again', icon="⚠️")
            else: 
                st.session_state.columns_chosen=True
                sth.update_step_state(previous_step = "columns", new_step = "dates")
        
        return data, date_col, target_metric_col, regressor_cols