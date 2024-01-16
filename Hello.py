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

# week1data = pd.read_csv("week1picks.csv")
week1data = week1data.drop(['Old Record', 'Record', 'Old BB Rec', 'Best Bet Record'], axis=1)

# get counts for picks for each game
game_list = week1data.columns.values.tolist()
game_list = game_list[1:7]

# construct a df of picks for each game
game1df = pd.DataFrame({"Game 1": ['Browns -2.5', 'Texans +2.5'], 
                                    "counts": week1data["Browns vs. Texans (+2.5)"].value_counts()})
game2df = pd.DataFrame({"Game 2": ['Chiefs -4.5', 'Dolphins +4.5'], 
                                    "counts": week1data["Dolphins vs. Chiefs (-4.5)"].value_counts()})
game3df = pd.DataFrame({"Game 3": ['Cowboys -7.5', 'Packers +7.5'], 
                                    "counts": week1data["Packers vs. Cowboys (-7.5)"].value_counts()})
game4df = pd.DataFrame({"Game 4": ['Lions -3', 'Rams +3'], 
                                    "counts": week1data["Rams vs. Lions (-3)"].value_counts()})
game5df = pd.DataFrame({"Game 5": ['Steelers +10', 'Bills -10'], 
                                    "counts": week1data["Steelers vs. Bills (-10)"].value_counts()})
game6df = pd.DataFrame({"Game 6": ['Eagles -3', 'Buccaneers +3'], 
                                    "counts": week1data["Eagles vs. Buccaneers (+3)"].value_counts()})


# Game 1
fig1 = px.bar(game1df, x='Game 1', y='counts', text_auto=True)
fig1 = fig1.update_yaxes(visible=False)
fig1.update_layout(
font=dict(
    size=18,  # Set the font size here
    # color="RebeccaPurple"
))

# Game 2
fig2 = px.bar(game2df, x='Game 2', y='counts', text_auto=True)
fig2 = fig2.update_yaxes(visible=False)
fig2.update_layout(
font=dict(
    size=18,  # Set the font size here
    # color="RebeccaPurple"
))

# Game 3
fig3 = px.bar(game3df, x='Game 3', y='counts', text_auto=True)
fig3 = fig3.update_yaxes(visible=False)
fig3.update_layout(
font=dict(
    size=18,  # Set the font size here
    # color="RebeccaPurple"
))

# Game 4
fig4 = px.bar(game4df, x='Game 4', y='counts', text_auto=True)
fig4 = fig4.update_yaxes(visible=False)
fig4.update_layout(
font=dict(
    size=18,  # Set the font size here
    # color="RebeccaPurple"
))

# Game 5
fig5 = px.bar(game5df, x='Game 5', y='counts', text_auto=True)
fig5 = fig5.update_yaxes(visible=False)
fig5.update_layout(
font=dict(
    size=18,  # Set the font size here
    # color="RebeccaPurple"
))

# Game 6
fig6 = px.bar(game6df, x='Game 6', y='counts', text_auto=True)
fig6 = fig6.update_yaxes(visible=False)
fig6.update_layout(
font=dict(
    size=18,  # Set the font size here
    # color="RebeccaPurple"
))

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write(":balloon: # Welcome to Streamlit! 👋 This is Brian's first streamlit deployment")

    st.markdown("## Week 1 Picks")

    game_list


    st.markdown("## Week 1 \#data")
    left_column, middle_column, right_column = st.columns(3)
    

    with left_column:
        # st.dataframe(game1df, hide_index=True)
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig4, use_container_width=True)
    with middle_column:
        # st.dataframe(game3df, hide_index=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig5, use_container_width=True)
    with right_column:
        # st.dataframe(game5df, hide_index=True)
        st.plotly_chart(fig3, use_container_width=True)
        st.plotly_chart(fig6, use_container_width=True)
    

    # left_column, right_column = st.columns(2)
    # You can use a column just like st.sidebar:

    # left_column.button('Press me!')

    # # Or even better, call Streamlit functions inside a "with" block:
    # with right_column:
    #     chosen = st.radio(
    #         'Sorting hat',
    #         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    #     st.write(f"You are in {chosen} house!")

    # st.sidebar.success("Select a demo above.")

    # st.markdown(
    #     """
    #     Streamlit is an open-source app framework built specifically for
    #     Machine Learning and Data Science projects.
    #     **👈 Select a demo from the sidebar** to see some examples
    #     of what Streamlit can do!
    #     ### Want to learn more?
    #     - Check out [streamlit.io](https://streamlit.io)
    #     - Jump into our [documentation](https://docs.streamlit.io)
    #     - Ask a question in our [community
    #       forums](https://discuss.streamlit.io)
    #     ### See more complex demos
    #     - Use a neural net to [analyze the Udacity Self-driving Car Image
    #       Dataset](https://github.com/streamlit/demo-self-driving)
    #     - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    # """
    # )


if __name__ == "__main__":
    run()
