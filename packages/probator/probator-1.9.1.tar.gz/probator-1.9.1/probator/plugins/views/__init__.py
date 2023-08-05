from flask import current_app

from probator.plugins import BaseView


class LoginRedirectView(BaseView):
    def get(self):
        authsys = current_app.active_auth_system
        data = authsys.login
        data['name'] = authsys.name
        return self.make_response(authsys.login)


class LogoutRedirectView(BaseView):
    def get(self):
        authsys = current_app.active_auth_system
        return self.make_response({'url': authsys.logout})
