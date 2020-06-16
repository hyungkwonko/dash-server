import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1("Dash Tutorial"),
    dcc.Graph(id='example',
    figure = {
        'data': [
            {'x': [1,2,3,4,5], 'y': [5,6,7,3,2], 'type': 'line', 'name': 'Trial1'},
            {'x': [1,2,3,4,5], 'y': [3,4,3,4,2], 'type': 'bar', 'name': 'Trial2'},
        ],
        'layout': {
            'title': 'basic dash example'
        }
    })
])

if __name__ == "__main__":
    app.run_server(debug=True)
