import streamlit as st
from helpers import pandas_helpers as pdh, st_helpers as sth, charting_helpers as ch
import datetime
import pandas as pd


def handle_dates_checks():
        data = st.session_state.file_data
        date_col = st.session_state.date_col
        target_metric_col = st.session_state.target_metric_col
        regressor_cols = st.session_state.regressor_col_list


        # Handle date column
        data = pdh.check_and_convert_data(
            df = data, 
            date_col=date_col,
            target_col=target_metric_col,
            regressor_cols=regressor_cols
            )
        
        default_date = st.session_state.default_last_date_to_show-datetime.timedelta(days = 7)

        if "chosen_date" in st.session_state:
             default_date = st.session_state.chosen_date
        
        if st.session_state.data_checked:
            # Only continue if all the data checks are fine

            dates_expander = st.expander(label = "Choose test date", expanded=st.session_state.step == "dates")

            with dates_expander:

                st.session_state.chosen_date = st.date_input(
                        "Date when you made the change",
                        value = default_date,
                        min_value=st.session_state.default_first_date_to_show,
                        max_value=st.session_state.default_last_date_to_show,
                        disabled=st.session_state.step != "dates"
                        )
                
                if st.session_state.chosen_date!=default_date:
                    #  Forcing rerun so that chart always updates if date changed
                    st.experimental_rerun()

                    

                chosen_timestamp = datetime.datetime.combine(
                     st.session_state.chosen_date, datetime.time()
                     ).timestamp()
                
                chosen_timestamp = pd.Timestamp(
                     chosen_timestamp, unit='s')


                data["test_period"] = data["time"]>=chosen_timestamp

                pre_data = data[~data['test_period']]
                post_data = data[data['test_period']]
                

                fig = ch.line_plot_highlighting_missing_sections(
                    df = pre_data,
                    future_df=post_data,
                    date_col = date_col,
                    target_col = target_metric_col)
                
                st.plotly_chart(fig)
                
                continue_with_dates = st.button("Confirm")

                if continue_with_dates:
                    st.session_state.cleaned_data = data
                    sth.update_step_state(previous_step = "dates", new_step = "impact")