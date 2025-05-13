import pandas as pd
import dash
from dash import dcc, html, Input, Output, ALL, ctx, dash_table
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Load and clean data
df = pd.read_csv("Dv_Final.csv")
df.columns = df.columns.str.strip()

# Drop rows with missing essential columns
essential_cols = ['protein', 'calories', 'sugar', 'fat', 'name', 'rating', 'minutes', 'Diet_Type']
df = df.dropna(subset=essential_cols)

# Compute health score
df['Health_Score'] = (
    (df['protein'] / df['calories']) * 100 -
    (df['sugar'] / df['calories']) * 50 -
    (df['fat'] / df['calories']) * 30
)

df = df[(df['calories'] < 2000) & (df['Health_Score'] > -100) & (df['Health_Score'] < 100)]

# Limit to first 10,000 unique names for sidebar list
MAX_RECIPES = 10000
sidebar_names = df['name'].drop_duplicates().head(MAX_RECIPES)

def classify(row):
    if row['calories'] <= 200 and row['Health_Score'] >= 7:
        return 'Healthy'
    elif row['calories'] > 200 and row['Health_Score'] <= 4:
        return 'Unhealthy'
    else:
        return 'Moderate'

df['Category'] = df.apply(classify, axis=1)

# Dash app initialization
app = dash.Dash(__name__)
server = app.server  # Add this line for deployment
app.title = "Recipe Health Dashboard"

nutrient_options = [
    {"label": "All", "value": "all"},
    {"label": "Protein", "value": "protein"},
    {"label": "Calories", "value": "calories"},
    {"label": "Fat", "value": "fat"},
    {"label": "Sugar", "value": "sugar"},
    {"label": "Carbs", "value": "carbs"}
]
group_options = [
    {"label": "Diet Type", "value": "Diet_Type"},
    {"label": "Health Category", "value": "Category"},
    {"label": "Diet Type + Health Category", "value": "both"}
]

# Layout
app.layout = html.Div([
    html.H1("Recipe Health Dashboard", style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    dcc.Tabs([
        # Tab 1: Nutrient Profile Explorer
        dcc.Tab(label="Nutrient Profile Explorer", children=[
            html.Div([
                dcc.Graph(
                    id='scatter-plot',
                    figure=go.Figure(
                        data=[go.Scatter(
                            x=df['calories'],
                            y=df['Health_Score'],
                            mode='markers',
                            marker=dict(
                                color=df['Category'].map({
                                    'Healthy': 'green',
                                    'Moderate': 'orange',
                                    'Unhealthy': 'red'
                                }),
                                size=8
                            ),
                            text=df['name'],
                            hovertemplate='<b>%{text}</b><br>Calories: %{x}<br>Health Score: %{y:.1f}<extra></extra>'
                        )]
                    ).update_layout(
                        title="Nutrient Profile Explorer",
                        xaxis_title="Calories",
                        yaxis_title="Health Score",
                        height=600
                    )
                )
            ])
        ]),
        
        # Tab 2: Nutrient Heatmap
        dcc.Tab(label="Nutrient Distribution", children=[
    html.Div([
                html.Label("Select Nutrient:"),
        dcc.Dropdown(
                    id='heatmap-nutrient-dropdown',
                    options=nutrient_options,
                    value='protein',
                    clearable=False,
                    style={'width': '300px', 'marginBottom': '20px'}
                ),
                dcc.Graph(id='nutrient-heatmap')
            ])
        ]),
        
        # Tab 3: Recipe Popularity Analysis
        dcc.Tab(label="Recipe Popularity", children=[
                        html.Div([
                            dcc.Graph(
                    figure=go.Figure(
                        data=[go.Scatter(
                            x=df['minutes'],
                            y=df['rating'],
                            mode='markers',
                            marker=dict(color='#2ecc71', size=8),
                            opacity=0.6
                        )]
                                ).update_layout(
                        title="Preparation Time vs Rating",
                        xaxis_title="Preparation Time (minutes)",
                        yaxis_title="Rating",
                            height=600
                        )
                    )
            ])
        ]),
        
        # Tab 4: Health Score Analysis
        dcc.Tab(label="Health Score Analysis", children=[
                html.Div([
                    dcc.Graph(
                    figure=go.Figure(
                        data=[go.Scatter(
                            x=df['Health_Score'],
                            y=df['rating'],
                            mode='markers',
                            marker=dict(
                                color=df['Category'].map({
                                    'Healthy': 'green',
                                    'Moderate': 'orange',
                                    'Unhealthy': 'red'
                                }),
                                size=8
                            ),
                            opacity=0.6
                        )]
                        ).update_layout(
                        title="Health Score vs Rating",
                        xaxis_title="Health Score",
                        yaxis_title="Rating",
                            height=600
                        )
                    )
            ])
        ])
    ])
])

# Callbacks
@app.callback(
    Output('nutrient-heatmap', 'figure'),
    [Input('heatmap-nutrient-dropdown', 'value')]
)
def update_heatmap(nutrient):
    if nutrient == 'all':
        return create_all_nutrients_heatmap()
    
    pivot = df.pivot_table(
        index='Diet_Type',
        columns='Category',
        values=nutrient,
        aggfunc='mean'
    ).fillna(0)
    
    return go.Figure(
        data=[go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale='RdBu',
            text=[[f"{val:.1f}" for val in row] for row in pivot.values],
            texttemplate="%{text}",
            showscale=True
        )]
    ).update_layout(
        title=f"Average {nutrient.title()} by Diet Type and Health Category",
        xaxis_title="Health Category",
        yaxis_title="Diet Type",
        height=600
    )

def create_all_nutrients_heatmap():
    nutrients = ["protein", "calories", "fat", "sugar", "carbs"]
        fig = make_subplots(
        rows=2, cols=3,
            subplot_titles=[f"{nut.title()}" for nut in nutrients],
        vertical_spacing=0.2
        )
    
    for i, nutrient in enumerate(nutrients, 1):
            pivot = df.pivot_table(
            index='Diet_Type',
            columns='Category',
            values=nutrient,
            aggfunc='mean'
        ).fillna(0)
        
        row = (i-1) // 3 + 1
        col = (i-1) % 3 + 1
        
        fig.add_trace(
            go.Heatmap(
                z=pivot.values,
                x=pivot.columns,
                y=pivot.index,
                colorscale='RdBu',
                text=[[f"{val:.1f}" for val in row] for row in pivot.values],
                texttemplate="%{text}",
                showscale=True
            ),
            row=row, col=col
        )
    
    fig.update_layout(height=800, title_text="All Nutrients Distribution")
        return fig

# Run server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port, debug=False)
