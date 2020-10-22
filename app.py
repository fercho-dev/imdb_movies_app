import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import plotly.express as px
from load import load_data

external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/sandstone/bootstrap.min.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# ------------------------ Load data --------------------------------
data = load_data()

# ------------------------ App layout -------------------------------
colors = {"table_header": "#70C6FF", "table_header2": "#E7CCC5"}
app.layout = html.Div(children=[
    # ------------------------- First Row -------------------------------------
    # ------------------------- Navbar with input and search button -----------
    dbc.Row(dbc.Col(dbc.Navbar(
            [
                html.A(
                    dbc.Row(
                        [dbc.Col(dbc.NavbarBrand("IMDb Explorer")), ],
                        align="center",
                        no_gutters=True,
                    ),
                ),
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(dbc.Row(
                    [
                        dbc.Col(dbc.Input(id="search_input",
                                          type="search",
                                          placeholder="Search a movie")),
                        dbc.Col(
                            dbc.Button(
                                "Search", color="info", id="search_button"),
                            width="auto",
                        ),
                    ],
                    no_gutters=True,
                    className="ml-auto flex-nowrap mt-3 mt-md-0",
                    align="center",
                ),
                    id="navbar-collapse", navbar=True
                ),
            ],
            color="dark",
            dark=True,
            ),
        width={"size": 12, "offset": 0}
    ),
    ),
    # ---------------------- Second row ------------------------------
    dbc.Row(
        dbc.Col(
            html.H4(children="Explore IMDb best and worst rated movies.",
                    style={"textAlign": "left"}
                    ),
            width={"size": 12, "offset": 0}
        ),
    ),
    # ---------------------- Third Row ---------------------------------------
    dbc.Row(
        dbc.Col(
            html.H6(children="Use dropdowns to filter the data.",
                    style={"textAlign": "left"}
                    ),
            width={"size": 12, "offset": 0}
        ),
    ),

    # ---------------------- Fourth Row --------------------------------------
    dbc.Row([
        # ------------------ Dropdown for query -------------------------------
        dbc.Col(
            dcc.Dropdown(id="query_dropdown",
                         options=[{"label": "Best Rated", "value": "best rated"},
                                  {"label": "Worst Rated", "value": "worst rated"}
                                  ],
                         multi=False,
                         value="best rated"),
            width={"size": 2, "order": 1, "offset": 0}
        ),
        # ----------------- Dropdown for gender ------------------------------
        dbc.Col(
            dcc.Dropdown(id="gender_dropdown",
                         options=[{"label": "Males", "value": "males"},
                                  {"label": "Females", "value": "females"},
                                  {"label": "Males and Females",
                                      "value": "males and females"}
                                  ],
                         multi=False,
                         value="males and females"),
            width={"size": 2, "order": 3, "offset": 0}
        ),
        # ---------------- Dropdown for Age ----------------------------------
        dbc.Col(
            dcc.Dropdown(id="age_dropdown",
                         options=[{"label": "All", "value": "all"}
                                  ],
                         multi=False,
                         value="all"),
            width={"size": 2, "order": 4, "offset": 0}
        ),
        # ---------------- Dropdown for decade ----------------------------------
        dbc.Col(
            dcc.Dropdown(id="decade_dropdown",
                         options=[{"label": "All decades", "value": "all"},
                                  {"label": "1920-1929",
                                      "value": "[1920, 1930)"},
                                  {"label": "1930-1939",
                                      "value": "[1930, 1940)"},
                                  {"label": "1940-1949",
                                      "value": "[1940, 1950)"},
                                  {"label": "1950-1959",
                                      "value": "[1950, 1960)"},
                                  {"label": "1960-1969",
                                      "value": "[1960, 1970)"},
                                  {"label": "1970-1979",
                                      "value": "[1970, 1980)"},
                                  {"label": "1980-1989",
                                      "value": "[1980, 1990)"},
                                  {"label": "1990-1999",
                                      "value": "[1990, 2000)"},
                                  {"label": "2000-2009",
                                      "value": "[2000, 2010)"},
                                  {"label": "2010-2020",
                                      "value": "[2010, 2021)"}
                                  ],
                         multi=False,
                         value="all"),
            width={"size": 2, "order": 2, "offset": 0}
        ),
    ]),
    # -------------------- Fith Row -----------------------------------------
    # -------------------- Table title --------------------------------------
    dbc.Row(
        dbc.Col(
            html.H2(children=[],
                    id="table_title",
                    style={"textAlign": "center"}
                    ),
            width={"size": 12, "offset": 0}
        ),
    ),
    # -------------------- Sixth Row ---------------------------------------
    # -------------------- Table -------------------------------------------
    dbc.Row(
        dbc.Col(
            dash_table.DataTable(
                id="table",
                style_cell={'textAlign': 'left', 'height': 'auto',
                            'minWidth': '160px', 'width': '160px', 'maxWidth': '160px',
                            'whiteSpace': 'normal'},
                style_header={
                    'backgroundColor': colors["table_header"],
                    'fontWeight': 'bold'
                },
                columns=[],
                data=[]
            ),
            width={"size": 10, "offset": 1}
        ),
    ),
])


