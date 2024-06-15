# Import required libraries
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import io
import plotly.express as px
import base64
from wordcloud import WordCloud
from collections import Counter
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load the data from the CSV file
tweets = pd.read_csv("Airplanetweets/data/Tweets.csv")

tweets['negativereason'] = tweets['negativereason'].replace({
    'Flight Booking Problems': 'Booking Problems',
    'Flight Attendant Complaints': 'Attendant Complaints',
    'Customer Service Issue': 'Customer Service'
})

# Convert tweet_created to datetime if it's not already
tweets['tweet_created'] = pd.to_datetime(tweets['tweet_created'])

# Get the date range
date_range = pd.date_range(tweets['tweet_created'].min(), tweets['tweet_created'].max())

# Function to create date marks for the slider, using only the day of the month
def create_short_date_marks(date_range):
    return {i: str(date.day) for i, date in enumerate(date_range)}


# Calculate positive tweet proportions (from the first code block)
positive_tweets = tweets[tweets['airline_sentiment'] == 'positive']
positive_counts = positive_tweets['airline'].value_counts().reset_index()
positive_counts.columns = ['airline', 'positive_count']
total_counts = tweets['airline'].value_counts().reset_index()
total_counts.columns = ['airline', 'total_count']
counts = pd.merge(positive_counts, total_counts, on='airline')
counts['positive_proportion'] = counts['positive_count'] / counts['total_count']

# Combine all tweets into a single string
all_tweets_text = ' '.join(tweets['text'])

# Preprocess text: Remove special characters, numbers and convert to lower case
all_tweets_text = re.sub(r'[^A-Za-z\s]', '', all_tweets_text).lower()

# Tokenize the text
words = word_tokenize(all_tweets_text)

# Remove stopwords
stop_words = set(stopwords.words('english'))
filtered_words = [word for word in words if word not in stop_words]

# Count word frequencies
word_counts = Counter(filtered_words)

# Get the top 40 words with highest frequency
most_common_words = word_counts.most_common(40)

# Create a DataFrame for Plotly
df = pd.DataFrame(most_common_words, columns=['Word', 'Count'])


# Generate word cloud
wordcloud = WordCloud(width=800, height=300, background_color='white').generate(all_tweets_text)

# Convert word cloud to image bytes
img_bytes = io.BytesIO()
plt.figure(figsize=(8, 4))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Word Cloud of Tweets')
plt.axis('off')
plt.tight_layout()
plt.savefig(img_bytes, format='png')
plt.close()

# Calculate tweet counts by airline for treemap
tweet_counts_by_airline = tweets['airline'].value_counts().reset_index()
tweet_counts_by_airline.columns = ['airline', 'tweet_count']

# Create treemap using Plotly Express
fig_treemap = px.treemap(df, path=['Word'], values='Count', 
                 color='Count', color_continuous_scale='viridis')

fig_treemap.update_layout(showlegend=False)

# Specify columns to display
columns_to_display = ['text', 'airline_sentiment']

