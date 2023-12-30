from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go
from text_func import *
from dictionary import *
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

df_0 = scrape_linkedin_jobs(number_of_jobs=50, exact_match=True)
df_1 = process_dataframe(df_0, '27 December 2023')

import regex as re
# Initialize a result dictionary
result = {}

# Iterate over your dictionary
for category, words in classification_dict.items():
    # Initialize a dictionary for the category
    category_dict = {}
    
    # Iterate over the words in the category
    for word in words:
        # Count the occurrences of the word in the 'job_description' column
        category_dict[word] = df_1['job_description'].apply(lambda x: len(re.findall(rf'\b{word}\b', x, re.IGNORECASE))).sum()
    
    # Convert the category dictionary to a DataFrame and store it in the result dictionary
    result[category] = pd.DataFrame(list(category_dict.items()), columns=['Word', 'Count'])

pl = result['programming_languages'][result['programming_languages']['Count'] > 0]
mlt = result['machine learning task'][result['machine learning task']['Count']>0]
db = result['database'][result['database']['Count']>0]
cp = result['cloud platform'][result['cloud platform']['Count']>0]
mla = result['machine learning algorithm'][result['machine learning algorithm']['Count']>0]

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Job Analysis', value='tab-1'),
        dcc.Tab(label='Job Specification', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Content of Tab 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph(id='pie-chart-programming-language', 
                      figure={
                          'data': [go.Pie(labels=pl['Word'], values=pl['Count'], textinfo='label+percent')],
                          'layout': go.Layout(title='Programming Language Used by Data Scientist', showlegend=False)},
                      style={'display': 'inline-block', 'width': '45%'}),
            dcc.Graph(id='pie-chart-ml-task', 
                      figure={
                          'data': [go.Pie(labels=mlt['Word'], values=mlt['Count'], textinfo='label+percent')],
                          'layout': go.Layout(title='Machine Learning Task of Data Scientist', showlegend=False)},
                      style={'display': 'inline-block', 'width': '45%'}),
            dcc.Graph(id='pie-chart-ml-algorithm', 
                      figure={
                          'data': [go.Pie(labels=mla['Word'], values=mla['Count'], textinfo='label+percent')],
                          'layout': go.Layout(title='Machine Learning Algorithm Used', showlegend=False)},
                      style={'display': 'inline-block', 'width': '45%'}),
            dcc.Graph(id='pie-chart-database', 
                    figure={
                        'data': [go.Pie(labels=db['Word'], values=db['Count'], textinfo='label+percent')],
                        'layout': go.Layout(title='Database Used', showlegend=False)},
                    style={'display': 'inline-block', 'width': '45%'}),
            dcc.Graph(id='pie-chart-cloud', 
                    figure={
                        'data': [go.Pie(labels=cp['Word'], values=cp['Count'], textinfo='label+percent')],
                        'layout': go.Layout(title='Cloud Platform Used', showlegend=False)},
                    style={'display': 'inline-block', 'width': '45%'})
        ])
    
if __name__ == '__main__':
    app.run_server(debug=True)
