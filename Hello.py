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
import re

LOGGER = get_logger(__name__)

#########################################################################
# helper functions that create and format the charts given a df with picks
#########################################################################
def create_team_chart(df, color_mapping):
    def extract_team_name(team_str):
        match = re.match(r"^(.*?)\s[\+\-]", team_str)
        return match.group(1) if match else team_str

    def insert_line_breaks(team_str, max_chars_per_line=10):
        words = team_str.split()
        wrapped_str = ""
        current_line_length = 0

        for word in words:
            if current_line_length + len(word) > max_chars_per_line:
                wrapped_str += "<br>"
                current_line_length = 0
            wrapped_str += word + " "
            current_line_length += len(word) + 1

        return wrapped_str.strip()

    df['TeamName'] = df['Team'].apply(extract_team_name)
    df['WrappedTeamName'] = df['Team'].apply(insert_line_breaks)
    df['Color'] = df['TeamName'].map(color_mapping)

    # Extract team names for the title
    team1, team2 = df['TeamName'].iloc[0], df['TeamName'].iloc[1]
    chart_title = f"{team1} vs. {team2}"

    fig = go.Figure(data=[go.Bar(
        x=df['WrappedTeamName'],
        y=df['Picks'],
        marker_color=df['Color'],
        text=df['Picks'],  # Add data labels
        textposition='inside'  # Position labels outside the bars
    )])

    fig.update_layout(
        xaxis=dict(tickangle=0, automargin=True, tickfont=dict(size=10)),
        title=chart_title,
        # xaxis_title="Team",
        # yaxis_title="Count"
    )

    return fig


##########################################################################


# pre-formatting data
##########################################################################
week1picks_table = pd.read_csv("week1_picks_tableformat.csv")

# construct a df of picks for each game
game1df = week1picks_table.query("Game_num == 1").drop("Game_num", axis=1)
game2df = week1picks_table.query("Game_num == 2").drop("Game_num", axis=1)
game3df = week1picks_table.query("Game_num == 3").drop("Game_num", axis=1)
game4df = week1picks_table.query("Game_num == 4").drop("Game_num", axis=1)
game5df = week1picks_table.query("Game_num == 5").drop("Game_num", axis=1)
game6df = week1picks_table.query("Game_num == 6").drop("Game_num", axis=1)

# Read team colors
team_colors = pd.read_csv('team_colors.csv')
color_mapping = team_colors.set_index('NFL_Team_Name')['c1_new'].to_dict()


## streamlit page creation and layout
def run():
    st.set_page_config(
        page_title="2024 NFL Playoff Pick 'em",
        page_icon=":shark:",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.write("# 2024 NFL Pick'em Stats")

    st.markdown("""Thought it would be cool to visualize some of the picks from the crowd. This page will also contain the standings""")

    st.write("## Standings")

    # Your Google Sheet's shareable link
    sheet_url = "https://docs.google.com/spreadsheets/d/1NXYlv93aJpPzh4OaWP1pS2Sxm-iQdNVlss83yxbYYAk/gviz/tq?tqx=out:csv&sheet=Week1_Picks"

    sheet_df = pd.read_csv(sheet_url, nrows=50)

    # Read the online sheet into a DataFrame
    columns_to_keep = ["Name", "Record", "Best Bet Record"]
    df_filtered = sheet_df[columns_to_keep]


    # Use the data in your Streamlit app
    

    st.markdown("## Week 1 Picks")

    # sort games into columns
    left_dfs = [game1df, game4df]
    middle_dfs = [game2df, game5df]
    right_dfs = [game3df, game6df]


    # added v left col
    # display columns
    very_left_column, left_column, middle_column, right_column = st.columns(4)
    with very_left_column:
        st.dataframe(df_filtered, hide_index=True)
    with left_column:
        for df in left_dfs:
            fig = create_team_chart(df, color_mapping)
            st.plotly_chart(fig, use_container_width=True)
    with middle_column:
        for df in middle_dfs:
            fig = create_team_chart(df, color_mapping)
            st.plotly_chart(fig, use_container_width=True)
    with right_column:
        for df in right_dfs:
            fig = create_team_chart(df, color_mapping)
            st.plotly_chart(fig, use_container_width=True)
    


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
