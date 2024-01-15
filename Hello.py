# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go



LOGGER = get_logger(__name__)

# pre-formatting data
week1data = pd.read_csv("week1picks.csv")

# from prompt: turn first row of pandas dataframe into headers
# also drop a few unnecessary cols
# week1data.columns = week1data.iloc[0]
# week1data = week1data.drop(0)
# week1data = week1data.drop(['Timestamp', 'Best Bet', ''], axis=1)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write(":balloon: # Welcome to Streamlit! 👋 This is Brian's first streamlit deployment")

    st.markdown("## Week 1 Picks")

    week1data = pd.read_csv("week1picks.csv")
    week1data = week1data.drop(['Old Record', 'Record', 'Old BB Rec', 'Best Bet Record'], axis=1)
    week1data

    st.markdown("## Week 1 \#data")

    game1df = week1data['Browns vs. Texans (+2.5)'].value_counts().astype(int).to_frame()
    test_data = pd.DataFrame({"Game 1": ['Browns -2.5', 'Texans +2.5'],
                          "counts": [36, 14]})

    st.markdown("Plotly chart")

    fig = px.bar(test_data, x='Game 1', y='counts', text_auto=True)
    fig = fig.update_yaxes(visible=False)
    fig.update_layout(
    font=dict(
        size=18,  # Set the font size here
        # color="RebeccaPurple"
    ))
    
    st.plotly_chart(fig)

    st.write(game1df)

    # game1df = pd.Series(week1data['Browns vs. Texans (+2.5)'].value_counts())
    # st.write(game1df)

    # chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])


    # st.bar_chart(test_data, x='counts', y='pick')

    base = (
      alt.Chart(test_data)
      .mark_bar()
      .encode( # x="counts", y="pick")
      x=alt.X('counts', axis=alt.Axis(title=None)),
      y=alt.Y('Game 1', axis=alt.Axis(title=None)),
    ))

#     c = base.mark_bar() # + base.mark_text(align='left', dx=2)
    # st.write(type(base.mark_bar()))
    st.altair_chart(base) #, use_container_width=True)

    left_column, right_column = st.columns(2)
    # You can use a column just like st.sidebar:
    left_column.button('Press me!')

    # Or even better, call Streamlit functions inside a "with" block:
    with right_column:
        chosen = st.radio(
            'Sorting hat',
            ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
        st.write(f"You are in {chosen} house!")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )


if __name__ == "__main__":
    run()
