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
from vega_datasets import data


LOGGER = get_logger(__name__)

#########################################################################
# helper functions that create and format the charts given a df with picks
#########################################################################
def create_team_chart(df, color_mapping,chart_title=None):
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
    if chart_title:
        pass
    else:
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


# Your Google Sheet's shareable link
# sheet_url = "https://docs.google.com/spreadsheets/d/1NXYlv93aJpPzh4OaWP1pS2Sxm-iQdNVlss83yxbYYAk/gviz/tq?tqx=out:csv&sheet=Week1_Picks"
golf_sheet_url = "https://docs.google.com/spreadsheets/d/1dyLJ7Z_o_vAT9ZlZqDRw-MLlxDTU6nps7EnF560Xoc4/gviz/tq?tqx=out:csv&sheet=Scoring"

golf_sheet_df = pd.read_csv(golf_sheet_url, nrows=8)

# summarize current total team points
pts_summary = golf_sheet_df.groupby('team')['total_pts'].agg('sum').reset_index()
pts_summary.insert(loc=2, column='pts_available', value=15)


# getting week 2 picks
sheet_url2 = "https://docs.google.com/spreadsheets/d/1NXYlv93aJpPzh4OaWP1pS2Sxm-iQdNVlss83yxbYYAk/gviz/tq?tqx=out:csv&sheet=Week2_Picks"
week2_sheet_df = pd.read_csv(sheet_url2, nrows=49)
week2_columns_to_keep = ["Name", "Texans vs. Ravens (-9.5)","Packers vs. 49ers (-9.5)",	"Bucs vs. Lions (-6.5)", "Chiefs vs. Bills (-2.5)", "Best Bet"]
week2_df_filtered = week2_sheet_df[week2_columns_to_keep]

# week 2 standings
columns_to_keep = ["Name", "Record", "Best Bet Record", "Pts"]
df_filtered = week2_sheet_df[columns_to_keep]
# Create a display DataFrame without the 'Score' column
df_sorted = df_filtered.sort_values(by='Pts', ascending=False)
df_display = df_sorted.rename(columns={'Pts': 'Pts (for sorting)'})

# Columns of interest
columns = ["Texans vs. Ravens (-9.5)", "Packers vs. 49ers (-9.5)", "Bucs vs. Lions (-6.5)", "Chiefs vs. Bills (-2.5)", "Best Bet"]

# Summarize each column
# Generate summaries for each column
summaries = {col: week2_df_filtered[col].value_counts().rename_axis('Team').reset_index(name='Picks') for col in columns}
# gm1_smry = summaries['Texans vs. Ravens (-9.5)']

##########################################################################
# streamlit page creation and layout
##########################################################################

