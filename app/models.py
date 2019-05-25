from datetime import datetime
from app.extensions import login, bcrypt
from flask_login import AnonymousUserMixin, UserMixin
from flask_sqlalchemy import BaseQuery
from sqlalchemy import Sequence
from sqlalchemy_searchable import SearchQueryMixin, make_searchable
from sqlalchemy_utils import TSVectorType
from app import db

db.configure_mappers()
make_searchable(db.metadata)

class Permission:
    GENERAL = 0
    ADMINISTER = 1

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.GENERAL, 'main', True),
            'Administer': (Permission.ADMINISTER, 'admin', False)
        }
        for x in roles:
            role = Role.query.filter_by(name=x).first()
            if role is None:
                role = Role(name=x)
            role.permissions = roles[x][0]
            role.index = roles[x][1]
            role.default = roles[x][2]
            db.session.add(role)
        db.session.commit()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    fullnames = db.Column(db.String(104), index=True, unique=False, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    password = db.Column(db.Binary(128), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, username, fullnames,phone_number, role=None, password=None, **kwargs):
        super(User, self).__init__(**kwargs)
        if role:
            self.role = role
        
        db.Model.__init__(self, username=username, fullnames=fullnames, phone_number=phone_number, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None
        
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)
    
    def check_password(self, value):
        return bcrypt.generate_password_hash(self.password, len(value))
    
    def can(self, permisions):
        return self.role.permissions >= permisions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_admin(self):
        return False

class PostQuery(BaseQuery, SearchQueryMixin):
    pass

class Posts(db.Model):
    query_class = PostQuery
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(150))
    description = db.Column(db.String(240))
    image_url = db.Column(db.String(140))
    search_vector = db.Column(TSVectorType('title'))

class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    users = db.relationship(
        'User'
    )

@login.user_loader
def load_user(id):
    return User.query.get(int(id))