from flask import session, current_app, request
from munch import munchify
from sqlalchemy import or_

from probator.constants import ROLE_ADMIN, ROLE_USER, HTTP
from probator.database import db
from probator.log import auditlog
from probator.plugins import BaseView
from probator.schema import User, Role
from probator.utils import generate_password, hash_password
from probator.wrappers import check_auth, rollback


class UserList(BaseView):
    URLS = ['/api/v1/users']

    @rollback
    @check_auth(ROLE_ADMIN)
    def get(self):
        """List all users"""
        self.reqparse.add_argument('page', type=int, default=1)
        self.reqparse.add_argument('count', type=int, default=50, choices=[25, 50, 100])
        self.reqparse.add_argument('authSystem', dest='auth_system', type=str, default=None, action='append')
        self.reqparse.add_argument('search', type=str, default=None)
        args = self.reqparse.parse_args()

        qry = db.User.order_by(User.username)
        if args.auth_system:
            qry = qry.filter(User.auth_system.in_(args.auth_system))

        if args.search:
            search = f'%{args.search}%'
            qry = qry.filter(
                or_(
                    User.username.ilike(search),
                    User.name.ilike(search),
                    User.email.ilike(search)
                )
            )

        total = qry.count()
        qry = qry.limit(args.count)

        if args.page > 0:
            offset = args.page * args.count
            qry = qry.offset(offset)

        users = qry.all()
        return self.make_response({
            'users': [x.to_json() for x in users],
            'userCount': total,
            'authSystems': list(current_app.available_auth_systems.keys()),
            'activeAuthSystem': current_app.active_auth_system.name
        })

    @rollback
    @check_auth(ROLE_ADMIN)
    def post(self):
        """Create a new user"""
        self.reqparse.add_argument('username', type=str, required=True)
        self.reqparse.add_argument('authSystem', dest='auth_system', type=str, required=True)
        self.reqparse.add_argument('name', type=str, default=None)
        self.reqparse.add_argument('email', type=str, default=None)
        self.reqparse.add_argument('roles', type=str, action='append', default=[])
        args = self.reqparse.parse_args()
        auditlog(event='user.create', actor=session['user'].username, data=args)

        user = db.User.find_one(
            User.username == args.username,
            User.auth_system == args.auth_system
        )
        roles = []
        if user:
            return self.make_response(f'User {args.username} already exists', HTTP.BAD_REQUEST)

        if args.auth_system not in current_app.available_auth_systems:
            return self.make_response(f'The {args.auth_system} auth system does not allow local edits', HTTP.BAD_REQUEST)

        if current_app.available_auth_systems[args.auth_system].readonly:
            return self.make_response(
                f'You cannot create users for the {args.auth_system} auth system as it is handled externally',
                HTTP.BAD_REQUEST
            )

        for role_name in args.roles:
            role = db.Role.find_one(Role.name == role_name)

            if not role:
                return self.make_response(f'No such role {role_name}', HTTP.BAD_REQUEST)

            if role_name == ROLE_ADMIN and ROLE_ADMIN not in session['user'].roles:
                self.log.error(f'User {session["user"].username} tried to grant admin privileges to {args.username}')
                return self.make_response('You do not have permission to grant admin privileges', HTTP.FORBIDDEN)

            roles.append(role)

        auth_sys = current_app.available_auth_systems[args.auth_system]
        password = generate_password()

        user = User()
        user.username = args.username
        user.password = hash_password(password)
        user.auth_system = auth_sys.name
        user.name = args.name
        user.email = args.email
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        User.add_role(user, roles)

        return self.make_response({
            'message': f'User {user.auth_system}/{user.username} has been created',
            'user': user,
            'password': password
        })

    @rollback
    @check_auth(ROLE_ADMIN)
    def options(self):
        """Returns metadata information required for User Creation"""
        roles = db.Role.all()

        return self.make_response({
            'roles': roles,
            'authSystems': list(current_app.available_auth_systems.keys()),
            'activeAuthSystem': current_app.active_auth_system.name
        })