def run():
    st.set_page_config(
        page_title="2024 Dudes Golf Trip",
        page_icon=":golf:",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    ##########################################################################
    # Golf data
    ##########################################################################

    st.write("# Golf data")
    st.dataframe(golf_sheet_df)


    st.dataframe(pts_summary)

    st.write("### Plotly")
    # Create two columns for the charts
    col1, col2 = st.columns(2)

    # Function to create a chart for a team
    def create_team_chart(team_data, right_aligned=False):
        fig = go.Figure()
        
        total_width = team_data['total_pts'] + team_data['pts_available']

        # Set colors based on team
        if team_data['team'] == 'Guys':
            total_pts_color = 'dodgerblue'
        elif team_data['team'] == 'Dudes':
            total_pts_color = 'forestgreen'
        else:
            total_pts_color = 'purple'  # Default color if neither Guys nor Dudes
        
        available_pts_color = 'lightgray'
        
        if right_aligned:
            # For right-aligned chart
            fig.add_trace(go.Bar(
                y=[''],
                x=[team_data['pts_available']],
                width=0.1,
                name='Available Points',
                orientation='h',
                marker=dict(color=available_pts_color)
            ))
            fig.add_trace(go.Bar(
                y=[''],
                x=[team_data['total_pts']],
                width=0.1,
                name='Total Points',
                orientation='h',
                marker=dict(color=total_pts_color)
            ))
            x_range = [0, total_width]
        else:
            # For left-aligned chart
            fig.add_trace(go.Bar(
                y=[''],
                x=[team_data['total_pts']],
                width=0.1,
                name='Total Points',
                orientation='h',
                marker=dict(color=total_pts_color)
            ))
            fig.add_trace(go.Bar(
                y=[''],
                x=[team_data['pts_available']],
                width=0.1,
                name='Available Points',
                orientation='h',
                marker=dict(color=available_pts_color)
            ))
            x_range = [total_width, 0]  # Reverse the x-axis

        fig.update_layout(
            # title=f"Points for {team_data['team']}",
            barmode='stack',
            height=120,  # You can adjust this value
            showlegend=False,
            # xaxis=dict(range=x_range, autorange=False),
            margin=dict(l=1, r=1, t=1, b=1)  # Reduce margins
    )
        
        return fig

    # Inject custom CSS to reduce gap between columns
    st.markdown("""
    <style>
        .stColumn {
            padding: 0px 0px 0px 0px;
        }
    </style>
    """, unsafe_allow_html=True)


    # Create and display left-aligned chart for Dudes
    with col1:
        st.write("## Guys")
        guys_data = pts_summary[pts_summary['team'] == 'Guys'].iloc[0]
        st.plotly_chart(create_team_chart(guys_data, right_aligned=False), use_container_width=True)

    # Create and display right-aligned chart for Guys
    with col2:
        st.write("## Dudes")
        dudes_data = pts_summary[pts_summary['team'] == 'Dudes'].iloc[0]
        st.plotly_chart(create_team_chart(dudes_data, right_aligned=True), use_container_width=True)

    st.write("## Latest version here - using st.plotly_chart()")

    # Create two columns for the charts
    col1, col2 = st.columns(2)

    def create_percentage_chart(team_data, reverse=False, bg_color='#F0F0F0'):
        # Calculate percentage
        percentage = (team_data['total_pts'] / 15) * 100
        
        # Create the chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[percentage],
            y=[team_data['team']],
            orientation='h',
            marker_color='dodgerblue' if team_data['team'] == 'Guys' else 'forestgreen',
            text=[f"{team_data['total_pts']:.1f}"],#[f"{percentage:.1f}%"],
            textposition='outside'
        ))
        
        if reverse == True:
            fig.update_layout(
                height=100,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(range=[100, 0], title="", showticklabels=False,),
                yaxis=dict(title="", showticklabels=False, showline=False),
                showlegend=False,
                plot_bgcolor=bg_color,  # Set plot background color
                # paper_bgcolor=bg_color  # Set paper background color
            )
        else:
            # Customize the chart
            fig.update_layout(
                height=100,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(range=[0, 100], title="", showticklabels=False,),
                yaxis=dict(title="", showticklabels=False, showline=False),
                showlegend=False,
                plot_bgcolor=bg_color,  # Set plot background color
            )
        
        return fig

    # Create and display chart for Guys
    with col1:
        st.write("## Guys")
        guys_data = pts_summary[pts_summary['team'] == 'Guys'].iloc[0]
        st.plotly_chart(create_percentage_chart(guys_data), use_container_width=True)

    # Create and display chart for Dudes
    with col2:
        st.write("## Dudes")
        dudes_data = pts_summary[pts_summary['team'] == 'Dudes'].iloc[0]
        st.plotly_chart(create_percentage_chart(dudes_data, reverse=True), use_container_width=True)



    st.write("## Built in st charts/ Vega?")

    source = data.barley()

    filtered_df = golf_sheet_df[golf_sheet_df['team'] == 'Guys']
    st.dataframe(filtered_df)

    # # Sort the dataframe by 'site' in descending order (Z-A)
    # source_sorted = source.sort_values('site', ascending=False)

    # # Reset the index to ensure proper ordering in the chart
    # source_sorted = source_sorted.reset_index(drop=True)

    # Convert the DataFrame to a list of dictionaries for Vega-Lite
    barley_dict = source.to_dict(orient='records')

    guys_dict = filtered_df.to_dict(orient='records')

    # Calculate the sum of total_pts
    total_pts_sum = filtered_df['total_pts'].sum()

    # Calculate the percentage (out of 15)
    percentage = (total_pts_sum / 15) * 100

    # Create a new dictionary with the percentage
    percentage_dict = [
        {"team": "Guys", "percentage": percentage}
    ]

    # Create the Vega-Lite chart specification
    vega_spec = {
        "data": {"values": percentage_dict},
        "mark": {"type": "bar", "color": "blue"},
        "encoding": {
            "x": {
                "field": "percentage",
                "type": "quantitative",
                "axis": {"format": ".0f", "title": "Percentage"},
                "scale": {"domain": [0, 100]}  # This ensures the axis always goes from 0 to 100
            },
            "y": {"field": "team", "type": "nominal", "axis": {"title": ""}},
            "tooltip": [
                {"field": "team", "type": "nominal"},
                {"field": "percentage", "type": "quantitative", "format": ".1f", "title": "Percentage"}
            ]
        },
        "config": {
            "view": {"strokeWidth": 0},
            "axis": {"grid": False}
        },
        "width": "container",
        "height": 100
    }

    # Display the chart
    st.vega_lite_chart(vega_spec, use_container_width=True)

    # Create the bar chart with the sorted data
    st.vega_lite_chart({
        "data": {"values": barley_dict},
        "mark": "bar",
        # "encoding": {
        #     "x": {"aggregate": "sum", "field": "yield"},
        #     "y": {"field": "variety"},
        #     "color": {"field": "site"}
        # }
        "encoding": {
            "x": {"aggregate": "sum", "field": "yield"},
            "y": {"field": "variety"},
            "color": {"field": "site"},
            "order": {"aggregate": "sum", "field": "yield"}
        }
        })

    # Create two columns for the charts
    col1, col2 = st.columns(2)

    # Function to create a DataFrame for the bar chart
    def create_chart_data(team_data, reverse=False):
        data = pd.DataFrame({
            'Total Points': [team_data['total_pts']],
            'Available Points': [team_data['pts_available']]
        })
        if reverse:
            data = data.sort_index(axis=1, ascending=True)
        else:
            data = data.sort_index(axis=1, ascending=False)
        return data


    # Create and display chart for Dudes
    with col1:
        st.subheader("Dudes")
        dudes_data = pts_summary[pts_summary['team'] == 'Dudes'].iloc[0]
        dudes_chart_data = create_chart_data(dudes_data)
        st.dataframe(dudes_chart_data)
        st.bar_chart(data=dudes_chart_data, horizontal=True)

    # Create and display chart for Guys
    with col2:
        st.subheader("Guys")
        guys_data = pts_summary[pts_summary['team'] == 'Guys'].iloc[0]
        guys_chart_data = create_chart_data(guys_data, reverse=True)
        st.dataframe(guys_data)
        st.dataframe(guys_chart_data)
        st.bar_chart(data=guys_chart_data,horizontal=True)




    # latest picks and standings
    latest_left, latest_right = st.columns(2, vertical_alignment="bottom")

    with latest_left:
        st.write("## Standings")
        st.dataframe(df_display, hide_index=True, height=400)
    with latest_right:
        st.write("## Divisional Round Picks")
        st.dataframe(week2_df_filtered, hide_index=True,)

    st.write("## Divisional Round Pick Charts")

    ### latest picks
    p_left, p_right = st.columns(2)
    # sort week 1 games into columns
    left_gm = [summaries['Texans vs. Ravens (-9.5)'], summaries['Bucs vs. Lions (-6.5)']]
    right_gm = [summaries['Packers vs. 49ers (-9.5)'], summaries['Chiefs vs. Bills (-2.5)'] ] 
    with p_left:
        for df in left_gm:
            fig = create_team_chart(df, color_mapping)
            st.plotly_chart(fig, use_container_width=True)
    with p_right:
        for df in right_gm:
            fig = create_team_chart(df, color_mapping)
            st.plotly_chart(fig, use_container_width=True)      

    bb_fig = create_team_chart(summaries['Best Bet'], color_mapping, chart_title='Most Popular Best Bets')
    st.plotly_chart(bb_fig, use_container_width=True)  

    ### prior week picks
    st.write("## Wild Card Round Picks")
    st.write("In hindsight, 'the crowd' in our pool was wrong in 5 out of 6 games (only the Chiefs bet hit, and that split was pretty close). Might be an interesting play to fade the crowd in your bets outside of this pool!")
    # display columns
    left_column, middle_column, right_column = st.columns(3)

    # sort week 1 games into columns
    left_dfs = [game1df, game4df]
    middle_dfs = [game2df, game5df]
    right_dfs = [game3df, game6df]

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