# ------------------------ Callbacks --------------------------------
# create table
@app.callback(
    [Output("table_title", "children"),
     Output("table", "columns"),
     Output("table", "data")],
    [Input("query_dropdown", "value"),
     Input("gender_dropdown", "value"),
     Input("decade_dropdown", "value")]
)
def make_table(query_value, gender_value, decade_value):
    # ----------------------------- make table title -----------------------
    if decade_value != "all":
        decade = decade_value.lstrip("[").rstrip(")")
        decade = decade.split(", ")
        decade_start = decade[0]
        decade_end = decade[1]
        title = f"{query_value} movies from {decade_start} to {decade_end} by {gender_value}".upper()
    else:
        title = f"{query_value} movies by {gender_value}".upper()

    # ----------------------------- make table --------------------------------
    # ------------------------------- query best rated ------------------------
    if query_value == "best rated":
        # --------------------------- query males votes -----------------------
        if gender_value == "males":
            # ----------------------- query all decades -----------------------
            if decade_value == "all":
                df = data[['original_title', 'director', 'year',
                           'males_allages_avg_vote', 'country']]
                df = df.sort_values(
                    by='males_allages_avg_vote', ascending=False)[:10]
                columns = [{"name": i, "id": i} for i in df.columns]
                table = df.to_dict("records")
            # ----------------------- query a specific decade ------------------
            else:  # filter data by decade
                df = data[data['decade'] == decade_value][[
                    'original_title', 'director', 'year', 'males_allages_avg_vote', 'country']]
                df = df.sort_values(
                    by='males_allages_avg_vote', ascending=False)[:10]
                columns = [{"name": i, "id": i} for i in df.columns]
                table = df.to_dict("records")
        # ----------------------------- query females votes ------------------
        elif gender_value == "females":
            # ----------------------- query all decades -----------------------
            if decade_value == "all":
                df = data[['original_title', 'director', 'year',
                           'females_allages_avg_vote', 'country']]
                df = df.sort_values(
                    by='females_allages_avg_vote', ascending=False)[:10]
                columns = [{"name": i, "id": i} for i in df.columns]
                table = df.to_dict("records")
            # ----------------------- query a specific decade ------------------
            else:  # filter data by decade
                df = data[data['decade'] == decade_value][[
                    'original_title', 'director', 'year', 'females_allages_avg_vote', 'country']]
                df = df.sort_values(
                    by='females_allages_avg_vote', ascending=False)[:10]
                columns = [{"name": i, "id": i} for i in df.columns]
                table = df.to_dict("records")
        # ----------------------------- query males and females votes ---------
        else:  # males and females
            # ------------------------- query all decades ----------------------
            if decade_value == "all":
                df = data[['original_title', 'director', 'year',
                           'avg_vote', 'country']]
                df = df.sort_values(by='avg_vote', ascending=False)[:10]
                columns = [{"name": i, "id": i} for i in df.columns]
                table = df.to_dict("records")
            # -------------------------- query a specific decade -----------------
            else:  # filter data by decade
                df = data[data['decade'] == decade_value][[
                    'original_title', 'director', 'year', 'avg_vote', 'country']]
                df = df.sort_values(by='avg_vote', ascending=False)[:10]
                columns = [{"name": i, "id": i} for i in df.columns]
                table = df.to_dict("records")

    # --------------------------------- query worst rated movies -------------------
    elif query_value == "worst rated":
        # ---------------------------- query males votes --------------------------
        if gender_value == "males":
            # ----------------------- query all decades -----------------------
            if decade_value == "all":
                df = data[['original_title', 'director', 'year',
                           'males_allages_avg_vote', 'country']]
                df = df.sort_values(
                    by='males_allages_avg_vote', ascending=True)[:10]
                columns = [{"name": i, "id": i} for i in df.columns]
                table = df.to_dict("records")
            # ----------------------- query a specific decade ------------------
            else:  # filter data by decade
                df = data[data['decade'] == decade_value][[
                    'original_title', 'director', 'year', 'males_allages_avg_vote', 'country']]
                df = df.sort_values(
                    by='males_allages_avg_vote', ascending=True)[:10]
                columns = [{"name": i, "id": i} for i in df.columns]
                table = df.to_dict("records")
        # ---------------------------- query females votes ------------------------
        elif gender_value == "females":
            # ----------------------- query all decades -----------------------
            if decade_value == "all":
                df = data[['original_title', 'director', 'year',
                           'females_allages_avg_vote', 'country']]
                df = df.sort_values(
                    by='females_allages_avg_vote', ascending=True)[:10]
                columns = [{"name": i, "id": i} for i in df.columns]
                table = df.to_dict("records")
            # ----------------------- query a specific decade ------------------
            else:  # filter data by decade
                df = data[data['decade'] == decade_value][[
                    'original_title', 'director', 'year', 'females_allages_avg_vote', 'country']]
                df = df.sort_values(
                    by='females_allages_avg_vote', ascending=True)[:10]
                columns = [{"name": i, "id": i} for i in df.columns]
                table = df.to_dict("records")
        # ----------------------------- query males and females votes -------------
        else:  # males and females
            # ------------------------ query all decades --------------------------
            if decade_value == "all":
                df = data[['original_title', 'director', 'year',
                           'avg_vote', 'country']]
                df = df.sort_values(by='avg_vote', ascending=True)[:10]
                columns = [{"name": i, "id": i} for i in df.columns]
                table = df.to_dict("records")
            # ---------------------------- query a specific decade -----------------
            else:  # filter data by decade
                df = data[data['decade'] == decade_value][[
                    'original_title', 'director', 'year', 'avg_vote', 'country']]
                df = df.sort_values(by='avg_vote', ascending=True)[:10]
                columns = [{"name": i, "id": i} for i in df.columns]
                table = df.to_dict("records")

    return title, columns, table


# ------------------------ Run app ----------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
