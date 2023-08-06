from datetime import datetime

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from flask import session, request

from probator.constants import MSG_INVALID_USER_OR_PASSWORD
from probator.database import db
from probator.plugins import BaseAuthPlugin, BaseView
from probator.schema.base import ApiKey
from probator.utils import generate_csrf_token, generate_jwt_token

ph = PasswordHasher()


class ApiKeyAuthView(BaseView):
    name = 'API Authentication'
    ns = 'auth_api'


class ApiKeyLogin(ApiKeyAuthView):
    URLS = ['/auth/api/login']

    def post(self):
        self.reqparse.add_argument('api_key', type=str, required=True)
        self.reqparse.add_argument('secret_key', type=str, required=True)
        args = self.reqparse.parse_args()

        try:
            api_key = db.ApiKey.filter(ApiKey.api_key_id == args.api_key).first()

            if not api_key:
                self.log.warn(f'Authentication attempt for unknown API key {args.api_key} from {request.remote_addr}')
                return self.make_response(MSG_INVALID_USER_OR_PASSWORD, 400)

            ph.verify(api_key.secret_key, args.secret_key)

            # Setup the user session with all the information required
            session['user'] = api_key
            session['is_api_user'] = True
            session['csrf_token'] = generate_csrf_token()
            session['accounts'] = [x.account_id for x in db.Account.all() if x.user_has_access(api_key)]
            token = generate_jwt_token(api_key, self.name)

            api_key.last_used = datetime.now()
            db.add(api_key)
            db.commit()

            return self.make_response({
                'authToken': token,
                'csrfToken': session['csrf_token']
            }, 200)

        except VerificationError:
            self.log.warn(f'Failed verifying credentials for {args.api_key} from {request.remote_addr}')
            return self.make_response(MSG_INVALID_USER_OR_PASSWORD, 400)

        except Exception as ex:
            self.log.exception(f'Unknown error occured while attempting use API key {args.api_key} from {request.remote_addr}: {ex}')

        finally:
            db.session.rollback()


class ApiKeyLogout(ApiKeyAuthView):
    URLS = ['/auth/api/logout']

    def get(self):
        session.clear()
        return self.make_response('Successfully logged out')


class ApiKeyAuth(BaseAuthPlugin):
    name = 'API Authentication'
    ns = 'auth_api'
    views = (ApiKeyLogin, ApiKeyLogout)
    readonly = False
    login = {'state': 'auth.login'}
    logout = '/auth/api/logout'
    static = True
