from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError
from requests.exceptions import HTTPError

from flask import redirect, url_for, Response, session, logging

from flask_dance.consumer import OAuth2ConsumerBlueprint, oauth_error

from .auth import Auth


class OktaOAuth2ConsumerBlueprint(OAuth2ConsumerBlueprint):
    """
    This subclass makes access_denied and invalid_token oauth_errors accessible.
    """
    def __init__(self, app, name, import_name, **kwargs):
        super().__init__(name, import_name, **kwargs)
        self.access_denied = False
        self.invalid_token = False
        self.logger = logging.create_logger(app)

    @oauth_error.connect
    def auth_error(self, error, error_description, error_uri):
        self.logger.error(f"{error}: {error_description} {error_uri}")
        if error == 'access_denied':
            self.access_denied = True
        if error == 'invalid_token':
            self.invalid_token = True


class OktaOAuth(Auth):
    def __init__(self, app, additional_scopes=None):
        super().__init__(app)
        self.base_url = app.server.config['OKTA_BASE_URL']
        self.logger = logging.create_logger(app.server)
        self.okta = OktaOAuth2ConsumerBlueprint(
            app=app.server,
            name='okta',
            import_name=__name__,
            client_id=app.server.config['OKTA_OAUTH_CLIENT_ID'],
            client_secret=app.server.config['OKTA_OAUTH_CLIENT_SECRET'],
            base_url=self.base_url,
            token_url=f'{self.base_url}/token',
            authorization_url=f'{self.base_url}/authorize',
            scope=['openid', 'email', 'profile'] + (additional_scopes if additional_scopes else []),
            # by default a login redirects to the root page
        )
        app.server.register_blueprint(self.okta, url_prefix="/login")

    def is_authorized(self):
        if not self.okta.session.authorized:
            return False
        try:
            resp = self.okta.session.get(f'{self.base_url}/userinfo')
            resp.raise_for_status()
            if resp.ok:
                json_response = resp.json()
                session['user_name'] = json_response.get('name')
                session['user_nickname'] = json_response.get('nickname')
                session['user_given_name'] = json_response.get('given_name')
                session['user_middle_name'] = json_response.get('middle_name')
                session['user_family_name'] = json_response.get('family_name')
                session['user_profile'] = json_response.get('profile')
                session['user_zoneinfo'] = json_response.get('zoneinfo')
                session['user_updated_at'] = json_response.get('updated_at')
                session['user_locale'] = json_response.get('locale')
                session['user_email'] = json_response.get('email')
                session['user_email_verified'] = json_response.get('email_verified')
                session['user_address'] = json_response.get('address')
                session['user_preferred_username'] = json_response.get('preferred_username')
                session['user_phone_number'] = json_response.get('phone_number')
                return True
        except HTTPError:
            # resp.status_code == 401 Happens e.g. when a user token was revoked.
            return False
        except (InvalidGrantError, TokenExpiredError):
            # no clue which other errors require this behavior, add when required for now raise
            return False

    def login_request(self):
        if self.okta.access_denied:
            # by setting self.okta.access_denied to False we allow a new auth dance when a user manually reloads
            # if the user is assigned to this application in the meantime, a reload is sufficient to load the page.
            self.okta.access_denied = False
            return Response(status=403)
        return redirect(url_for("okta.login"))

    def auth_wrapper(self, f):
        def wrap(*args, **kwargs):
            if self.is_authorized():
                response = f(*args, **kwargs)
            else:
                return self.login_request()
            return response
        return wrap

    def index_auth_wrapper(self, original_index):
        def wrap(*args, **kwargs):
            if self.is_authorized():
                return original_index(*args, **kwargs)
            else:
                return self.login_request()
        return wrap
