import datetime
from marshmallow import fields, Schema
from . import db
from ..app import bcrypt

# Models are used to interact with the database
class UserModel(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, data):
        print(type(data))
        print(data)
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.email = data.get('email')
        self.password = self._generate_hash(data.get('password'))

    def __repr__(self):
        return f'<id {self.id}>'
    
    def _generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode('utf-8')

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def save(self):
        '''Saves current state of model to db'''
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        '''deletes row from db'''
        db.session.delete(self)
        db.session.commit()

    def update(self, data: dict):
        '''takes in data to modify model'''
        for key, item in data.items():
            if key == 'password':
                self.password = self._generate_hash(data)
            setattr(self, key, item)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_by_email(email):
        return UserModel.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(id):
        return UserModel.query.get(id)

# Schemas tell us how the Model is structured
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
