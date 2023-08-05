#! /usr/bin/env python

# Example app

import os

import dash_core_components as dcc
import dash_html_components as html

from dash import Dash
from dash.dependencies import Input, Output
from flask import Flask, session

from dash_okta_oauth2 import OktaOAuth

# configure app
server = Flask(__name__)
app = Dash(
    __name__,
    server=server,
    url_base_pathname='/'
)
# app.config['suppress_callback_exceptions']=True

# configure google oauth using environment variables
server.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
server.config["OKTA_OAUTH_CLIENT_ID"] = os.environ["OKTA_OAUTH_CLIENT_ID"]
server.config["OKTA_OAUTH_CLIENT_SECRET"] = os.environ["OKTA_OAUTH_CLIENT_SECRET"]
server.config["OKTA_BASE_URL"] = os.environ["OKTA_BASE_URL"]

# allow for insecure transport for local testing (remove in prod)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

auth = OktaOAuth(app)

@server.route("/")
def MyDashApp():
    return app.index()


app.layout = html.Div(children=[
    html.H1(children="Private Dash App"),

    html.Div(id='placeholder', style={'display':'none'}),
    html.Div(id='welcome'),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 6], 'type': 'bar', 'name': 'Montreal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

@app.callback(
    Output('welcome', 'children'),
    [Input('placeholder', 'children')]
)
def on_load(value):
    return f"Welcome, {session['user_given_name']} {session['user_family_name']}!"

if __name__ == '__main__':
    app.run_server(host='localhost')
