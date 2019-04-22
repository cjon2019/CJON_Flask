from flask import request, json, Response, Blueprint
from .. models.user import UserModel, UserSchema
from .. shared.authentication import Auth 

user_api = Blueprint('users', __name__)
user_schema = UserSchema()

def custom_response(res, status_code):
    return Response(
        mimetype = "application/json",
        response = json.dumps(res),
        status=status_code
    )

# READ - Get all Users
@user_api.route('/', methods=['GET'])
# @Auth.auth_required
def get_all():
    users = UserModel.get_all_users()
    ser_users = user_schema.dump(users, many=True)
    print(ser_users)
    return custom_response(ser_users[0], 200)

# READ - Get one User
@user_api.route('/<int:id>', methods=['GET'])
def get_one(id):
    user = UserModel.get_by_id(id)
    ser_data = user_schema.dump(user)
    return custom_response(ser_data[0], 200)

# CREATE new user
@user_api.route('/', methods=['POST'])
def create():
    # Parse requests body json into a python dictionary
    req_data = request.get_json()

    # Pass in the dictionary and load into a user schema
    data = user_schema.load(req_data)
    print(data)
    # if error:
    #     return custom_response(error, 400)

    # Check if User already exists in the db
    user_in_db = UserModel.get_by_email(req_data.get('email'))
    if user_in_db:
        message = {'error': 'User already exists, please supply another email'}
        return custom_response(message, 400)

    # Pass in the user schema and get a User object (model) back
    user = UserModel(data)
    user.save()
    ser_data = user_schema.dump(user)
    token = Auth.generate_token(ser_data[0].get('id'))
    return custom_response({'jwt_token': token}, 201)

# UPDATE user 
# BUG: Trying to update password will give an exception.
@user_api.route('/update/<int:id>', methods=['PUT'])
def update(id):
    req_data = request.get_json()
    new_data = user_schema.load(req_data, partial=True)
    user = UserModel.get_by_id(id)
    user.update(new_data)
    ser_user = user_schema.dump(user)
    return custom_response(ser_user[0], 200)

# DELETE user by Id
@user_api.route('/<int:id>', methods =['DELETE'])
@Auth.auth_required
def delete(id):
    user = UserModel.get_by_id(id)
    user.delete()
    return custom_response({'message': f'Deleted User Id: {id}'}, 204)

# Login to get generate token (token expires after 1 day)
@user_api.route('/login', methods=['POST'])
def login():
    '''
    Validates and returns a web token if the user credentials are verified
    '''
    req_data = request.get_json()
    data = user_schema.load(req_data)
    if not req_data.get('email') or not req_data.get('password'):
        return custom_response({'error': 'Email and Password required to login'})
    user = UserModel.get_by_email(req_data.get('email'))
    if not user:
        return custom_response({'error': 'invalid credentials'}, 400)

    if not user.check_hash(req_data.get('password')):
        return custom_response({'error': 'invalid credentials'})
    ser_data = user_schema.dump(user)
    token = Auth.generate_token(ser_data[0].get('id'))

    return custom_response({
        'jwt_token': token,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email' : user.email,
        'id': user.id}, 200)

# TODO: Fix bug, when trying to update User's Password