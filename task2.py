from pathlib import Path
from dash import Dash, html, dcc, Input, Output, callback, ctx
import plotly.express as px
import pandas as pd

app = Dash()

folder = Path("data")   # e.g., Path("data")
files = sorted(folder.glob("*.csv"))

PALETTE = {
    "north": "#1f77b4",
    "south": "#ff7f0e",
    "east":  "#2ca02c",
    "west":  "#d62728",
}

# Read all and stack vertically
df = pd.concat(
    (pd.read_csv(f) for f in files),
    ignore_index=True
)

df = df[df["product"] == "pink morsel"]

clean_price = df["price"].str[1:]

df["price_num"] = pd.to_numeric(clean_price, errors="coerce")

newdf = pd.DataFrame({
    "Sales":df["price_num"] * df["quantity"],
    "date":df["date"],
    "region":df["region"]
    }
)

# optional: write it back out
newdf.to_csv("all_data.csv", index=False)

markdown_text = '''
### Markdown in Dash

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app.layout = html.Div(children=[
    html.H1(children='Sales for Pink Morsel',style={'textAlign': 'center', 'color': '#7FDBFF'}),

    html.Div(children='Dash: A web application framework for your data.'),
    
    html.Div(
        [
            html.Label("Region:", htmlFor="selected-region"),
            dcc.RadioItems(
                options=newdf['region'].unique(),
                value="north",           
                inline=True,
                id='selected-region'              
        )
        ], style={
            "display": "flex",
            "alignItems": "center",
            "gap": "8px",
            "whiteSpace": "nowrap",     # keep "Region:" from wrapping
            "width": "48%",
        }),


    dcc.Graph(
        id='region-sales-graph'
    ),
    
    dcc.Markdown(children = markdown_text)
    
])

@callback(
    Output('region-sales-graph', 'figure'),
    Input('selected-region', 'value'))

def update_graph(selectedregion):
    dff = newdf[newdf['region'] == selectedregion]

    fig = px.line(x=dff["date"], y=dff["Sales"])
    
    fig.update_traces(line_color=PALETTE.get(selectedregion, "#636EFA"))
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    
    return fig

def update(region):
    return f'Region is {region}.'

def display(region):
    button_clicked = ctx.triggered_id
    return f'You last clicked button with ID {button_clicked}'

if __name__ == '__main__':
    app.run(debug=True)
