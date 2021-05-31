import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc


def form(**kwargs):

    ids = []
    forms = []
    for key, val in kwargs.items():
        if isinstance(val, str):
            typee = "text"
        elif (isinstance(val, float)) or (isinstance(val, int)):
            typee = "number"
        if any(x in val.lower() for x in ['key', 'secret', 'pass']):
            typee = "password"
        forms.append(dbc.FormGroup([
            dbc.Label(val, html_for = key),
            dbc.Input(type=typee, id=key, size="30", persistence_type = 'local', persistence = True, debounce = True, invalid = False),
        ]))
        ids.append(key)
    form = dbc.Card([
            dbc.CardBody(forms)   
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