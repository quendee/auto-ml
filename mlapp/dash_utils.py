import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import visdcc


def form(out_id = None, **kwargs):

    ids = []
    forms = []
    for key, val in kwargs.items():
        pres = True
        if isinstance(val, str):
            typee = "text"
        elif (isinstance(val, float)) or (isinstance(val, int)):
            typee = "number"
        if any(x in val.lower() for x in ['key', 'secret', 'pass']):
            typee = "password"
            pres = False
        forms.append(dbc.FormGroup([
            dbc.Label(val, html_for = key),
            dbc.Input(type=typee, id=key, size="30", persistence_type = 'local', persistence = pres, debounce = True, invalid = False),
        ]))
        ids.append(key)
    vis = visdcc.Run_js(id = out_id) if out_id else None
    form = dbc.Card([
            dbc.CardBody(forms),
            vis
            ])

    return form, ids

def nav():
    search_bar = dbc.Row(
    [
        dbc.Col(dbc.NavLink("Setup", href="/setup", active="exact", style = {'color': 'black', 'width':'100px', 'color':'#ff4411'})),
        dbc.Col(dbc.NavLink("Data Fetcher", href="/", active="exact", style = {'color': 'black', 'width':'100px', 'color':'#ff4411'})),
        dbc.Col(dbc.NavLink("Pipeline Steps", href="/pipeline", active="exact",style = {'color': 'black', 'width':'100px', 'color':'#ff4411'})),
        dbc.Col(dbc.NavLink("Process Data", href="/process", active="exact", style = {'color': 'black', 'width':'100px', 'color':'#ff4411'})),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center"
)

    navbar = dbc.Navbar([
                html.A(
                    dbc.Row([
                    dbc.Col(dbc.NavbarBrand("ML Pipeline", style = {'color':'#ff4411', 'font-size': '24px', 'font-weight': 'bold', 'margin-left':'20px'})),
                ],
                    align="center",
                    no_gutters=True,
                    )),
                    dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
                ], className='background'
            )
    return navbar


def uploader():
    up = dbc.Card([
        dbc.CardBody([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'textAlign': 'center',
            'cursor': 'pointer'
        },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        dbc.Label("Separator", html_for = "separator"),
        dbc.Input(type="text", id="separator", persistence_type = 'local', persistence = True, debounce = True, invalid = False, style={"width":"40px"}),
        html.Div(id='output-data-upload'),
    ])
    ])
    return up


def selector():

    lab2 = html.P(
        [
            "Pipeline steps",
        ]
    )
    dd = dbc.Card([
    dbc.CardBody([
    dbc.Input(id = 'path-pipe', type="text", value="steps"),
    dbc.FormText("Enter the bucket where the pipelines were stored", color="secondary"),
    dbc.Label(lab2, html_for="dropdown-pipes"),
    dcc.Dropdown(id="dropdown-pipes",
    multi=True,
    placeholder = "Select processing step"
    ),
    dbc.Button(
    dbc.Spinner(id='loading-process' ,size="sm"),
    id="apply-processing",
    color="primary",
    ),
    visdcc.Run_js(id = 'pipe-res')
    ])
    ])
    return dd
