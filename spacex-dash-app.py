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



### Task 1
available_sites = [{'label': site, 'value': site } for site in spacex_df['Launch Site'].unique()]
available_sites.append({
    'label': 'All Sites',
    'value': 'ALL'
})


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                    options=available_sites, 
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0,
                                    max=10_000,
                                    step=1_000,
                                    value=[0, 10_000]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    df = spacex_df
    if entered_site == "ALL":
        return px.pie(df, values='class',
            names= df['Launch Site'],
            title='Total Success Launches by Site'
        ) 
    else:
        current_site = df[df['Launch Site'] == entered_site]
        return px.pie(current_site, values=current_site['class'].value_counts().values,
            names=[0,1],
            title=f'Total Success Launches for site {entered_site}'
        ) 



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, payload_range):
    df = spacex_df[(spacex_df['Payload Mass (kg)']>= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    if entered_site == "ALL":
        return px.scatter(df, 
            x='Payload Mass (kg)', 
            y='class',
            color='Booster Version Category'
        )
    else:
        current_site = df[df['Launch Site'] == entered_site]
        return px.scatter(current_site, 
            x='Payload Mass (kg)', 
            y='class',
            color='Booster Version Category'
        )

# Run the app
if __name__ == '__main__':
    app.run(port=8051)