class UserDetails(BaseView):
    URLS = ['/api/v1/user/<int:user_id>']

    @rollback
    @check_auth(ROLE_ADMIN)
    def get(self, user_id):
        """Returns a specific user"""
        user = db.User.find_one(User.user_id == user_id)
        roles = db.Role.all()

        if not user:
            return self.make_response('Unable to find the user requested, might have been removed', HTTP.NOT_FOUND)

        return self.make_response({
            'user': user.to_json(),
            'roles': roles
        }, HTTP.OK)

    @rollback
    @check_auth(ROLE_ADMIN)
    def put(self, user_id):
        """Update a user object"""
        data = munchify(request.json)
        if 'roles' not in data:
            return self.make_response('Invalid request, missing required value roles', HTTP.BAD_REQUEST)

        new_roles = data.roles

        user = db.User.find_one(User.user_id == user_id)
        roles = db.Role.find(Role.name.in_(new_roles))
        if not user:
            return self.make_response(f'No such user found: {user_id}', HTTP.NOT_FOUND)

        if user.username == 'admin' and user.auth_system == 'Local Authentication':
            return self.make_response('You cannot modify the built-in admin user', HTTP.FORBIDDEN)

        user.name = data.name
        user.email = data.email

        user.roles = []
        for role in roles:
            if role in new_roles:
                user.roles.append(role)

        db.session.add(user)
        db.session.commit()

        auditlog(event='user.create', actor=session['user'].username, data={'roles': new_roles})
        return self.make_response({'message': 'User roles updated'}, HTTP.OK)

    @rollback
    @check_auth(ROLE_ADMIN)
    def delete(self, user_id):
        """Delete a user"""
        auditlog(event='user.delete', actor=session['user'].username, data={'userId': user_id})
        if session['user'].user_id == user_id:
            return self.make_response(
                'You cannot delete the user you are currently logged in as',
                HTTP.FORBIDDEN
            )

        user = db.User.find_one(User.user_id == user_id)
        if not user:
            return self.make_response(f'No such user id found: {user_id}', HTTP.UNAUTHORIZED)

        if user.username == 'admin' and user.auth_system == 'builtin':
            return self.make_response('You cannot delete the built-in admin user', HTTP.FORBIDDEN)

        username = user.username
        auth_system = user.auth_system
        db.session.delete(user)
        db.session.commit()

        return self.make_response(f'User {auth_system}/{username} has been deleted', HTTP.OK)


class PasswordReset(BaseView):
    URLS = ['/api/v1/user/password/<int:user_id>']

    @rollback
    @check_auth(ROLE_USER)
    def put(self, user_id):
        if user_id == session['user'].user_id:
            self.reqparse.add_argument('password', type=str, required=False)
            args = self.reqparse.parse_args()

            if args.password:
                password = args.password
                provided = True
            else:
                password = generate_password()
                provided = False
        else:
            password = generate_password()
            provided = False

        user = db.User.find_one(User.user_id == user_id)
        if not user:
            return self.make_response('User not found', HTTP.NOT_FOUND)

        if ROLE_ADMIN not in session['user'].roles and user_id != session['user'].user_id:
            self.log.warning(f'{session["user"].user_id} tried to change the password for another user')
            return self.make_response('You cannot change other users passwords', HTTP.FORBIDDEN)

        authsys = current_app.available_auth_systems[user.auth_system]
        if authsys.readonly:
            return self.make_response(f'You cannot reset passwords for the {authsys.name} based users', HTTP.FORBIDDEN)

        user.password = hash_password(password)
        db.session.add(user)
        db.session.commit()

        auditlog(event='user.passwordReset', actor=session['user'].username, data={'password': '*REDACTED*'})

        return self.make_response({
            'message': f'Password reset for {user.auth_system}/{user.username}',
            'user': user.to_json(),
            'password': password if not provided else None
        }, HTTP.OK)
