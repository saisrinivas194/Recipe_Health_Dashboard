import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import plotly.io as pio

# Set renderer for Google Colab
pio.renderers.default = "colab"

# ==========================================
# LOAD AND CLEAN DATA
# ==========================================
df = pd.read_csv("/content/Dv_Final.csv")
df.columns = df.columns.str.strip()

# Drop rows with missing essential columns
essential_cols = ['protein', 'calories', 'sugar', 'fat', 'name', 'rating', 'minutes', 'Diet_Type']
df = df.dropna(subset=essential_cols)

# ==========================================
# COMPUTE HEALTH SCORE
# ==========================================
df['Health_Score'] = (
    (df['protein'] / df['calories']) * 100 -
    (df['sugar'] / df['calories']) * 50 -
    (df['fat'] / df['calories']) * 30
)

# Filter for valid range
df = df[(df['calories'] < 2000) & (df['Health_Score'] > -100) & (df['Health_Score'] < 100)]

# ==========================================
# CREATE HEALTH CATEGORIES
# ==========================================
def classify(row):
    if row['calories'] <= 200 and row['Health_Score'] >= 7:
        return 'Healthy'
    elif row['calories'] > 200 and row['Health_Score'] <= 4:
        return 'Unhealthy'
    else:
        return 'Moderate'

df['Category'] = df.apply(classify, axis=1)

# ==========================================
# CREATE DASHBOARD LAYOUT
# ==========================================
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        'Nutrient Profile Explorer',
        'Nutrient Heatmap',
        'Recipe Popularity: Preparation Time vs Rating',
        'Average Rating by Protein Level',
        'Average Rating by Health Score Range',
        'Health Score vs Rating'
    ),
    vertical_spacing=0.12,
    horizontal_spacing=0.1
)

# ==========================================
# 1. NUTRIENT PROFILE EXPLORER
# ==========================================
scatter = go.Scatter(
    x=df['calories'],
    y=df['Health_Score'],
    mode='markers',
    marker=dict(
        color=df['Category'].map({'Healthy': 'green', 'Moderate': 'orange', 'Unhealthy': 'red'}),
        size=8
    ),
    text=df['name'],
    hovertemplate='<b>%{text}</b><br>Calories: %{x}<br>Health Score: %{y:.1f}<extra></extra>'
)
fig.add_trace(scatter, row=1, col=1)
fig.add_vline(x=200, line_dash="dash", line_color="gray", row=1, col=1)
fig.add_hline(y=7, line_dash="dash", line_color="green", row=1, col=1)
fig.add_hline(y=4, line_dash="dash", line_color="blue", row=1, col=1)

# ==========================================
# 2. NUTRIENT HEATMAP
# ==========================================
pivot = df.pivot_table(
    index='Diet_Type',
    columns='Category',
    values='protein',
    aggfunc='mean'
).fillna(0)

heatmap = go.Heatmap(
    z=pivot.values,
    x=pivot.columns,
    y=pivot.index,
    colorscale='RdBu',
    text=[[f"{val:.1f}" for val in row] for row in pivot.values],
    texttemplate="%{text}",
    showscale=True
)
fig.add_trace(heatmap, row=1, col=2)

# ==========================================
# 3. PREP TIME VS RATING
# ==========================================
scatter_time = go.Scatter(
    x=df['minutes'],
    y=df['rating'],
    mode='markers',
    marker=dict(color='#2ecc71', size=8),
    opacity=0.6
)
fig.add_trace(scatter_time, row=2, col=1)

# ==========================================
# 4. PROTEIN LEVEL VS RATING
# ==========================================
df['protein_level'] = pd.qcut(df['protein'], q=3, labels=['Low', 'Medium', 'High'])
protein_rating = df.groupby('protein_level')['rating'].mean().reset_index()

bar = go.Bar(
    x=protein_rating['protein_level'],
    y=protein_rating['rating'],
    marker_color='#3498db'
)
fig.add_trace(bar, row=2, col=2)

# ==========================================
# 5. HEALTH SCORE RANGE VS RATING
# ==========================================
df['Health_Score_Range'] = pd.cut(
    df['Health_Score'],
    bins=[-100, -50, 0, 50, 100],
    labels=['Very Low', 'Low', 'High', 'Very High']
)
health_rating = df.groupby('Health_Score_Range')['rating'].mean().reset_index()

bar2 = go.Bar(
    x=health_rating['Health_Score_Range'],
    y=health_rating['rating'],
    marker_color='#e74c3c'
)
fig.add_trace(bar2, row=3, col=1)

# ==========================================
# 6. HEALTH SCORE VS RATING SCATTER
# ==========================================
scatter2 = go.Scatter(
    x=df['Health_Score'],
    y=df['rating'],
    mode='markers',
    marker=dict(
        color=df['Category'].map({'Healthy': 'green', 'Moderate': 'orange', 'Unhealthy': 'red'}),
        size=8
    ),
    opacity=0.6
)
fig.add_trace(scatter2, row=3, col=2)

# ==========================================
# UPDATE LAYOUT
# ==========================================
fig.update_layout(
    height=1500,
    width=1200,
    showlegend=False,
    title_text="Recipe Analysis Dashboard",
    title_x=0.5,
    title_font_size=24,
    template="plotly_white"
)

# Update axes labels
fig.update_xaxes(title_text="Calories", row=1, col=1)
fig.update_yaxes(title_text="Health Score", row=1, col=1)

fig.update_xaxes(title_text="Health Category", row=1, col=2)
fig.update_yaxes(title_text="Diet Type", row=1, col=2)

fig.update_xaxes(title_text="Preparation Time (minutes)", row=2, col=1)
fig.update_yaxes(title_text="Rating", row=2, col=1)

fig.update_xaxes(title_text="Protein Level", row=2, col=2)
fig.update_yaxes(title_text="Average Rating", row=2, col=2)

fig.update_xaxes(title_text="Health Score Range", row=3, col=1)
fig.update_yaxes(title_text="Average Rating", row=3, col=1)

fig.update_xaxes(title_text="Health Score", row=3, col=2)
fig.update_yaxes(title_text="Rating", row=3, col=2)

# Show the figure
fig.show() 