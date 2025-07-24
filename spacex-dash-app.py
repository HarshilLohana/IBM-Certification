# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                  options=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'site1', 'value': 'site1'}, ...]
                                dcc.Dropdown(id='site-dropdown',options=dropdown_options,
                                value='ALL',  # Set 'ALL' as the default selected value
                                placeholder="Select a Launch Site", # Text displayed when no option is selected
                                searchable=True)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(data, values='class', 
        names='pie chart names', 
        title='title')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_site_df = filtered_df[filtered_df['LaunchSite'] == entered_site]

        # Return the outcomes pie chart for a selected site
        # Count success vs. failure for the specific site
        fig = px.pie(filtered_site_df,
                     values=filtered_site_df['success_str'].value_counts().values, # Counts of True/False for the site
                     names=filtered_site_df['success_str'].value_counts().index,   # Labels 'True', 'False'
                     title=f'Success vs. Failure for {entered_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_range):
    # Filter by payload range first
    low, high = payload_range
    filtered_df_payload = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if entered_site == 'ALL':
        fig = px.scatter(filtered_df_payload,
                         x='Payload Mass (kg)',
                         y='success_str', # 'class' column
                         color='Booster Version Category',
                         title='Payload Mass vs. Launch Outcome (All Sites)',
                         labels={'success_str': 'Launch Outcome (Success/Failure)'})
        return fig
    else:
        # Filter by selected site AND payload range
        filtered_site_df = filtered_df_payload[
            filtered_df_payload['LaunchSite'] == entered_site
        ]
        fig = px.scatter(filtered_site_df,
                         x='Payload Mass (kg)',
                         y='success_str', # 'class' column
                         color='Booster Version Category',
                         title=f'Payload Mass vs. Launch Outcome for {entered_site}',
                         labels={'success_str': 'Launch Outcome (Success/Failure)'})
        return fig

# Run the app
if __name__ == '__main__':
    app.run()
