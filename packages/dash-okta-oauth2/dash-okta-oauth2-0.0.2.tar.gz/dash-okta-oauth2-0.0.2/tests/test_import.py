"""
Test Dash Okta Auth.
"""

import pytest

from dash_okta_oauth2 import OktaOAuth

from dash import Dash
from flask import Flask


@pytest.fixture
def app(name='dask'):
    """Dash App."""
    server = Flask(name)
    server.config["OKTA_OAUTH_CLIENT_ID"] = ""
    server.config["OKTA_OAUTH_CLIENT_SECRET"] = ""
    server.config["OKTA_BASE_URL"] = ""
    return Dash(name, server=server,
                url_base_pathname='/')


def test_init(app):
    """Test initialisation."""
    auth = OktaOAuth(app)

    assert auth.app is app
