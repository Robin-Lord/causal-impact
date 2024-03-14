import css_and_styling
import streamlit as st
from content_blocks import initial, file_upload, choose_columns, choose_dates, show_impact_estimate
import logging

import ga4py.add_tracker as add_tracker
from ga4py.custom_arguments import MeasurementArguments

@add_tracker.analytics_hit_decorator
def main() -> None:

    # Handle initial variable setup
    initial.set_variables()

    # Add styling and initial content above accordions
    css_and_styling.add_custom_css()
    initial.add_content()

    # Add tool to upload data
    file_upload.add_accordion()

    # Handle uploaded data
    if st.session_state.uploaded_file is not None:
        file_upload.display_uploaded_file()
        choose_columns.show_column_choosers()

    if "columns_chosen" in st.session_state:
        choose_dates.handle_dates_checks()

    if "cleaned_data" in st.session_state:

        show_impact_estimate.display_impact_estimate()

    







if __name__ == "__main__":
    try:
        # Add tracking
        tracking_args_dict: MeasurementArguments = {
            # "testing_mode": True,
            "page_location": "python_causal_impact", 
            "page_title": "python causal impact", 
            "skip_stage": ["start", "end"],
            "logging": "all"
        }
        main(ga4py_args_remove = tracking_args_dict)
    except Exception as e:
        # Log the full traceback to console or a file
        logging.error("An exception occurred", exc_info=True)

        # Display a user-friendly error message
        st.error(e)