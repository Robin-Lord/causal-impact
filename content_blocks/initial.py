
import streamlit as st
import pandas as pd
from helpers import st_helpers as sth

from ga4py.custom_arguments import MeasurementArguments

def set_variables():
    # Set session states to track which part of the process we're in
    if "step" not in st.session_state:
        # Step defaults
        st.session_state.step = "upload"

        # Flag for if file uploaded
        st.session_state.uploaded_file = None
        st.session_state.file_data = None

        # Column defaults
        st.session_state.date_col = None
        st.session_state.target_metric_col = None
        st.session_state.regressor_col_list = None
        st.holiday_country = "None"

        st.session_state.ci = None

        # Add tracking arguments to be referenced throughout the script
        basic_tracking_info: MeasurementArguments = {
            # "testing_mode": True,
            "page_location": "python_causal_impact", 
            "page_title": "python causal impact", 
        }
        st.session_state.basic_tracking_info = basic_tracking_info



def add_content():

    st.title("Impact Measurement Tool")

    st.image("assets/aira_logo.png", caption='Aira Digital Marketing', width=150)



    st.markdown("""# Aira's Causal Impact running tool
                                    
Welcome to Aira's Causal Impact tool!
                
Use this tool to run Causal Impact over your data and test whether a change had a positive/ negative/ undetermined impact. 
                
Upload a CSV file with a column of dates, a column showing the metric you think you've impacted, and a "regressor" column.
                """)
    
    what_is = st.expander(label="What is this tool and what is it for?", expanded = False)
    with what_is:
        st.markdown("""## What is this tool and what is it for?""")           

        st.markdown(                    
"""This is a forecasting tool based on [Google's Causal Impact](https://facebook.github.io/prophet/).
                    

It uses Machine Learning to look at your historic data, and estimate whether a change you made was positive, negative, or undetermined.
                    
Tools like Causal Impact are a very powerful way to measure change when you know you can't just trust cookie-based tracking, and you are dealing with things like complex seasonal effects.

Like if your business is growing year-on-year, you're running sales, you're going into summer, and you still want to understand if your work has had a positive impact, rather than it just being a combination of those things that means the numbers would go up anyway.

It's also useful if, for example, you did good work in a market that's declining (in which case 'better performance' could look like the line staying flat).
""")
        

        st.image("assets/causal-impact-example-charts.png")
        st.markdown("Image from the [Causal Impact web page](https://google.github.io/CausalImpact/CausalImpact.html)")
        st.markdown("""                    
                    

Causal Impact compares actual performance to what we would normally expect performance to be, using Machine Learning.

By doing that comparison we can see if the actual performance is higher, lower, or about the same as what we'd expect.
                    
Then we can use the library to estimate *how much* better or worse our actual performance is, in comparison to expectations, so we can estimate what size of positive or negative impact our change had on the business.

""")
        st.markdown("""

This tool was created by the Aira Innovations team.
                    
Thanks for reading! Lots of love
                    
**Aira Innovation Team**
                    
                    """)
        
        # Create two columns for the bios
        d, r = st.columns(2)

        with d:
            st.image("assets/David-Westby.jpg")
            st.markdown("""
**[David Westby](https://www.linkedin.com/in/dawestby/)**
                        
*Senior Data and Insights Consultant*.
                        
                        """)            
            
        with r:
            st.image("assets/Robin.jpg")
            st.markdown("""
**[Robin Lord](https://www.linkedin.com/in/robin-lord-9906b85a/)**
                        
*Assoc. Director of Innovations*
                                            
Developed this tool.
                        
                        """)
            
    

    what_do_i_need = st.expander(label="What do I need to do?", expanded = False)
    with what_do_i_need:
        st.markdown("""## What do I need to do?

Upload a CSV file which has at least three columns:
                    
|     Date                   | Target column (Historic data for whatever number you want to impact)  | At least one 'Regressor' column (explanation below )  |
|----------------------------|-------------------------------------------------------|-------------------------------------------------------|
| {date in yyyy-mm-dd format}|    (always a number, can be whole number or decimal)   |    (always a number, can be whole number or decimal)   |
| {date in yyyy-mm-dd format}|    (always a number, can be whole number or decimal)   |    (always a number, can be whole number or decimal)   |
| {date in yyyy-mm-dd format}|    (always a number, can be whole number or decimal)   |    (always a number, can be whole number or decimal)   |

                    
- You can call your date column, target number column, and regressor columns whatever you want, you will have a chance to select them once you've uploaded your data
- You have to have a valid yyyy-mm-dd date in every single row
- You must have a row for every single date between your start date and end date (so you can't go from 11 June 2024 to 14 June 2024)
- You must fill out every row of your target metric and regressor columns


### Regressors                    

In this case, 'Regressors' are just a fancy way of saying "a number which should show similar patterns to my target metric, but isn't affected by this change.

For example - if you think you made a change that drove more non-brand traffic to the website, you could use daily branded impressions as a regressor. If overall interest in your industry or brand went up, you would *normally* expect site traffic *and* brand searches to both go up. If that happens then Causal Impact will be able to better identify that your change isn't responsible for all of increase in site traffic. 
                    
If, on the other hand, your number goes up a bit but branded impressions go *down* by a lot, that could help Causal Impact identify that your change may have had *even more* positive impact than it looks. Because your traffic went up *even though* interest in your industry went down, so if everything had been equal you could have seen an even bigger uplift in site traffic (and if you hadn't made the change your testing, you might have seen big losses).                     
                    
There are multiple ways to add in regressors, they can be traffic or impressions numbers, or could be as simple as just 1s and 0s. It's worth putting some thought into what regressors you'll use.
                    
A dataframe with regressors might look something like this:

                    
|     Date                   | Historic data for whatever number you want to forecast|   regressor_1  | regressor_2  |
|----------------------------|-------------------------------------------------------|----------------|--------------|
| {date in yyyy-mm-dd format}|    (always a number, can be whole number or decimal)   |      1         |      0       |
| {date in yyyy-mm-dd format}|    (always a number, can be whole number or decimal)   |      1         |      0       |
| {date in yyyy-mm-dd format}|    (always a number, can be whole number or decimal)   |      1         |      0       |
| {date in yyyy-mm-dd format}|    (always a number, can be whole number or decimal)   |      0         |      10      |
| {date in yyyy-mm-dd format}|    (always a number, can be whole number or decimal)   |      0         |      5       |
| {date in yyyy-mm-dd format}|    (always a number, can be whole number or decimal)   |      0         |      5       |
| {date in yyyy-mm-dd format}|                                                       |      1         |      0       |
| {date in yyyy-mm-dd format}|                                                       |      1         |      0       |
| {date in yyyy-mm-dd format}|                                                       |      1         |      0       |
| {date in yyyy-mm-dd format}|                                                       |      1         |      0       |
| {date in yyyy-mm-dd format}|                                                       |      1         |      0       |                    
                    

                    
**If you want to see some example data you can use - check out the "Example Data" tab below.**
                    
                    """)
    example_data_tab = st.expander(label="Example data", expanded = False)
    with example_data_tab:

        st.markdown("""## Example Data""")

        example_data = pd.read_csv("tests/test_files/example_data_for_users.csv")

        st.write(example_data.head())

        example_csv = sth.convert_df(example_data)   

        st.markdown("""

If you want some example data to get started with/play around with - feel free to download and use this example data.""")
                    
        st.download_button(
        f"Download example data",
        example_csv,
        f"Example data for impact.csv",
        f"Example data for impact/csv",
        key='download-example-csv'
        )

        st.markdown("""
                    
Download it here and then upload it to the tool below to begin.

If you need more information about how exactly you use this tool, check out the "What do I need to do?" section above.
""")


        
    easier_way = st.expander(label="I'm not sure what I'm doing, is there an easier way?", expanded = False)
    with easier_way:
        st.markdown("""## This seems complicated, is there an easier way?
                    
You have a couple of options:
                    
1. You could **[work with Aira!](https://www.aira.net/)** we don't do impact measurement as a stand alone service but if you're planning marketing activity we can help you plan it and, as part of that, we'll do much more advanced forecasting than this (which includes things like expected impact from different activity).

2. You could try other tools, i.e. Greg Bernhart's [Search Console focused impact tester](https://dethfire-causalimpact-causalimpact-app-3fpnwm.streamlit.app/).
                    """)