# Function to randomly select a row and return the specific columns
def get_random_row_data(df, columns):
    random_row = df.sample(n=1)
    return random_row[columns].to_dict('records')[0]

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    style={'display': 'flex', 'flexDirection': 'column', 'align-items': 'center', 'height': '100vh', 'background-color': '#f0f2f5', 'padding': '20px'},
    children=[
        html.H1("Airline Tweets Sentiment Analysis"),
        html.Div(id='random-tweet-output', style={
        'whiteSpace': 'pre-line',
        'border': '1px solid black',
        'padding': '10px',
        'margin': '10px',
        'borderRadius': '5px',
        'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)',
        'display': 'block',
        'width' : '700px',
        'height' : '100px'
        }),
        html.Button("Display Random Tweet", id='random-tweet-button', n_clicks=0 ,
                style={
                  'backgroundColor': 'blue',  
                  'color': 'white',          
                  'padding': '10px 20px',    
                  'border': 'none',          
                  'borderRadius': '5px',     
                  'cursor': 'pointer',
                  'margin-bottom' : '10px'      
                }),
        html.Div(
            style={
                'border': '2px solid #ccc',
                'border-radius': '15px',
                'padding': '5px',
                'width': '80%',
                'background-color': '#ffffff',
                'box-shadow': '2px 2px 12px rgba(0,0,0,0.1)',
                'text-align': 'center'
            },
            children=[
                html.H3("Negative tweets Between Airlines ", style={'margin-top': '5px', 'margin-left': '10px'}),
                html.Div(
                    style={'display': 'flex', 'justify-content': 'space-around', 'margin-bottom': '20px'},
                    children=[
                        dcc.Dropdown(
                            id='airline1-dropdown',
                            options=[{'label': airline, 'value': airline} for airline in tweets['airline'].unique()],
                            value='United',
                            style={'width': '90%'},
                            clearable=False
                        ),
                        dcc.Dropdown(
                            id='airline2-dropdown',
                            options=[{'label': airline, 'value': airline} for airline in tweets['airline'].unique()],
                            value='Delta',
                            style={'width': '90%'},
                            clearable=False
                        ),
                    ]
                ),
                dcc.Graph(
                    id='negative-reasons-comparison-bar-chart',
                    style={'height': '400px'}
                )
            ]
        ),
        html.Div(
            style={'display': 'flex', 'justifyContent': 'space-between', 'width': '80%', 'margin-bottom': '20px'},
            children=[
                html.Div(
                    style={
                        'margin-top': '15px',
                        'border': '2px solid #ccc',
                        'border-radius': '15px',
                        'padding': '5px',  
                        'width': '60%',
                        'background-color': '#ffffff',
                        'box-shadow': '2px 2px 12px rgba(0,0,0,0.1)',
                        'text-align': 'center',
                        'height': '400px',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'alignItems': 'center',
                        'justifyContent': 'center'
                    },
                    children=[
                        html.H4("Tweets by Airline", style={'margin-top': '5px', 'margin-bottom': '15px'}),  # Added bottom margin for separation
                        dcc.Graph(
                            id='tweets-graph',
                            figure={},  
                            style={
                                'height': '100%',  
                                'width': '100%'  
                            }
                        )
                    ]
                ),
                html.Div(
                    style={
                        'margin-top': '15px',
                        'width': '30%',
                        'padding': '10px',
                        'background-color': '#555555',
                        'border': '2px solid #ccc',
                        'border-radius': '15px',
                        'box-shadow': '2px 2px 12px rgba(0,0,0,0.1)',
                        'text-align': 'center',
                        'height' : '400px'
                    },
                    children=[
                        html.H5("Filter Options"),
                        dcc.Dropdown(
                            id='sentiment-dropdown',
                            options=[
                                {'label': 'Positive', 'value': 'positive'},
                                {'label': 'Negative', 'value': 'negative'},
                                {'label': 'All Tweets', 'value': 'all'}
                            ],
                            value='positive',  # Default value
                            style={'margin-bottom': '20px'}
                        ),
                        html.H5("Select Date Range"),
                        html.P(
                            f"This contains data from {date_range[0].strftime('%d %b %Y')} to {date_range[-1].strftime('%d %b %Y')}",
                            style={'fontSize': '12px', 'color': 'gray'}
                            ),
                        dcc.RangeSlider(
                            id='date-slider',
                            min=0,
                            max=len(date_range) - 1,
                            value=[0, len(date_range) - 1],
                            marks=create_short_date_marks(date_range),
                            step=1,  # One day step
                            updatemode='mouseup', 
                            allowCross=False
                        )
                    ]
                )
            ]
        ),
        html.Div(
            style={
                'border': '2px solid #ccc',
                'border-radius': '15px',
                'padding': '20px',
                'width': '80%',
                'background-color': '#ffffff',
                'box-shadow': '2px 2px 12px rgba(0,0,0,0.1)',
                'text-align': 'center',
                'margin-bottom': '20px'
            },
            children=[
                dcc.Tabs(
                    id='tabs',
                    value='wordcloud',
                    children=[
                        dcc.Tab(label='Word Cloud', value='wordcloud', selected_style={'background-color': '#0074D9', 'color': 'white'}),
                        dcc.Tab(label='Treemap', value='treemap', selected_style={'background-color': '#0074D9', 'color': 'white'})
                    ]
                ),
                html.Div(id='tabs-content')
            ]
        )
    ]
)

# Callback function to update the negative reasons comparison plot based on selected airlines
@app.callback(
    Output('negative-reasons-comparison-bar-chart', 'figure'),
    [Input('airline1-dropdown', 'value'),
     Input('airline2-dropdown', 'value')]
)
def update_graph(selected_airline1, selected_airline2):
    # Filter for the selected airlines
    airline1_tweets = tweets[tweets['airline'] == selected_airline1]
    airline2_tweets = tweets[tweets['airline'] == selected_airline2]

    # Count the negative reasons
    airline1_negative_counts = airline1_tweets['negativereason'].value_counts()
    airline2_negative_counts = airline2_tweets['negativereason'].value_counts()

    # Create a DataFrame for comparison
    comparison_df = pd.DataFrame({
        'Negative Reason': airline1_negative_counts.index,
        selected_airline1: airline1_negative_counts.values,
        selected_airline2: airline2_negative_counts.reindex(airline1_negative_counts.index, fill_value=0).values
    })

    # Convert the second airline's counts to negative values for plotting
    comparison_df[selected_airline2] = -comparison_df[selected_airline2]

    # Create a bar plot using Plotly
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=comparison_df['Negative Reason'],
        y=comparison_df[selected_airline1],
        name=selected_airline1,
        marker_color='skyblue'
    ))

    fig.add_trace(go.Bar(
        x=comparison_df['Negative Reason'],
        y=comparison_df[selected_airline2],
        name=selected_airline2,
        marker_color='orange'
    ))

    # Update layout
    fig.update_layout(
        title=f'Negative tweets between {selected_airline1} vs {selected_airline2}',
        yaxis_title='Count',
        barmode='relative',
        xaxis_tickangle=-90,
        plot_bgcolor='white',
        paper_bgcolor='white',
        yaxis=dict(
            title='Count',
            tickmode='array',
            tickvals=[-max(comparison_df[selected_airline2]), 0, max(comparison_df[selected_airline1])],
            ticktext=[abs(max(comparison_df[selected_airline2])), 0, max(comparison_df[selected_airline1])]
        ),
        yaxis_tickformat='0f'
    )

    # Add grid lines for better readability
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgray')

    return fig

