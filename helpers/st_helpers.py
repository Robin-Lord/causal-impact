import streamlit as st
import os
import ga4py.add_tracker as add_tracker
from ga4py.custom_arguments import MeasurementArguments


@add_tracker.analytics_hit_decorator
def update_step(new_step):
    st.session_state.step = new_step
    st.experimental_rerun()

def update_step_state(
        previous_step: str,
        new_step: str
    ):
    if st.session_state.step == previous_step:
        # Add tracking at each point of the process        
        tracking_args_dict: MeasurementArguments = st.session_state.basic_tracking_info
        tracking_args_dict["skip_stage"] = ["start", "end"]
        tracking_args_dict["stage"] = new_step

        update_step(new_step=new_step,
                    ga4py_args_remove = tracking_args_dict)

def continue_or_reset(message = ""):
    # Auto testing flag that lets us choose these choices
    auto_yes_no = os.getenv("AUTO_YES_NO")

    # Yes/No buttons
    st.write(message)
    if st.button('Yes') or auto_yes_no == "yes":
        st.write('You selected "Yes" - continuing.')
        return True
    elif st.button('No') or auto_yes_no == "no":
        raise ValueError("You selected 'no' meaning you don't want to continue - please refresh the page")
    

@st.experimental_memo
def convert_df(df, index = False):
   return df.to_csv(index=index).encode('utf-8')

