import datetime
from marshmallow import fields, Schema
from . import db
from ..app import bcrypt

# Schemas tell us how the Model is structured
class SkillsSchema(Schema):
    id = fields.Int(dump_only=True)
    owner_id = fields.Int(required=True)
    content = fields.Str(required=True)

class SkillsModel(db.Model):
    __tablename__ = 'Skills'

    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Testing
    owner_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, data):
        # self.user_id = data.get('data.user.id') # Testing
        self.owner_id = data.get('owner_id')
        self.content = data.get('content')

    def __repr__(self):
        return f'<id {self.id}>'

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    @staticmethod
    def get_all_skills():
        return SkillsModel.query.all()

    @staticmethod
    def get_one_skill(id):
        return SkillsModel.query.get(id)