# Define the callback to update the graph
@app.callback(
    Output('tweets-graph', 'figure'),
    [Input('sentiment-dropdown', 'value'),
     Input('date-slider', 'value')]
)
def update_graph(selected_sentiment, selected_dates):
    start_date = date_range[selected_dates[0]]
    end_date = date_range[selected_dates[1]]
    
    if selected_sentiment == 'all':
        # Filter by date range
        filtered_tweets = tweets[(tweets['tweet_created'] >= start_date) & (tweets['tweet_created'] <= end_date)]
        counts = filtered_tweets['airline'].value_counts().reset_index()
        counts.columns = ['airline', 'count']

        # Create text annotations for airline names inside bars
        annotations = []
        for airline, count in zip(counts['airline'], counts['count']):
            annotations.append({
                'x': airline,
                'y': count / 2,  # Place text at half the height of the bar
                'text': airline,
                'font': {'size': 8, 'color': 'black'},
                'showarrow': False,
                'xanchor': 'center',  
                'yanchor': 'middle',
                'textangle': -90
            })
        
        figure = {
            'data': [
                {'x': counts['airline'], 'y': counts['count'], 'type': 'bar', 'name': 'Tweet Count'}
            ],
            'layout': {
                'title': f'Count of all Tweets from {start_date.date()} to {end_date.date()}',
                'yaxis': {'title': 'Count of Tweets'},
                'xaxis': {'showticklabels': False },
                'annotations': annotations
            }
        }
    else:
        # Filter by sentiment and date range
        filtered_tweets = tweets[(tweets['airline_sentiment'] == selected_sentiment) & 
                                 (tweets['tweet_created'] >= start_date) & 
                                 (tweets['tweet_created'] <= end_date)]
        
        sentiment_counts = filtered_tweets['airline'].value_counts().reset_index()
        sentiment_counts.columns = ['airline', 'count']
        total_counts = tweets['airline'].value_counts().reset_index()
        total_counts.columns = ['airline', 'total_count']
        counts = pd.merge(sentiment_counts, total_counts, on='airline')
        counts['proportion'] = counts['count'] / counts['total_count']

        annotations = []
        for airline, proportion in zip(counts['airline'], counts['proportion']):
            annotations.append({
                'x': airline,
                'y': proportion / 2,  
                'text': airline,  
                'font': {'size': 8, 'color': 'black'},
                'showarrow': False,
                'xanchor': 'center',  
                'yanchor': 'middle',
                'textangle': -90
            })
        
        
        figure = {
            'data': [
                {'x': counts['airline'], 'y': counts['proportion'], 'type': 'bar', 'name': f'{selected_sentiment.capitalize()} Proportion'}
            ],
            'layout': {
                'title': f'{selected_sentiment.capitalize()} Tweets from {start_date.date()} to {end_date.date()}',
                'yaxis': {'title': 'Tweets'},
                'xaxis': {'showticklabels': False},  
                'annotations': annotations
            }
        }

    return figure

# Callback function to update tab content
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'wordcloud':
        return html.Div(
            style={'width': '100%', 'height': 'auto'},
            children=[
                html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(img_bytes.getvalue()).decode()), style={'width': '100%', 'height': 'auto'})
            ]
        )
    elif tab == 'treemap':
        return dcc.Graph(
            id='treemap',
            figure=fig_treemap,
            style={'height': '400px'}
        )
    
# Callback to update the displayed random tweet
@app.callback(
    Output('random-tweet-output', 'children'),
    Input('random-tweet-button', 'n_clicks')
)
def update_output(n_clicks):
    if n_clicks > 0:
        random_data = get_random_row_data(tweets, columns_to_display)
        display_text = [
            html.Div(random_data['text'], style={'marginBottom': '10px'}),
            html.Div(f"~ {random_data['airline_sentiment']}", style={'textAlign': 'right', 'color': 'blue'})
        ]
        return display_text
    return "Click the button to display a random tweet."


# Run the app
if __name__ == '__main__':
    app.run_server(debug=False) 
