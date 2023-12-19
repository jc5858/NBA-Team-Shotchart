# Load the dataset
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load data
@st.cache_data
def load_data():
    df_2010 = pd.read_csv('2010-11.csv')
    df_2022 = pd.read_csv('2022-23.csv')
    return df_2010, df_2022

df_2010, df_2022 = load_data()

# Check if Streamlit's session state has a "page" attribute. If not, set it to "homepage"
if "page" not in st.session_state:
    st.session_state.page = "homepage"

# Function for the homepage
def homepage():
    # Displaying the details on the homepage
    st.title("NBA Team Shot Chart: 2010-11 vs. 2022-23")
    st.write("Created by: Jason Chien(jc5858)")
    st.write("Course Title: Fundamentals of Sports Analytics")
    st.write("""
    Introduction:
    This webapp provides a visual representation of NBA team shot charts for the 2010-11 and 2022-23 seasons. By selecting a team, users can view where shots were made or missed on the basketball court for both seasons.
    """)
    st.write("""
    Instructions:
    1. Select a team from the dropdown list.
    2. The shot chart for the selected team will be displayed for both 2010-11 and 2022-23 seasons.
    """)

    if st.button("Get Started"):
        st.session_state.page = "main_app"

# Function to draw the basketball court
from matplotlib.patches import Circle, Rectangle, Arc
def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the basketball hoop
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                        fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                        fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                        linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                    color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                            color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the 
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                        linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                        linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                    bottom_free_throw, restricted, corner_three_a,
                    corner_three_b, three_arc, center_outer_arc,
                    center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

# Function to plot shot chart
def plot_shot_chart(df, title, color):
    plt.figure(figsize=(12, 11))
    draw_court(outer_lines=True)
    plt.title(title)
    missed_shot = df[df['EVENT_TYPE'] == 'Missed Shot']
    plt.scatter(missed_shot.LOC_X, missed_shot.LOC_Y, s=3, c='red')
    made_shot = df[df['EVENT_TYPE'] == 'Made Shot']
    plt.scatter(made_shot.LOC_X, made_shot.LOC_Y, s=3, c=color)
    plt.xlim(-300, 300)
    plt.ylim(-100, 500)
    st.pyplot(plt)

# Function for the main app
def main_app():
    # Get unique teams from both datasets
    unique_teams_2010 = set(df_2010['TEAM_NAME'].unique())
    unique_teams_2022 = set(df_2022['TEAM_NAME'].unique())
    unique_teams = list(unique_teams_2010.union(unique_teams_2022))
    unique_teams.sort()

    selected_team = st.sidebar.selectbox("Select a Team:", unique_teams)

    st.title(f"{selected_team}'s Shooting Chart")

    team_df_2010 = df_2010[df_2010['TEAM_NAME'] == selected_team]
    team_df_2022 = df_2022[df_2022['TEAM_NAME'] == selected_team]

    fig, ax = plt.subplots(1, 2, figsize=(18, 8.25))  # Adjusting the figure size

    if not team_df_2010.empty:
        draw_court(ax[0], outer_lines=True)
        ax[0].set_title(f"Shot Chart for {selected_team} (2010-11)")
        missed_shot = team_df_2010[team_df_2010['EVENT_TYPE'] == 'Missed Shot']
        ax[0].scatter(missed_shot.LOC_X, missed_shot.LOC_Y, s=3, c='red')
        made_shot = team_df_2010[team_df_2010['EVENT_TYPE'] == 'Made Shot']
        ax[0].scatter(made_shot.LOC_X, made_shot.LOC_Y, s=3, c='green')
        ax[0].set_xlim(-300, 300)
        ax[0].set_ylim(-100, 500)

    if not team_df_2022.empty:
        draw_court(ax[1], outer_lines=True)
        ax[1].set_title(f"Shot Chart for {selected_team} (2022-23)")
        missed_shot = team_df_2022[team_df_2022['EVENT_TYPE'] == 'Missed Shot']
        ax[1].scatter(missed_shot.LOC_X, missed_shot.LOC_Y, s=3, c='red')
        made_shot = team_df_2022[team_df_2022['EVENT_TYPE'] == 'Made Shot']
        ax[1].scatter(made_shot.LOC_X, made_shot.LOC_Y, s=3, c='green')
        ax[1].set_xlim(-300, 300)
        ax[1].set_ylim(-100, 500)

    st.pyplot(fig)

# Control the flow
if st.session_state.page == "homepage":
    homepage()
else:
    main_app()
