import os
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, dash_table
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc


os.chdir('C:/Users/HP/Desktop/PROYECTO/C001')

# datos a leer gapminder
df = px.data.gapminder()
df = pd.DataFrame(df)
df.columns = ['pais','continente','anio','esperanzaDeVida','poblacion','pibPercapita','isoAlpha', 'isoNum']
continentesUnicos = df['continente'].unique()


app = dash.Dash(__name__, external_stylesheets=[dbc.themes. FLATLY], suppress_callback_exceptions=True)

# %% ----------------------------------------------------------------------------
# los argumentos de estilo para la barra lateral. 
# Usamos posición:fija y un ancho fijo
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#F3F3F3",
}

# los estilos para el contenido principal lo colocan a la derecha de la barra lateral 
# y agrega algo de relleno.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# %% ----------------------------------------------------------------------------
sidebar = html.Div(
    [
        html.P("MENÚ", className="lead", style={'textAlign':'center'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("INICIO", href="/", active="exact"),
                dbc.NavLink("PAG 01", href="/page-1", active="exact"),
                dbc.NavLink("PAG 02", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
# pagina1 ----------------------
pag1 = html.Div([
    html.H4(children='BIENVENIDO - APP DASH', style={'textAlign':'center'}),
    #html.P("AUTOR: CRISTOPHER CHACHALO"),
    html.Hr(),
    html.Img(src='/assets/001.webp',  style={'margin-top': '2px', 'width': '100%', 'height': 'auto', 'align':'center'}),
])
# pagina1 ----------------------
pag2 = html.Div([
    html.H4(children='BIENVENIDO - APP DASH', style={'textAlign':'center'}),
    #html.P("AUTOR: CRISTOPHER CHACHALO"),
    html.Hr(),
    html.P('Seleccione el continente que desea visualizar'),
    dcc.Dropdown(continentesUnicos, continentesUnicos[:2], multi=True, id='continente_item'),
    dcc.Graph(id='scatter01'),
])
# Add controls to build the interaction
@app.callback(
    Output(component_id='scatter01', component_property='figure'),
    Input(component_id='continente_item', component_property='value')
)
def update_graph(continent):
    df_continente = df[df["continente"].isin(continent)]
    #dfrangeMin = df_continente.groupby('pais')[['pibPercapita','anio']].sum().reset_index()
    #rangexmin = dfrangeMin['pibPercapita'].min()-100
    fig = px.scatter(df_continente, 
                     x='pibPercapita', y='esperanzaDeVida',
                     color='continente',size='poblacion', 
                     size_max=60 ,hover_name='pais',
                     log_x=True, animation_frame='anio',
                     #animation_group='pais', range_x=[rangexmin, 10000], range_y=[25,90],
                     animation_group='pais', range_x=[300, 10000], range_y=[25,90], template='seaborn'
    )
    return fig




# %% ----------------------------------------------------------------------------
# content
content = html.Div(id="page-content", style=CONTENT_STYLE)
# %% ----------------------------------------------------------------------------
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return pag1 # primer pestaña
    elif pathname == "/page-1":
        return pag2
    elif pathname == "/page-2":
        return html.P("Bien, pagina 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: No se encontro la pagina", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(debug =True)
