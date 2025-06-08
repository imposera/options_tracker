import dash
from dash import html, dcc, Input, Output, State, ctx, dash_table
import pandas as pd
import uuid
import datetime

# Sample structure for initial antifragile options data
initial_data = [
    {
        "id": str(uuid.uuid4()),
        "Ticker": "SPY",
        "Strategy": "Tail Hedge",
        "Strike(s)": "400P",
        "Type": "Long Put",
        "Premium Paid": 38,
        "DTE": 17,
        "Breakeven": 362,
        "Convex Zone": "< 390",
        "Status": "Active"
    },
    {
        "id": str(uuid.uuid4()),
        "Ticker": "FUBO",
        "Strategy": "Munchkin Ladder",
        "Strike(s)": "1C/2C",
        "Type": "Long Call",
        "Premium Paid": 65,
        "DTE": "10/24",
        "Breakeven": "1.65 avg",
        "Convex Zone": "> 2.10",
        "Status": "Tracking"
    },
    {
        "id": str(uuid.uuid4()),
        "Ticker": "SOFI",
        "Strategy": "Earnings Strangle",
        "Strike(s)": "6C/5P",
        "Type": "Strangle",
        "Premium Paid": 80,
        "DTE": 8,
        "Breakeven": "5.85/6.15",
        "Convex Zone": "> 7 or < 4",
        "Status": "Awaiting ER"
    }
]

# Convert to DataFrame
df = pd.DataFrame(initial_data)

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Antifragile Options Tracker"),

    html.Div([
        html.Button("Add New Position", id="add-btn", n_clicks=0),
        html.Div(id="form-div", style={"marginTop": 20}),
    ]),

    dash_table.DataTable(
        id='positions-table',
        columns=[
            {"name": col, "id": col, "editable": True} for col in df.columns if col != "id"
        ] + [{"name": "Remove", "id": "remove", "presentation": "markdown"}],
        data=df.to_dict("records"),
        editable=True,
        row_deletable=False,
        style_table={'overflowX': 'auto'},
        style_cell={"textAlign": "left"},
    ),
    dcc.Store(id='positions-store', data=df.to_dict("records"))
])

# Callback to add a new row
def new_position():
    return {
        "id": str(uuid.uuid4()),
        "Ticker": "",
        "Strategy": "",
        "Strike(s)": "",
        "Type": "",
        "Premium Paid": 0,
        "DTE": "",
        "Breakeven": "",
        "Convex Zone": "",
        "Status": ""
    }

@app.callback(
    Output("positions-table", "data"),
    Input("add-btn", "n_clicks"),
    State("positions-table", "data"),
    prevent_initial_call=True
)
def add_row(n_clicks, rows):
    rows.append(new_position())
    return rows

if __name__ == '__main__':
    app.run(debug=True)

