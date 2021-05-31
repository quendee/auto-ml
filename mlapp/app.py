import typing
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from auto-ml import dash_utils
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_scripts=["//cdn.jsdelivr.net/npm/sweetalert2@10"], external_stylesheets=[dbc.themes.SANDSTONE], suppress_callback_exceptions=True)

content = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
    ])


navbar = dash_utils.nav()

app.layout = dbc.Container([
    navbar,
    content
    ],
    fluid=True
)

aws_form, aws_ids = dash_utils.form(aws_profile = "AWS Profile", aws_akey = "AWS Access Key", aws_secret = "AWS Secret Key")


page_1_layout = html.Div([
dbc.Row(dbc.Col([aws_form]),
    no_gutters = True)
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
            [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/setup':
        return page_1_layout

if __name__ == '__main__':
    app.run_server(debug=True)
