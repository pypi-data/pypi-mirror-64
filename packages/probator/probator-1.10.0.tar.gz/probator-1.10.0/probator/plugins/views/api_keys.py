import string
from uuid import uuid4

from flask import session

from probator.constants import ROLE_ADMIN
from probator.database import db
from probator.log import auditlog
from probator.plugins import BaseView
from probator.schema.base import ApiKey, Role
from probator.utils import generate_password, hash_password
from probator.wrappers import rollback, check_auth


class ApiKeyList(BaseView):
    URLS = ['/api/v1/api-keys']

    @rollback
    @check_auth(ROLE_ADMIN)
    def get(self):
        """List API keys

        Returns:
            flask.Response
        """
        api_keys = db.ApiKey.all()

        return self.make_response({
            'message': None,
            'apiKeys': [x.to_json() for x in api_keys]
        })

    @rollback
    @check_auth(ROLE_ADMIN)
    def post(self):
        """Create new API Key

        Attributes:
            description (str): API Key description
            roles (list of str): List of role names to attach to key

        Returns:
            flask.Response
        """
        self.reqparse.add_argument('description', type=str, required=True)
        self.reqparse.add_argument('roles', type=str, action='append', required=True)
        args = self.reqparse.parse_args()

        api_key_id = uuid4()
        secret_key = generate_password(length=64, characters=string.ascii_letters + string.digits)

        api_key = ApiKey()
        api_key.api_key_id = api_key_id
        api_key.secret_key = hash_password(secret_key)
        api_key.description = args.description
        api_key.roles = [Role.get(role) for role in args.roles]

        db.add(api_key)
        db.commit()

        return self.make_response(
            {
                'message': 'API Key created',
                'apiKey': api_key,
                'secretKey': secret_key
            }
        )


class ApiKeyDetail(BaseView):
    URLS = ['/api/v1/api-key/<string:api_key_id>']

    @rollback
    @check_auth(ROLE_ADMIN)
    def get(self, api_key_id):
        """Return details about an API key

        Args:
            api_key_id (str): API Key ID

        Returns:
            flask.Response
        """
        api_key = db.ApiKey.filter(ApiKey.api_key_id == api_key_id).first()
        if api_key:
            return self.make_response({
                'message': None,
                'apiKey': api_key
            })
        else:
            return self.make_response({
                'message': 'Unable to find API Key',
                'apiKey': None
            })

    @rollback
    @check_auth(ROLE_ADMIN)
    def delete(self, api_key_id):
        """Delete an account

        Args:
            api_key_id (str): API Key ID

        Returns:
            flask.Response
        """
        apikey = db.ApiKey.filter(ApiKey.api_key_id == api_key_id).first()
        if not apikey:
            raise Exception('No such API Key found')

        db.delete(apikey)
        db.commit()

        auditlog(event='apikey.delete', actor=session['user'].username, data={'apiKeyId': api_key_id})

        return self.make_response('API Key deleted')
