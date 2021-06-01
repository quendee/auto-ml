import pandas as pd
import base64
import io
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from mlapp import dash_utils
from mlapp.helper import helper


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

aws_form, aws_ids = dash_utils.form(out_id="setup-js", aws_region = "AWS Region", aws_akey = "AWS Access Key", aws_secret = "AWS Secret Key")

uploade = dash_utils.uploader()

selectr = dash_utils.selector()

page_1_layout = html.Div([dcc.Store(id='data-session', storage_type='session'),
dbc.Row([dbc.Col([uploade]), dbc.Col([aws_form, selectr])]
    ,no_gutters = True)
])


@app.callback([Output('data-session', 'data'),
              Output('output-data-upload', 'children'),
              Output("setup-js", "run")],
              Input('upload-data', 'contents'),
              [State('upload-data', 'filename'),
              State('separator', 'value')])
def parse_contents(contents, filename, separator):
    if contents is None:
        raise PreventUpdate
    filename = filename[0]
    _, content_string = contents[0].split(separator)

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        out = df.to_json(orient="records")
    except Exception as e:
        out_result = helper.create_pop(f"Failed due to {e}", "error", "Failed!")
        return None, None, out_result
    
    table = dbc.Table.from_dataframe(df.head(), striped=True, bordered=True, hover=True, responsive = True, dark = True)
    out_result = helper.create_pop(f"Successfully read the data", "success", "Success!")


    return json.dumps(out), table, out_result


@app.callback(
    Output("dropdown-pipes", "options"),
    Input("data-session", "data")
)
def p1_update(data):
    if data is None:
        raise PreventUpdate
    try:
        tab = json.loads(data)
        tab = pd.read_json(tab, orient='records')
        cols = list(tab.columns)
        final = helper.update_options(cols)
        return final
    except Exception as e: 
        return [{'label': "error", 'value': f"error {e}"}]

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/setup':
        return page_1_layout


if __name__ == '__main__':
    app.run_server(debug=True, host = "0.0.0.0")
