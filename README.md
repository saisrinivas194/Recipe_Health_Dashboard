# Recipe Health Dashboard

An interactive dashboard for exploring recipe data, focusing on health and nutrition profiles across different recipes.

## Features

- **Nutrient Profile Explorer**: Visualize recipes by calories vs. health score
- **Recipe Nutrient Heat Map**: Explore nutrient distribution across different diet types and preparation times
- **Recipe Popularity Factors**: Analyze how preparation time and complexity affect recipe ratings
- **Nutrient Impact on Ratings**: See how different nutrients correlate with popularity
- **Health Score vs. Rating**: Examine if healthier recipes tend to receive higher ratings

## Deployment Options

### Heroku

1. Create an account on [Heroku](https://www.heroku.com/)
2. Install the Heroku CLI and login
3. Clone this repository or upload it to GitHub
4. Run the following commands:
   ```
   heroku create your-app-name
   git push heroku main
   ```

### Render

1. Create an account on [Render](https://render.com/)
2. Create a new Web Service
3. Connect your GitHub repository or upload files manually
4. Configure the build:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:server`

### Python Anywhere

1. Sign up for a free account on [PythonAnywhere](https://www.pythonanywhere.com/)
2. Upload your files
3. Create a new web app with Flask
4. Configure WSGI file to point to your app's server variable

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`
4. Open your browser to http://localhost:8050

## Data Source

The dashboard uses recipe data from `Dv_Final.csv` which includes nutritional information, preparation details, and ratings.

## Requirements

See `requirements.txt` for the full list of dependencies. # Recipe_Health_Dashboard
