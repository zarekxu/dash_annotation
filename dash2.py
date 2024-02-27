import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import base64
import io
import markdown

# Sample CSV file with items
CSV_FILE = 'sample_data_markdown.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(CSV_FILE)

# Number of items
num_items = len(df)

# Initial dropdown values
initial_dropdown_values = [3] * num_items

# Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='output-data-upload'),
    html.Div(id='scores-output'),  # Display scores here
    html.Button('Show Scores List', id='show-scores-button', n_clicks=0, style={'margin': '10px'}),
    html.Div(id='scores-list')
])

# Callback to handle file upload and display scores
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(contents, filename):
    if contents is None:
        return []

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    # Create a div to display items with numbering and horizontal lines
    items_div = []
    for i in range(len(df)):
        item_number = i + 1
        items_div.append(html.Div([
            html.Hr(),  # Horizontal line
            html.P(f"Item {item_number}:"),  # Item number
            dcc.Markdown(df.iloc[i]['Item']),  # Render Markdown
            html.P("Select Score:"),
            dcc.Dropdown(
                id={'type': 'dropdown-score', 'index': i},
                options=[
                    {'label': str(score), 'value': score} for score in range(1, 6)
                ],
                value=3,  # Default value
                clearable=False
            )
        ]))

    return items_div

# Callback to display scores
@app.callback(
    Output('scores-output', 'children'),
    [Input('upload-data', 'contents')],
    [State({'type': 'dropdown-score', 'index': 'all'}, 'value')]
)
def display_scores(contents, scores):
    if contents is None:
        return []
    
    # Create a string to display scores
    score_list = [f"Item {i+1}: {score}" for i, score in enumerate(scores)]
    score_text = "\n".join(score_list)
    
    return html.Div([
        html.Hr(),  # Horizontal line
        html.H3("Scores:"),
        dcc.Markdown("\n".join(score_list))
    ])

# Callback to display scores list when button is clicked
@app.callback(
    Output('scores-list', 'children'),
    [Input('show-scores-button', 'n_clicks')],
    [State({'type': 'dropdown-score', 'index': i}, 'value') for i in range(num_items)]
)
def show_scores_list(n_clicks, *scores):
    if n_clicks == 0:
        return []
    
    # Create a list to display scores
    scores_list = html.Ul([
        html.Li(f"Item {i+1}: {score}") for i, score in enumerate(scores)
    ])
    
    return scores_list

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
