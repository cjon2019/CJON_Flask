from flask import request, json, Response, Blueprint
from .. models.skills import SkillsModel, SkillsSchema
from .. shared.authentication import Auth

skills_api = Blueprint('skills', __name__)
skills_schema = SkillsSchema()

def custom_response(res, status_code):
    return Response(
        mimetype = "application/json",
        response = json.dumps(res),
        status=status_code
    )

# READ - Gets all skills
@skills_api.route('/', methods=['GET'])
def skills_get_all():
    skills = SkillsModel.get_all_skills()
    ser_data, error = skills_schema.dump(skills, many=True)
    print(type(ser_data))
    print(ser_data)
    return custom_response(ser_data, 200)

# READ - Get 1 skill
@skills_api.route('/<int:id>', methods=['GET'])
def skills_get_by_id(id):
    post = SkillsModel.get_one_skill(id)
    if not post:
        return custom_response({'error': 'Skill not found'}, 404)
    data, error = skills_schema.dump(post)
    return custom_response(data, 200)

# CREATE - Post new skill to db
@skills_api.route('/', methods=['POST'])
def skills_create():

    req_data = request.get_json()
    print(f'req_data = {req_data}')

    data, error = skills_schema.load(req_data)
    print(f'data = {data}')

    skills = SkillsModel(data)
    skills.save()

    ser_data, error = skills_schema.dump(skills)
    print(f'ser_data = {ser_data}')
    return custom_response(ser_data, 201)

# UPDATE - Update an existing skill
@skills_api.route('/<int:id>', methods=['PUT'])
def skills_update(id):
    req_data = request.get_json()
    skill = SkillsModel.get_one_skill(id)

    if not skill:
        return custom_response({'error': 'Skill not found'}, 404)

    data, error = skills_schema.dump(skill)

    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response({'error': 'Permission Denied'}, 400)

    data, error = skills_schema.load(req_data, partial=True)

    skill.update(data)
    data, error = skills_schema.dump(skill)
    return custom_response(data, 200)


# Delete - Delete skill from User
@skills_api.route('<int:id>', methods=['DELETE'])
def delete(id):
    post = SkillsModel.get_one_skill(id)

    if not post:
        return custom_response({'error': 'Skill not found'}, 404)

    data, error = skills_schema.dump(post)
    # if data.get('owner_id') != g.user.get('id'):
    #     return custom_response({'error': 'Permission Denied'}, 400)

    post.delete()
    return custom_response({'message': 'Deleted'}, 204)
