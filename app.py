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
    html.H1("Nutrition (N2)"),
    dcc.Tabs([
        dcc.Tab(label="Introduction", children=[
            html.Div([
                html.H2("Understanding Recipe Nutrition Through Interactive Visualizations", 
                       style={'textAlign': 'center', 'marginBottom': '30px', 'color': '#2c3e50'}),
                
                html.Div([
                    html.H3("Why This Dashboard?", style={'marginBottom': '20px'}),
                    html.P([
                        "This interactive dashboard combines six carefully designed visualizations to help users make informed decisions about recipes ",
                        "based on their nutritional content, health scores, and popularity. Each visualization addresses specific aspects of recipe analysis, ",
                        "making complex nutritional data accessible and actionable."
                    ], style={'fontSize': '16px', 'marginBottom': '30px', 'lineHeight': '1.5'})
                ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '5px', 'marginBottom': '30px'}),

                html.H3("Visualization Explanations", style={'marginBottom': '20px'}),
                
                html.Div([
                    html.H4("1. Nutrient Profile Explorer", style={'color': '#2c3e50'}),
                    html.P([
                        "This scatter plot visualization maps recipes based on their calories and health scores. ",
                        "Purpose: To help users understand the relationship between caloric content and overall health score of recipes. ",
                        "Key Features:",
                        html.Ul([
                            html.Li("Interactive selection of recipes from a comprehensive list"),
                            html.Li("Color-coded categories (Healthy, Moderate, Unhealthy) for quick identification"),
                            html.Li("Reference lines showing important thresholds for health classification"),
                            html.Li("Hover information for detailed recipe information")
                        ])
                    ], style={'marginBottom': '20px'})
                ], style={'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '5px', 'marginBottom': '20px'}),

                html.Div([
                    html.H4("2. Nutrient Visualization by Diet Type", style={'color': '#2c3e50'}),
                    html.P([
                        "A heatmap visualization showing nutrient distribution across different diet types. ",
                        "Purpose: To compare nutrient content across different dietary preferences and preparation times. ",
                        "Key Features:",
                        html.Ul([
                            html.Li("Interactive nutrient selection (protein, calories, fat, sugar, carbs)"),
                            html.Li("Color intensity indicating nutrient concentration"),
                            html.Li("Diet type comparison for informed dietary choices"),
                            html.Li("Preparation time consideration for practical meal planning")
                        ])
                    ], style={'marginBottom': '20px'})
                ], style={'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '5px', 'marginBottom': '20px'}),

                html.Div([
                    html.H4("3. Recipe Popularity Factors", style={'color': '#2c3e50'}),
                    html.P([
                        "Regression plots analyzing factors affecting recipe popularity. ",
                        "Purpose: To understand what makes recipes popular among users. ",
                        "Key Features:",
                        html.Ul([
                            html.Li("Analysis of preparation time vs ratings"),
                            html.Li("Impact of recipe complexity on popularity"),
                            html.Li("Trend lines showing general relationships"),
                            html.Li("Interactive data points for detailed information")
                        ])
                    ], style={'marginBottom': '20px'})
                ], style={'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '5px', 'marginBottom': '20px'}),

                html.Div([
                    html.H4("4. Nutrient Impact on Popularity", style={'color': '#2c3e50'}),
                    html.P([
                        "Bar charts showing how different nutrient levels affect recipe ratings. ",
                        "Purpose: To reveal relationships between nutritional content and recipe popularity. ",
                        "Key Features:",
                        html.Ul([
                            html.Li("Grouped bars for different nutrient levels"),
                            html.Li("Rating distribution analysis"),
                            html.Li("Multiple nutrient comparisons"),
                            html.Li("Clear visual patterns of user preferences")
                        ])
                    ], style={'marginBottom': '20px'})
                ], style={'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '5px', 'marginBottom': '20px'}),

                html.Div([
                    html.H4("5. Health Score vs. Rating Categories", style={'color': '#2c3e50'}),
                    html.P([
                        "Distribution analysis of health scores across rating categories. ",
                        "Purpose: To examine if healthier recipes tend to be more popular. ",
                        "Key Features:",
                        html.Ul([
                            html.Li("Health score range categorization"),
                            html.Li("Rating category distribution"),
                            html.Li("Pattern identification in health-popularity relationship"),
                            html.Li("Interactive exploration of health score ranges")
                        ])
                    ], style={'marginBottom': '20px'})
                ], style={'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '5px', 'marginBottom': '20px'}),

                html.Div([
                    html.H4("6. Health-Popularity Relationship", style={'color': '#2c3e50'}),
                    html.P([
                        "Scatter plot examining direct relationship between health scores and ratings. ",
                        "Purpose: To visualize correlation between recipe healthiness and popularity. ",
                        "Key Features:",
                        html.Ul([
                            html.Li("Direct correlation visualization"),
                            html.Li("Health category color coding"),
                            html.Li("Trend line for relationship strength"),
                            html.Li("Detailed recipe information on hover")
                        ])
                    ], style={'marginBottom': '20px'})
                ], style={'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '5px'})
            ], style={'padding': '40px'})
        ]),
        dcc.Tab(label="Nutrient Profile Explorer", children=[
            html.Div(style={'padding': '20px'}, children=[
                # Title at the top
                html.H1(
                    "How to communicate the nutrient profile of different recipes so that people can use them for deciding about their food habits?",
                    style={'textAlign': 'center', 'marginBottom': '30px', 'color': '#2c3e50'}
                ),
                
                # Container for graph and recipe list side by side
                html.Div(style={
                    'display': 'flex',
                    'flexDirection': 'row',
                    'gap': '20px',
                    'marginTop': '20px'
                }, children=[
                    # Graph container on the left
                    html.Div(style={
                        'flex': '3',
                        'minWidth': '0'
                    }, children=[
                        dcc.Graph(
                            id="scatter-plot",
                            style={'height': '70vh'},
                            config={'displayModeBar': True}
                        )
                    ]),
                    
                    # Recipe list container on the right
                    html.Div(style={
                        'flex': '1',
                        'minWidth': '250px',
                        'backgroundColor': '#f9f9f9',
                        'borderLeft': '3px solid #ccc',
                        'padding': '20px'
                    }, children=[
                        html.H3("Recipe List"),
                        html.Ul(
                            id='recipe-list',
                            children=[
                                html.Li(
                                    recipe,
                                    id={'type': 'recipe-item', 'index': i},
                                    n_clicks=0,
                                    style={'cursor': 'pointer', 'padding': '4px'}
                                ) for i, recipe in enumerate(sidebar_names)
                            ],
                            style={'height': '65vh', 'overflowY': 'auto', 'listStyleType': 'none', 'padding': 0}
                        )
                    ])
                ]),
                
                # Comprehensive Explanation Section
                html.Div([
                    html.H3("Understanding the Nutrient Profile Explorer", 
                           style={'color': '#2c3e50', 'marginTop': '40px', 'marginBottom': '20px'}),
                    
                    # Main Purpose
                    html.Div([
                        html.H4("Main Purpose:", 
                               style={'color': '#34495e', 'marginBottom': '15px'}),
                        html.P([
                            "This interactive visualization helps users understand the relationship between a recipe's caloric content ",
                            "and its overall health score, enabling informed decisions about food choices based on nutritional value."
                        ], style={'marginBottom': '20px', 'lineHeight': '1.6'})
                    ]),
                    
                    # What This Visualization Shows
                    html.Div([
                        html.H4("What This Visualization Shows:", 
                               style={'color': '#34495e', 'marginBottom': '15px'}),
                        html.Ul([
                            html.Li("Distribution of recipes based on calories and health scores"),
                            html.Li("Health categorization (Healthy, Moderate, Unhealthy) of each recipe"),
                            html.Li("Relationship between caloric content and overall health score"),
                            html.Li("Individual recipe positions in the nutritional landscape")
                        ], style={'marginBottom': '20px'})
                    ]),
                    
                    # Key Features
                    html.Div([
                        html.H4("Key Features:", 
                               style={'color': '#34495e', 'marginBottom': '15px'}),
                        html.Ul([
                            html.Li([
                                html.Strong("Interactive Recipe Selection: "),
                                "Click on recipes in the list to highlight them in the plot"
                            ]),
                            html.Li([
                                html.Strong("Color Coding: "),
                                "Green for Healthy, Red for Moderate, Blue for Unhealthy recipes"
                            ]),
                            html.Li([
                                html.Strong("Reference Lines: "),
                                "Dashed lines showing important health and calorie thresholds"
                            ]),
                            html.Li([
                                html.Strong("Hover Information: "),
                                "Detailed nutritional information available on hover"
                            ])
                        ], style={'marginBottom': '20px'})
                    ]),
                    
                    # How to Use
                    html.Div([
                        html.H4("How to Use:", 
                               style={'color': '#34495e', 'marginBottom': '15px'}),
                        html.Ul([
                            html.Li("Browse the recipe list to find recipes of interest"),
                            html.Li("Click on recipes to highlight them in the scatter plot"),
                            html.Li("Hover over points to see detailed nutritional information"),
                            html.Li("Use the reference lines to understand health classification")
                        ], style={'marginBottom': '20px'})
                    ]),
                    
                    # Insights to Gain
                    html.Div([
                        html.H4("Insights to Gain:", 
                               style={'color': '#34495e', 'marginBottom': '15px'}),
                        html.Ul([
                            html.Li("Identify recipes that balance health and caloric content"),
                            html.Li("Understand the relationship between calories and health score"),
                            html.Li("Compare similar recipes based on their nutritional profiles"),
                            html.Li("Discover patterns in recipe health classifications")
                        ], style={'marginBottom': '20px'})
                    ]),
                    
                    # Understanding the Health Score
                    html.Div([
                        html.H4("Understanding the Health Score:", 
                               style={'color': '#34495e', 'marginBottom': '15px'}),
                        html.Ul([
                            html.Li([
                                html.Strong("High Health Score (Green): "),
                                "Indicates balanced nutrition with good protein content and moderate calories"
                            ]),
                            html.Li([
                                html.Strong("Moderate Score (Red): "),
                                "Represents recipes with average nutritional balance"
                            ]),
                            html.Li([
                                html.Strong("Low Health Score (Blue): "),
                                "Suggests recipes that might be high in calories or less nutritionally balanced"
                            ])
                        ], style={'marginBottom': '20px'})
                    ]),
                    
                    # Practical Applications
                    html.Div([
                        html.H4("Practical Applications:", 
                               style={'color': '#34495e', 'marginBottom': '15px'}),
                        html.Ul([
                            html.Li("Meal planning based on nutritional goals"),
                            html.Li("Finding healthier alternatives to favorite recipes"),
                            html.Li("Understanding the nutritional trade-offs in different recipes"),
                            html.Li("Making informed decisions about recipe modifications")
                        ])
                    ])
                ], style={
                    'backgroundColor': '#f8f9fa',
                    'padding': '25px',
                    'borderRadius': '10px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    'marginTop': '40px',
                    'marginBottom': '30px'
                })
            ])
        ]),
        dcc.Tab(label="Nutrient Visualization by Diet Type", children=[
            html.Div([
                html.H1("How to communicate the nutrient profile of different recipes so that people can use them for deciding about their food habits?"),
                
                # Control Panel - Simplified to only nutrient selection
                html.Div([
                    html.Label("Select Nutrient:"),
                    dcc.Dropdown(
                        id='heatmap-nutrient-dropdown',
                        options=nutrient_options,
                        value='protein',
                        clearable=False,
                        style={'width': '300px'}
                    )
                ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'}),
                
                # Heatmap
                dcc.Graph(id='nutrient-heatmap'),
                
                # Statistics Panel
                html.Div(id='stats-panel', style={'marginTop': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px'}),
                
                # Visualization Explanation
                html.Div([
                    html.H3("What This Visualization Expresses:", 
                           style={'marginTop': '30px', 'marginBottom': '20px', 'color': '#2c3e50', 'fontWeight': 'bold'}),
                    
                    html.Div([
                        # Purpose and Overview
                        html.Div([
                            html.H4("Purpose:", style={'color': '#34495e', 'marginBottom': '10px'}),
                            html.P("This heatmap visualizes how nutrient content varies across different diet types and preparation times, enabling users to make informed decisions about their food choices.",
                                  style={'marginBottom': '20px', 'lineHeight': '1.5'})
                        ]),
                        
                        # Key Features
                        html.Div([
                            html.H4("Key Features:", style={'color': '#34495e', 'marginBottom': '10px'}),
                            html.Ul([
                                html.Li("Color Intensity: Darker/lighter colors show higher/lower nutrient values", 
                                       style={'marginBottom': '8px'}),
                                html.Li("Grid Layout: Organized by Diet Type (columns) and Preparation Time (rows)", 
                                       style={'marginBottom': '8px'}),
                                html.Li("Interactive Elements: Hover over cells to see detailed nutrient information", 
                                       style={'marginBottom': '8px'}),
                                html.Li("Statistical Insights: View highest, lowest, and average values along with correlations", 
                                       style={'marginBottom': '8px'})
                            ], style={'paddingLeft': '20px'})
                        ], style={'marginBottom': '20px'}),
                        
                        # Insights Revealed
                        html.Div([
                            html.H4("Insights Revealed:", style={'color': '#34495e', 'marginBottom': '10px'}),
                            html.Ul([
                                html.Li("Nutrient Distribution: Identify which diet types typically have higher/lower values of each nutrient", 
                                       style={'marginBottom': '8px'}),
                                html.Li("Time-Nutrient Relationship: Understand how preparation time affects nutrient content", 
                                       style={'marginBottom': '8px'}),
                                html.Li("Diet Comparisons: Compare nutritional profiles between different diet types (e.g., Vegetarian vs. Non-Vegetarian)", 
                                       style={'marginBottom': '8px'}),
                                html.Li("Pattern Recognition: Spot trends and patterns in nutrient distribution across categories", 
                                       style={'marginBottom': '8px'})
                            ], style={'paddingLeft': '20px'})
                        ]),
                        
                        # How to Use
                        html.Div([
                            html.H4("How to Use:", style={'color': '#34495e', 'marginBottom': '10px'}),
                            html.Ul([
                                html.Li("Select a nutrient from the dropdown to focus on specific nutritional aspects", 
                                       style={'marginBottom': '8px'}),
                                html.Li("Hover over cells to view detailed statistics including average values and standard deviation", 
                                       style={'marginBottom': '8px'}),
                                html.Li("Use the statistics panel to understand the overall distribution and correlations", 
                                       style={'marginBottom': '8px'}),
                                html.Li("Compare different regions of the heatmap to identify patterns and relationships", 
                                       style={'marginBottom': '8px'})
                            ], style={'paddingLeft': '20px'})
                        ])
                    ], style={
                        'backgroundColor': '#f8f9fa',
                        'padding': '25px',
                        'borderRadius': '10px',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                        'fontSize': '15px'
                    })
                ], style={'marginTop': '30px', 'marginBottom': '40px'})
            ])
        ]),
        dcc.Tab(label="Recipe Popularity Factors", children=[
            html.Div([
                html.H1("What makes recipes popular?", 
                       style={'textAlign': 'center', 'marginBottom': '30px', 'color': '#2c3e50'}),
                
                # Two graphs in a row
                html.Div([
                    # 1. Preparation Time vs Ratings (Regression Plot)
                    html.Div([
                        dcc.Graph(
                            id='time-vs-rating',
                            figure=px.scatter(
                                df,
                                x='minutes',
                                y='rating',
                                opacity=0.4,
                                color_discrete_sequence=['#2ecc71'],
                                title='Preparation Time vs Ratings',
                                labels={'minutes': 'Time (minutes)', 'rating': 'Rating'},
                                height=500,
                                trendline='ols',
                                trendline_color_override='#e74c3c'
                            ).update_layout(
                                title_font_size=14,
                                xaxis_title_font_size=12,
                                yaxis_title_font_size=12,
                                xaxis_gridcolor='lightgray',
                                yaxis_gridcolor='lightgray',
                                xaxis_title='Time (minutes)',
                                yaxis_title='Rating',
                                plot_bgcolor='white'
                            ).update_traces(
                                marker=dict(size=8)
                            )
                        ),
                        # Explanation for Time vs Rating
                        html.Div([
                            html.H4("Preparation Time vs Ratings Analysis", 
                                   style={'color': '#2c3e50', 'marginTop': '20px', 'marginBottom': '15px'}),
                            html.Div([
                                html.H5("What This Visualization Shows:", style={'color': '#34495e', 'marginBottom': '10px'}),
                                html.Ul([
                                    html.Li("Relationship between recipe preparation time and user ratings"),
                                    html.Li("Trend line (in red) showing the overall pattern"),
                                    html.Li("Distribution of ratings across different preparation times"),
                                    html.Li("Potential sweet spot for recipe duration")
                                ], style={'marginBottom': '15px'}),
                                html.H5("Key Insights:", style={'color': '#34495e', 'marginBottom': '10px'}),
                                html.Ul([
                                    html.Li("Impact of time investment on recipe satisfaction"),
                                    html.Li("Whether longer preparation times lead to better ratings"),
                                    html.Li("Optimal preparation time range for high ratings"),
                                    html.Li("Outliers showing exceptional cases")
                                ])
                            ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px'})
                        ])
                    ], style={'width': '48%', 'display': 'inline-block'}),
                    
                    # 2. Number of Steps vs Ratings (Regression Plot)
                    html.Div([
                        dcc.Graph(
                            id='steps-vs-rating',
                            figure=px.scatter(
                                df,
                                x='n_steps',
                                y='rating',
                                opacity=0.4,
                                color_discrete_sequence=['#3498db'],
                                title='Number of Steps vs Ratings',
                                labels={'n_steps': 'Number of Steps', 'rating': 'Rating'},
                                height=500,
                                trendline='ols',
                                trendline_color_override='#e74c3c'
                            ).update_layout(
                                title_font_size=14,
                                xaxis_title_font_size=12,
                                yaxis_title_font_size=12,
                                xaxis_gridcolor='lightgray',
                                yaxis_gridcolor='lightgray',
                                xaxis_title='Number of Steps',
                                yaxis_title='Rating',
                                plot_bgcolor='white'
                            ).update_traces(
                                marker=dict(size=8)
                            )
                        ),
                        # Explanation for Steps vs Rating
                        html.Div([
                            html.H4("Recipe Complexity (Steps) vs Ratings Analysis", 
                                   style={'color': '#2c3e50', 'marginTop': '20px', 'marginBottom': '15px'}),
                            html.Div([
                                html.H5("What This Visualization Shows:", style={'color': '#34495e', 'marginBottom': '10px'}),
                                html.Ul([
                                    html.Li("Correlation between recipe complexity and user ratings"),
                                    html.Li("Impact of number of steps on recipe popularity"),
                                    html.Li("Distribution of ratings for different complexity levels"),
                                    html.Li("Trend line indicating the general relationship")
                                ], style={'marginBottom': '15px'}),
                                html.H5("Key Insights:", style={'color': '#34495e', 'marginBottom': '10px'}),
                                html.Ul([
                                    html.Li("Whether complex recipes are more appreciated"),
                                    html.Li("Optimal complexity level for high ratings"),
                                    html.Li("User preference for simple vs. complex recipes"),
                                    html.Li("Balance between complexity and user satisfaction")
                                ])
                            ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px'})
                        ])
                    ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
                ]),
                
                # Overall Analysis Section
                html.Div([
                    html.H3("Overall Analysis of Recipe Popularity Factors", 
                           style={'color': '#2c3e50', 'marginTop': '40px', 'marginBottom': '20px'}),
                    html.Div([
                        # Combined Insights
                        html.Div([
                            html.H4("Combined Insights from Both Visualizations:", 
                                   style={'color': '#34495e', 'marginBottom': '15px'}),
                            html.Ul([
                                html.Li("Relationship between effort (time and steps) and recipe success"),
                                html.Li("User preferences regarding recipe complexity"),
                                html.Li("Balance between convenience and thoroughness"),
                                html.Li("Patterns in highly-rated recipes")
                            ], style={'marginBottom': '20px'})
                        ]),
                        
                        # How to Use These Insights
                        html.Div([
                            html.H4("How to Use These Insights:", 
                                   style={'color': '#34495e', 'marginBottom': '15px'}),
                            html.Ul([
                                html.Li("Identify optimal recipe characteristics for high ratings"),
                                html.Li("Understand user preferences for recipe complexity"),
                                html.Li("Find the sweet spot between preparation effort and user satisfaction"),
                                html.Li("Make informed decisions about recipe development and selection")
                            ])
                        ])
                    ], style={
                        'backgroundColor': '#f8f9fa',
                        'padding': '25px',
                        'borderRadius': '10px',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                        'marginBottom': '30px'
                    })
                ])
            ], style={'padding': '40px'})
        ]),
        dcc.Tab(label="Nutrient Impact on Popularity", children=[
            html.Div([
                html.H2("What makes recipes popular?", 
                        style={'textAlign': 'center'}),
                
                # Row 1: Protein and Carbs
                html.Div([
                    # Protein vs Ratings
                    html.Div([
                        dcc.Graph(
                            id='protein-rating-bars',
                            figure=px.histogram(
                                df,
                                x='rating',
                                color='protein_level',
                                barmode='group',
                                labels={'rating': 'Rating', 'protein_level': 'Protein Level'},
                                title='Rating Distribution by Protein Level',
                                color_discrete_sequence=px.colors.qualitative.Set2,
                                category_orders={"rating": sorted(df['rating'].unique())}
                            ).update_layout(
                                xaxis_title='Rating',
                                yaxis_title='Count',
                                legend_title='Protein Level',
                                plot_bgcolor='white'
                            )
                        ),
                        # Explanation for Protein Impact
                        html.Div([
                            html.H4("Protein Content Impact on Ratings", 
                                   style={'color': '#2c3e50', 'marginTop': '20px', 'marginBottom': '15px'}),
                            html.Div([
                                html.H5("What This Visualization Shows:", style={'color': '#34495e', 'marginBottom': '10px'}),
                                html.Ul([
                                    html.Li("Distribution of ratings across different protein levels"),
                                    html.Li("Comparison of high, medium, and low protein recipes"),
                                    html.Li("Relationship between protein content and recipe popularity"),
                                    html.Li("User preferences for protein-rich recipes")
                                ], style={'marginBottom': '15px'}),
                                html.H5("Key Insights:", style={'color': '#34495e', 'marginBottom': '10px'}),
                                html.Ul([
                                    html.Li("Whether high-protein recipes are more popular"),
                                    html.Li("Optimal protein levels for high ratings"),
                                    html.Li("User preferences regarding protein content"),
                                    html.Li("Impact of protein on recipe success")
                                ])
                            ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px'})
                        ])
                    ], style={'width': '48%', 'display': 'inline-block'}),
                    
                    # Carbs vs Ratings
                    html.Div([
                        dcc.Graph(
                            id='carbs-rating-bars',
                            figure=px.histogram(
                                df,
                                x='rating',
                                color='carbs_level',
                                barmode='group',
                                labels={'rating': 'Rating', 'carbs_level': 'Carbs Level'},
                                title='Rating Distribution by Carbohydrate Level',
                                color_discrete_sequence=px.colors.qualitative.Set2,
                                category_orders={"rating": sorted(df['rating'].unique())}
                            ).update_layout(
                                xaxis_title='Rating',
                                yaxis_title='Count',
                                legend_title='Carbs Level',
                                plot_bgcolor='white'
                            )
                        ),
                        # Explanation for Carbs Impact
                        html.Div([
                            html.H4("Carbohydrate Content Impact on Ratings", 
                                   style={'color': '#2c3e50', 'marginTop': '20px', 'marginBottom': '15px'}),
                            html.Div([
                                html.H5("What This Visualization Shows:", style={'color': '#34495e', 'marginBottom': '10px'}),
                                html.Ul([
                                    html.Li("Distribution of ratings for different carbohydrate levels"),
                                    html.Li("Comparison between high and low-carb recipes"),
                                    html.Li("User preferences regarding carbohydrate content"),
                                    html.Li("Impact of carbs on recipe popularity")
                                ], style={'marginBottom': '15px'}),
                                html.H5("Key Insights:", style={'color': '#34495e', 'marginBottom': '10px'}),
                                html.Ul([
                                    html.Li("Preferred carbohydrate levels in recipes"),
                                    html.Li("Relationship between carbs and ratings"),
                                    html.Li("Current trends in carb preferences"),
                                    html.Li("Balance point for carbohydrate content")
                                ])
                            ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px'})
                        ])
                    ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
                ], style={'marginBottom': '40px'}),
                
                # Row 2: Sugar and Fat
                html.Div([
                    # Sugar vs Ratings
                    html.Div([
                        dcc.Graph(
                            id='sugar-rating-bars',
                            figure=px.histogram(
                                df,
                                x='rating',
                                color='sugar_level',
                                barmode='group',
                                labels={'rating': 'Rating', 'sugar_level': 'Sugar Level'},
                                title='Rating Distribution by Sugar Level',
                                color_discrete_sequence=px.colors.qualitative.Set2,
                                category_orders={"rating": sorted(df['rating'].unique())}
                            ).update_layout(
                                xaxis_title='Rating',
                                yaxis_title='Count',
                                legend_title='Sugar Level',
                                plot_bgcolor='white'
                            )
                        ),
                        # Explanation for Sugar Impact
                        html.Div([
                            html.H4("Sugar Content Impact on Ratings", 
                                   style={'color': '#2c3e50', 'marginTop': '20px', 'marginBottom': '15px'}),
                            html.Div([
                                html.H5("What This Visualization Shows:", style={'color': '#34495e', 'marginBottom': '10px'}),
                                html.Ul([
                                    html.Li("Rating patterns across sugar content levels"),
                                    html.Li("Impact of sugar content on recipe popularity"),
                                    html.Li("User preferences for sweetness levels"),
                                    html.Li("Distribution of ratings for different sugar contents")
                                ], style={'marginBottom': '15px'}),
                                html.H5("Key Insights:", style={'color': '#34495e', 'marginBottom': '10px'}),
                                html.Ul([
                                    html.Li("Optimal sugar levels for high ratings"),
                                    html.Li("User tolerance for sugar content"),
                                    html.Li("Balance between sweetness and popularity"),
                                    html.Li("Trends in sugar preference")
                                ])
                            ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px'})
                        ])
                    ], style={'width': '48%', 'display': 'inline-block'}),
                    
                    # Fat vs Ratings
                    html.Div([
                        dcc.Graph(
                            id='fat-rating-bars',
                            figure=px.histogram(
                                df,
                                x='rating',
                                color='fat_level',
                                barmode='group',
                                labels={'rating': 'Rating', 'fat_level': 'Fat Level'},
                                title='Rating Distribution by Fat Level',
                                color_discrete_sequence=px.colors.qualitative.Set2,
                                category_orders={"rating": sorted(df['rating'].unique())}
                            ).update_layout(
                                xaxis_title='Rating',
                                yaxis_title='Count',
                                legend_title='Fat Level',
                                plot_bgcolor='white'
                            )
                        ),
                        # Explanation for Fat Impact
                        html.Div([
                            html.H4("Fat Content Impact on Ratings", 
                                   style={'color': '#2c3e50', 'marginTop': '20px', 'marginBottom': '15px'}),
                            html.Div([
                                html.H5("What This Visualization Shows:", style={'color': '#34495e', 'marginBottom': '10px'}),
                                html.Ul([
                                    html.Li("Distribution of ratings across fat content levels"),
                                    html.Li("Relationship between fat content and popularity"),
                                    html.Li("User preferences regarding fat levels"),
                                    html.Li("Impact of fat content on recipe success")
                                ], style={'marginBottom': '15px'}),
                                html.H5("Key Insights:", style={'color': '#34495e', 'marginBottom': '10px'}),
                                html.Ul([
                                    html.Li("Optimal fat content for high ratings"),
                                    html.Li("User preferences for fat levels"),
                                    html.Li("Balance between taste and health considerations"),
                                    html.Li("Trends in fat content preference")
                                ])
                            ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px'})
                        ])
                    ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
                ]),
                
                # Calories Impact
                html.Div([
                    dcc.Graph(
                        id='calories-rating-bars',
                        figure=px.histogram(
                            df,
                            x='rating',
                            color='calories_level',
                            barmode='group',
                            labels={'rating': 'Rating', 'calories_level': 'Calories Level'},
                            title='Rating Distribution by Calories Level',
                            color_discrete_sequence=px.colors.qualitative.Set2,
                            category_orders={"rating": sorted(df['rating'].unique())}
                        ).update_layout(
                            xaxis_title='Rating',
                            yaxis_title='Count',
                            legend_title='Calories Level',
                            plot_bgcolor='white'
                        )
                    ),
                    # Explanation for Calories Impact
                    html.Div([
                        html.H4("Caloric Content Impact on Ratings", 
                               style={'color': '#2c3e50', 'marginTop': '20px', 'marginBottom': '15px'}),
                        html.Div([
                            html.H5("What This Visualization Shows:", style={'color': '#34495e', 'marginBottom': '10px'}),
                            html.Ul([
                                html.Li("Distribution of ratings across calorie levels"),
                                html.Li("Impact of caloric content on recipe popularity"),
                                html.Li("User preferences for different calorie ranges"),
                                html.Li("Relationship between calories and recipe success")
                            ], style={'marginBottom': '15px'}),
                            html.H5("Key Insights:", style={'color': '#34495e', 'marginBottom': '10px'}),
                            html.Ul([
                                html.Li("Optimal calorie range for high ratings"),
                                html.Li("User preferences regarding caloric content"),
                                html.Li("Balance between satisfaction and health consciousness"),
                                html.Li("Trends in calorie preference")
                            ])
                        ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px'})
                    ])
                ], style={'width': '100%', 'marginTop': '40px', 'marginBottom': '40px'}),
                
                # Overall Analysis and Summary
                html.Div([
                    html.H3("Comprehensive Nutrient Impact Analysis", 
                           style={'color': '#2c3e50', 'marginTop': '40px', 'marginBottom': '20px'}),
                    html.Div([
                        # Overall Insights
                        html.Div([
                            html.H4("Overall Insights:", style={'color': '#34495e', 'marginBottom': '15px'}),
                            html.Ul([
                                html.Li("Relationship between nutritional content and recipe popularity"),
                                html.Li("User preferences for different nutrient combinations"),
                                html.Li("Balance between taste, health, and satisfaction"),
                                html.Li("Trends in nutritional preferences")
                            ], style={'marginBottom': '20px'})
                        ]),
                        
                        # Practical Applications
                        html.Div([
                            html.H4("Practical Applications:", style={'color': '#34495e', 'marginBottom': '15px'}),
                            html.Ul([
                                html.Li("Recipe development guidelines based on nutrient preferences"),
                                html.Li("Optimization strategies for recipe success"),
                                html.Li("Understanding user preferences for different nutrient profiles"),
                                html.Li("Balancing nutritional value with user satisfaction")
                            ])
                        ])
                    ], style={
                        'backgroundColor': '#f8f9fa',
                        'padding': '25px',
                        'borderRadius': '10px',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                        'marginBottom': '30px'
                    })
                ])
            ], style={'padding': '40px'})
        ]),
        dcc.Tab(label="Health Score vs. Rating Categories", children=[
            html.Div([
                html.H1("Do healthy recipes have a high popularity?", 
                       style={'textAlign': 'center', 'marginBottom': '30px', 'color': '#2c3e50'}),
                
                # Bar Plot (Health Score vs. Rating Category)
                html.Div([
                    dcc.Graph(
                        id='health-rating-bar',
                        figure=px.histogram(
                            df.assign(Health_Score_Range=pd.cut(
                                df['Health_Score'], 
                                bins=[-100, -50, 0, 50, 100],
                                labels=['Very Low (-100 to -50)', 'Low (-50 to 0)', 'High (0 to 50)', 'Very High (50 to 100)']
                            )),
                            x='Health_Score_Range',
                            color='Rating_Category',
                            barmode='group',
                            title='Count of Recipes by Health Score and Rating Category',
                            color_discrete_sequence=px.colors.qualitative.Set2,
                            labels={'Health_Score_Range': 'Health Score Range', 'count': 'Number of Recipes'}
                        ).update_layout(
                            xaxis_title='Health Score Range',
                            yaxis_title='Count of Recipes',
                            legend_title='Rating Category',
                            plot_bgcolor='white',
                            height=600
                        )
                    ),
                    
                    # Detailed Explanation
                    html.Div([
                        html.H3("Understanding Health Score vs. Rating Categories", 
                               style={'color': '#2c3e50', 'marginTop': '30px', 'marginBottom': '20px'}),
                        
                        # What This Visualization Shows
                        html.Div([
                            html.H4("What This Visualization Shows:", 
                                   style={'color': '#34495e', 'marginBottom': '15px'}),
                            html.Ul([
                                html.Li("Distribution of recipes across different health score ranges"),
                                html.Li("Relationship between health scores and rating categories"),
                                html.Li("Proportion of highly-rated recipes in each health score range"),
                                html.Li("Pattern of user preferences for healthy vs. less healthy recipes")
                            ], style={'marginBottom': '20px'})
                        ]),
                        
                        # Key Features
                        html.Div([
                            html.H4("Key Features:", 
                                   style={'color': '#34495e', 'marginBottom': '15px'}),
                            html.Ul([
                                html.Li("Grouped bars showing rating categories within each health score range"),
                                html.Li("Color-coded rating categories for easy comparison"),
                                html.Li("Health score ranges from very low to very high"),
                                html.Li("Count of recipes indicating popularity in each category")
                            ], style={'marginBottom': '20px'})
                        ]),
                        
                        # Insights Revealed
                        html.Div([
                            html.H4("Insights Revealed:", 
                                   style={'color': '#34495e', 'marginBottom': '15px'}),
                            html.Ul([
                                html.Li("Whether healthier recipes tend to receive higher ratings"),
                                html.Li("User preferences across different health score ranges"),
                                html.Li("Distribution patterns of recipe ratings"),
                                html.Li("Potential correlation between health and popularity")
                            ], style={'marginBottom': '20px'})
                        ]),
                        
                        # How to Interpret
                        html.Div([
                            html.H4("How to Interpret:", 
                                   style={'color': '#34495e', 'marginBottom': '15px'}),
                            html.Ul([
                                html.Li("Compare bar heights within each health score range"),
                                html.Li("Look for patterns in rating distribution"),
                                html.Li("Observe the overall trend across health scores"),
                                html.Li("Note any significant differences between categories")
                            ])
                        ])
                    ], style={
                        'backgroundColor': '#f8f9fa',
                        'padding': '25px',
                        'borderRadius': '10px',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                        'marginTop': '30px'
                    })
                ])
            ], style={'padding': '40px'})
        ]),
        dcc.Tab(label="Health-Popularity Relationship", children=[
            html.Div([
                html.H2("Do healthy recipes have a high popularity?", style={'textAlign': 'center'}),
                
                # Scatter Plot (Health Score vs. Rating)
                html.Div([
                    dcc.Graph(
                        id='health-rating-scatter',
                        figure=px.scatter(
                            df,
                            x='Health_Score',
                            y='rating',
                            color='Category',
                            color_discrete_map={'Moderate': 'orange', 'Healthy': 'green', 'Unhealthy': 'red'},
                            opacity=0.7,
                            title='Relationship Between Health Score and Rating',
                            labels={'Health_Score': 'Health Score', 'rating': 'Rating'},
                            trendline='ols',
                            trendline_color_override='darkgray',
                            hover_data=['name', 'calories', 'protein']
                        ).update_layout(
                            xaxis_title='Health Score',
                            yaxis_title='Rating',
                            legend_title='Health Category',
                            plot_bgcolor='white',
                            height=600
                        )
                    ),
                    
                    # Detailed Explanation
                    html.Div([
                        html.H3("Understanding the Health-Popularity Relationship", 
                               style={'color': '#2c3e50', 'marginTop': '30px', 'marginBottom': '20px'}),
                        
                        # What This Visualization Shows
                        html.Div([
                            html.H4("What This Visualization Shows:", 
                                   style={'color': '#34495e', 'marginBottom': '15px'}),
                            html.Ul([
                                html.Li("Direct relationship between health scores and ratings"),
                                html.Li("Distribution of recipes across health categories"),
                                html.Li("Trend line showing overall correlation"),
                                html.Li("Individual recipe positions with detailed information")
                            ], style={'marginBottom': '20px'})
                        ]),
                        
                        # Key Features
                        html.Div([
                            html.H4("Key Features:", 
                                   style={'color': '#34495e', 'marginBottom': '15px'}),
                            html.Ul([
                                html.Li("Color-coded health categories (Healthy, Moderate, Unhealthy)"),
                                html.Li("Trend line indicating general relationship"),
                                html.Li("Interactive hover information with recipe details"),
                                html.Li("Scatter pattern showing distribution density")
                            ], style={'marginBottom': '20px'})
                        ]),
                        
                        # Insights Revealed
                        html.Div([
                            html.H4("Insights Revealed:", 
                                   style={'color': '#34495e', 'marginBottom': '15px'}),
                            html.Ul([
                                html.Li("Correlation strength between health and popularity"),
                                html.Li("Clustering patterns of highly-rated recipes"),
                                html.Li("Distribution of ratings within health categories"),
                                html.Li("Outliers and exceptional cases")
                            ], style={'marginBottom': '20px'})
                        ]),
                        
                        # How to Interpret
                        html.Div([
                            html.H4("How to Interpret:", 
                                   style={'color': '#34495e', 'marginBottom': '15px'}),
                            html.Ul([
                                html.Li("Follow the trend line to understand the general relationship"),
                                html.Li("Look for clusters of points indicating common patterns"),
                                html.Li("Observe the spread of ratings within each health category"),
                                html.Li("Use hover information to explore specific recipes")
                            ])
                        ]),
                        
                        # Practical Applications
                        html.Div([
                            html.H4("Practical Applications:", 
                                   style={'color': '#34495e', 'marginTop': '20px', 'marginBottom': '15px'}),
                            html.Ul([
                                html.Li("Recipe development focusing on both health and popularity"),
                                html.Li("Understanding user preferences for healthy recipes"),
                                html.Li("Identifying successful healthy recipe characteristics"),
                                html.Li("Optimizing recipes for both health and user satisfaction")
                            ])
                        ])
                    ], style={
                        'backgroundColor': '#f8f9fa',
                        'padding': '25px',
                        'borderRadius': '10px',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                        'marginTop': '30px'
                    })
                ])
            ], style={'padding': '40px'})
        ]),
        dcc.Tab(label="Attributes Information", children=[
            html.Div([
                html.H2("Dataset Attributes", style={'textAlign': 'center', 'marginBottom': '30px'}),
                dash_table.DataTable(
                    data=[
                        {"Attribute": "name", "Type": "Categorical", "Description": "Recipe name"},
                        {"Attribute": "calories", "Type": "Quantitative", "Description": "Total calories in the recipe"},
                        {"Attribute": "protein", "Type": "Quantitative", "Description": "Protein content in grams"},
                        {"Attribute": "fat", "Type": "Quantitative", "Description": "Fat content in grams"},
                        {"Attribute": "sugar", "Type": "Quantitative", "Description": "Sugar content in grams"},
                        {"Attribute": "carbs", "Type": "Quantitative", "Description": "Carbohydrate content in grams"},
                        {"Attribute": "rating", "Type": "Ordinal", "Description": "Recipe rating (1-5)"},
                        {"Attribute": "Diet_Type", "Type": "Categorical", "Description": "Type of diet (e.g., Vegetarian, Non-Vegetarian)"},
                        {"Attribute": "Health_Score", "Type": "Quantitative", "Description": "Calculated health score based on nutrient ratios"},
                        {"Attribute": "Category", "Type": "Categorical", "Description": "Health category (Healthy, Moderate, Unhealthy)"},
                        {"Attribute": "minutes", "Type": "Quantitative", "Description": "Preparation time in minutes"},
                        {"Attribute": "n_steps", "Type": "Quantitative", "Description": "Number of steps in recipe"}
                    ],
                    columns=[
                        {"name": "Attribute", "id": "Attribute"},
                        {"name": "Type", "id": "Type"},
                        {"name": "Description", "id": "Description"}
                    ],
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '10px',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                    },
                    style_header={
                        'backgroundColor': '#f8f9fa',
                        'fontWeight': 'bold',
                        'borderBottom': '2px solid #dee2e6'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f8f9fa'
                        }
                    ]
                ),
                html.Div([
                    html.H3("Attribute Types Explanation:", style={'marginTop': '30px'}),
                    html.Ul([
                        html.Li("Categorical: Attributes that represent categories or groups without inherent order"),
                        html.Li("Quantitative: Numerical attributes that can be measured and compared"),
                        html.Li("Ordinal: Attributes with categories that have a meaningful order")
                    ], style={'fontSize': '16px', 'lineHeight': '1.5'})
                ], style={'marginTop': '20px', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '5px'})
            ], style={'padding': '40px'})
        ])
    ])
])

# Callbacks
@app.callback(
    Output("scatter-plot", "figure"),
    [Input({'type': 'recipe-item', 'index': ALL}, 'n_clicks')]
)
def update_graph(clicks):
    highlight_index = None
    if any(clicks):
        highlight_index = max([i for i, v in enumerate(clicks) if v])

    filtered = df
    
    color_map = {
        'Moderate': 'red',
        'Healthy': 'green',
        'Unhealthy': 'blue'
    }
    label_map = {
        'Moderate': 'Moderate (High)',
        'Healthy': 'Healthy (Low)',
        'Unhealthy': 'Unhealthy (Medium)'
    }

    fig = px.scatter(
        filtered,
        x="calories",
        y="Health_Score",
        color="Category",
        color_discrete_map=color_map,
        hover_data=['name'],
        title='',
        category_orders={'Category': ['Moderate', 'Healthy', 'Unhealthy']}
    )

    # Using responsive layout settings
    fig.update_layout(
        autosize=True,
        margin=dict(l=50, r=50, t=30, b=50),
        plot_bgcolor='rgba(240,240,240,0.2)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Make points slightly larger for better visibility
    fig.update_traces(marker=dict(size=8))

    for trace in fig.data:
        cat = trace.name
        if cat in label_map:
            trace.name = label_map[cat]

    if highlight_index is not None:
        recipe_name = sidebar_names.iloc[highlight_index]
        match = filtered[filtered['name'] == recipe_name]
        if not match.empty:
            recipe_row = match.iloc[0]
            fig.add_annotation(
                x=recipe_row['calories'],
                y=recipe_row['Health_Score'],
                text=f"<b>{recipe_row['name']}</b><br>Category: {recipe_row['Category']}",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                ax=40,
                ay=-40,
                bgcolor='white',
                bordercolor='black',
                borderwidth=2,
                font=dict(size=14, color='black')
            )

    fig.add_vline(x=200, line_dash="dash", line_color="gray", line_width=3, opacity=0.8)
    fig.add_hline(y=7, line_dash="dash", line_color="green", line_width=3, opacity=0.8)
    fig.add_hline(y=4, line_dash="dash", line_color="blue", line_width=3, opacity=0.8)

    return fig

@app.callback(
    [Output('nutrient-heatmap', 'figure'),
     Output('stats-panel', 'children')],
    [Input('heatmap-nutrient-dropdown', 'value')]
)
def update_heatmap(nutrient):
    nutrients = ["protein", "calories", "fat", "sugar", "carbs"]
    
    def create_stats_panel(selected_nutrient, pivot_data):
        # Find highest and lowest values
        max_val = pivot_data.max().max()
        min_val = pivot_data.min().min()
        max_loc = np.where(pivot_data.values == max_val)
        min_loc = np.where(pivot_data.values == min_val)
        
        # Calculate correlations
        correlations = {}
        for other_nut in nutrients:
            if other_nut != selected_nutrient:
                corr = df[selected_nutrient].corr(df[other_nut])
                correlations[other_nut] = corr
        
        # Sort correlations by absolute value
        sorted_corr = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
        
        return html.Div([
            html.H4("Statistics and Insights", style={'marginBottom': '15px'}),
            
            # Highest and Lowest Values
            html.Div([
                html.Div([
                    html.H5("Highest Value:", style={'color': '#2ecc71'}),
                    html.P([
                        f"{max_val:.2f} ",
                        html.Span(f"({pivot_data.index[max_loc[0][0]]} - {pivot_data.columns[max_loc[1][0]]})",
                                style={'color': '#7f8c8d'})
                    ])
                ], style={'flex': 1}),
                html.Div([
                    html.H5("Lowest Value:", style={'color': '#e74c3c'}),
                    html.P([
                        f"{min_val:.2f} ",
                        html.Span(f"({pivot_data.index[min_loc[0][0]]} - {pivot_data.columns[min_loc[1][0]]})",
                                style={'color': '#7f8c8d'})
                    ])
                ], style={'flex': 1}),
                html.Div([
                    html.H5("Average:", style={'color': '#3498db'}),
                    html.P(f"{pivot_data.mean().mean():.2f}")
                ], style={'flex': 1})
            ], style={'display': 'flex', 'marginBottom': '20px', 'gap': '20px'}),
            
            # Correlations
            html.Div([
                html.H5("Nutrient Correlations:", style={'marginBottom': '10px'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Strong(f"{nut.title()}: "),
                            html.Span(f"{corr:.3f}",
                                    style={'color': '#2ecc71' if corr > 0 else '#e74c3c'})
                        ], style={'marginBottom': '5px'})
                        for nut, corr in sorted_corr
                    ])
                ], style={'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '5px'})
            ])
        ])

    if nutrient == "all":
        n = len(nutrients)
        cols = 3
        rows = (n + cols - 1) // cols
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=[f"{nut.title()}" for nut in nutrients],
            horizontal_spacing=0.18,
            vertical_spacing=0.32
        )
        
        all_stats = []
        for i, nut in enumerate(nutrients):
            pivot = df.pivot_table(
                index='Time_Category',
                columns='Diet_Type',
                values=nut,
                aggfunc=np.mean
            )
            
            # Calculate statistics for each nutrient
            all_stats.append(create_stats_panel(nut, pivot))
            
            std_dev = df.pivot_table(
                index='Time_Category',
                columns='Diet_Type',
                values=nut,
                aggfunc=np.std
            )
            count = df.pivot_table(
                index='Time_Category',
                columns='Diet_Type',
                values=nut,
                aggfunc='count'
            )
            
            col = i % cols + 1
            row = i // cols + 1
            
            if col == 3:
                colorbar_x = (col - 0.5) / cols + 0.18
            else:
                colorbar_x = (col - 0.5) / cols + 0.13
            colorbar_y = 1.0 - (row - 0.5) / rows
            
            hover_text = [[
                f"Diet Type: {col}<br>" +
                f"Time Category: {idx}<br>" +
                f"Average {nut.title()}: {val:.1f}<br>" +
                f"Std Dev: {std_dev.loc[idx, col]:.2f}<br>" +
                f"Sample Size: {count.loc[idx, col]:.0f}"
                for col, val in zip(pivot.columns, row_vals)
            ] for idx, row_vals in zip(pivot.index, pivot.values)]
            
            heatmap = go.Heatmap(
                z=pivot.values,
                x=pivot.columns,
                y=pivot.index,
                colorscale='RdBu',
                colorbar=dict(
                    title=dict(
                        text=f"{nut.title()}",
                        side="right"
                    ),
                    x=colorbar_x,
                    y=colorbar_y,
                    len=0.5/rows,
                    thickness=18,
                    outlinewidth=1
                ),
                text=[[f"{v:.1f}" if v==v else '' for v in row] for row in pivot.values],
                texttemplate="%{text}",
                hovertext=hover_text,
                hoverinfo='text',
                showscale=True
            )
            fig.add_trace(heatmap, row=row, col=col)
        
        fig.update_layout(
            height=370*rows,
            width=500*cols + 120,
            title={
                'text': "Nutrient Heat Maps by Diet Type and Preparation Time",
                'x': 0.5,
                'xanchor': 'center'
            },
            margin=dict(t=80, l=20, r=20, b=20),
            dragmode='pan'
        )
        
        # Combine all statistics
        stats_panel = html.Div(all_stats, style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px'})
        return fig, stats_panel
    
    else:
        pivot = df.pivot_table(
            index='Time_Category',
            columns='Diet_Type',
            values=nutrient,
            aggfunc=np.mean
        )
        
        std_dev = df.pivot_table(
            index='Time_Category',
            columns='Diet_Type',
            values=nutrient,
            aggfunc=np.std
        )
        count = df.pivot_table(
            index='Time_Category',
            columns='Diet_Type',
            values=nutrient,
            aggfunc='count'
        )
        
        hover_text = [[
            f"Diet Type: {col}<br>" +
            f"Time Category: {idx}<br>" +
            f"Average {nutrient.title()}: {val:.1f}<br>" +
            f"Std Dev: {std_dev.loc[idx, col]:.2f}<br>" +
            f"Sample Size: {count.loc[idx, col]:.0f}"
            for col, val in zip(pivot.columns, row_vals)
        ] for idx, row_vals in zip(pivot.index, pivot.values)]
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale='RdBu',
            text=[[f"{v:.1f}" if v==v else '' for v in row] for row in pivot.values],
            texttemplate="%{text}",
            hovertext=hover_text,
            hoverinfo='text'
        ))
        
        fig.update_layout(
            height=700,
            title={
                'text': f"Average {nutrient.title()} by Diet Type and Preparation Time",
                'x': 0.5,
                'xanchor': 'center'
            },
            dragmode='pan'
        )
        
        # Create statistics panel for single nutrient
        stats_panel = create_stats_panel(nutrient, pivot)
        return fig, stats_panel

# Run server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port, debug=False)
