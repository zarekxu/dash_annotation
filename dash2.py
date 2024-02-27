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
    html.Button('Save Scores', id='save-button', n_clicks=0),
    html.Div(id='save-status')
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

# Callback to save scores to TXT file
@app.callback(
    Output('save-status', 'children'),
    [Input('save-button', 'n_clicks')],
    [State({'type': 'dropdown-score', 'index': 'all'}, 'value')]
)
def save_scores_to_txt(n_clicks, scores):
    if n_clicks == 0:
        return []

    # Create a string to save scores
    score_text = "\n".join([f"Item {i+1}: {score}" for i, score in enumerate(scores)])

    # Save the scores to a new TXT file
    with open('scores.txt', 'w') as f:
        f.write(score_text)

    return html.Div('Scores saved to scores.txt')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
