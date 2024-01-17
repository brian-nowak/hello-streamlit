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

# pre-formatting data
week1data = pd.read_csv("week1picks.csv")
week1picks_table = pd.read_csv("week1_picks_tableformat.csv")

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
game1df = week1picks_table.query("Game_num == 1").drop("Game_num", axis=1)
game2df = week1picks_table.query("Game_num == 2").drop("Game_num", axis=1)
game3df = week1picks_table.query("Game_num == 3").drop("Game_num", axis=1)
game4df = week1picks_table.query("Game_num == 4").drop("Game_num", axis=1)
game5df = week1picks_table.query("Game_num == 5").drop("Game_num", axis=1)
game6df = week1picks_table.query("Game_num == 6").drop("Game_num", axis=1)


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
        marker_color=df['Color']
    )])

    fig.update_layout(
        xaxis=dict(tickangle=0, automargin=True, tickfont=dict(size=10)),
        title=chart_title,
        # xaxis_title="Team",
        # yaxis_title="Count"
    )

    return fig




##########################################################################

# # Function to extract the team name
# def extract_team_name(team_str):
#     match = re.match(r"^(.*?)\s[\+\-]", team_str)
#     return match.group(1) if match else team_str

# # Function to insert line breaks for wrapping
# def insert_line_breaks(team_str, max_chars_per_line=10):
#     words = team_str.split()
#     wrapped_str = ""
#     current_line_length = 0

#     for word in words:
#         if current_line_length + len(word) > max_chars_per_line:
#             wrapped_str += "<br>"  # Line break
#             current_line_length = 0
#         wrapped_str += word + " "
#         current_line_length += len(word) + 1  # +1 for space

#     return wrapped_str.strip()

# Read team colors
team_colors = pd.read_csv('team_colors.csv')
color_mapping = team_colors.set_index('NFL_Team_Name')['c1_new'].to_dict()

# # extract team name for color mapping
# game1df['TeamName'] = game1df['Team'].apply(extract_team_name)
# # wrap team name for display purposes
# game1df['WrappedTeamName'] = game1df['Team'].apply(insert_line_breaks)
# # Map team names to colors
# game1df['Color'] = game1df['TeamName'].map(color_mapping)



# Game 1

# # Create Plotly bar chart
# fig = go.Figure(data=[go.Bar(
#     x=game1df['WrappedTeamName'],
#     y=game1df['Picks'],
#     marker_color=game1df['Color']
# )])

# # Adjust layout for wrapped text
# fig.update_layout(
#     xaxis=dict(
#         tickangle=0,  # Set tick angle to 0 for horizontal text
#         automargin=True,  # Ensure automatic margin adjustment
#         tickfont=dict(size=10)  # You can adjust the font size if necessary
#     ) #,
#     # title="Team Counts",
#     # xaxis_title="Team",
#     # yaxis_title="Count"
# )

# Game 2
fig2 = px.bar(game2df, x='Team', y='Picks', text_auto=True)
fig2 = fig2.update_yaxes(visible=False)
fig2.update_layout(
font=dict(
    size=18,  # Set the font size here
    # color="RebeccaPurple"
))

# Game 3
fig3 = px.bar(game3df, x='Team', y='Picks', text_auto=True)
fig3 = fig3.update_yaxes(visible=False)
fig3.update_layout(
font=dict(
    size=18,  # Set the font size here
    # color="RebeccaPurple"
))

# Game 4
fig4 = px.bar(game4df, x='Team', y='Picks', text_auto=True)
fig4 = fig4.update_yaxes(visible=False)
fig4.update_layout(
font=dict(
    size=18,  # Set the font size here
    # color="RebeccaPurple"
))

# Game 5
fig5 = px.bar(game5df, x='Team', y='Picks', text_auto=True)
fig5 = fig5.update_yaxes(visible=False)
fig5.update_layout(
font=dict(
    size=18,  # Set the font size here
    # color="RebeccaPurple"
))

# Game 6
fig6 = px.bar(game6df, x='Team', y='Picks', text_auto=True)
fig6 = fig6.update_yaxes(visible=False)
fig6.update_layout(
font=dict(
    size=18,  # Set the font size here
    # color="RebeccaPurple"
))

def run():
    st.set_page_config(
        page_title="2024 NFL Playoff Pick 'em",
        page_icon="👋",
        layout="wide"
    )

    st.write(":balloon: # Welcome to Streamlit! 👋 This is Brian's first streamlit deployment")

    st.markdown("## Week 1 Picks")

    # game_list
    
    # Assuming game1df, game2df, ..., game6df are your DataFrames
    left_dfs = [game1df, game4df]
    middle_dfs = [game2df, game5df]
    right_dfs = [game3df, game6df]

    # dataframes = [game1df, game2df, game3df, game4df, game5df, game6df]

    # for df in dataframes:
    #     fig = create_team_chart(df, color_mapping)
    #     st.plotly_chart(fig)


    st.markdown("## Week 1 \#data")
    left_column, middle_column, right_column = st.columns(3)
    

    with left_column:
        # st.dataframe(game1df, hide_index=True)
        # st.plotly_chart(fig1, use_container_width=True)
        # st.plotly_chart(fig4, use_container_width=True)
        for df in left_dfs:
            fig = create_team_chart(df, color_mapping)
            st.plotly_chart(fig, use_container_width=True)
    with middle_column:
        # st.dataframe(game3df, hide_index=True)
        # st.plotly_chart(fig2, use_container_width=True)
        # st.plotly_chart(fig5, use_container_width=True)
        for df in middle_dfs:
            fig = create_team_chart(df, color_mapping)
            st.plotly_chart(fig, use_container_width=True)
    with right_column:
        # st.dataframe(game5df, hide_index=True)
        # st.plotly_chart(fig3, use_container_width=True)
        # st.plotly_chart(fig6, use_container_width=True)
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
