from flask import request, json, Response, Blueprint
import requests

jobs_api = Blueprint('jobs', __name__)

headers = {
    'Host': 'data.usajobs.gov',
    'User-Agent': 'nicholas.coxe@gmail.com',
    'Authorization-Key' : 'wN/n6HZljpJ4go21Ct/KB+RCGj1KtIKG3mQSKCZGPe4='
}

def custom_response(res, status_code):
    return Response(
        mimetype = "application/json",
        response = json.dumps(res),
        status=status_code
    )
@jobs_api.route('/', methods=['GET'])
def jobs_get():
    return f'Jobs GET index page'

@jobs_api.route('/', methods=['POST'])
def jobs_post():
    url = 'https://data.usajobs.gov/api/Search?'
    # Get data from POST request
    req_data = request.get_json()
    state = req_data.get('state')
    position = req_data.get('position')
    location_query = f'LocationName={state}'
    position_query = f'PositionTitle={position}'
    final_url = f'https://data.usajobs.gov/api/Search?ResultsPerPage=500&{location_query}&{position_query}'
    response = requests.get(final_url, headers=headers)

    # Convert to Python Dictionary
    data = response.json()

    # Number of Jobs found with query
    result_count = data['SearchResult']['SearchResultCount']
    print(result_count)
    
    # Print Position Titles for all Positions where the LocationName == state
    for i in range(result_count):
        if state in data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionLocation'][0]['LocationName']:
            print(f"Position Title : {data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionTitle']}")

    # Converts JSON back into a string, so that the browser can render it
    json_formatted_string = json.dumps(data)
    print(type(json_formatted_string))
    return json_formatted_string

@jobs_api.route('/state/<string:state>', methods=['GET'])
def job_state_query(state):
    url = 'https://data.usajobs.gov/api/Search?'
    location_query = f'ResultsPerPage=500&LocationName={state}/'
    final_url = url + location_query
    response = requests.get(final_url, headers=headers)
    # Convert to Python Dictionary
    data = response.json()

    # Number of Jobs found with query
    result_count = data['SearchResult']['SearchResultCount']
    print(result_count)
    
    # Print Position Titles for all Positions where the LocationName == state
    for i in range(result_count):
        if state in data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionLocation'][0]['LocationName']:
            #POSITION TITLE
            print(f"Position Title : {data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionTitle']}")

    # Converts JSON back into a string, so that the browser can render it
    json_formatted_string = json.dumps(data)
    print(type(json_formatted_string))
    return json_formatted_string

@jobs_api.route('/position/<string:position>', methods=['GET'])
def job_position_query(position):
    url = 'https://data.usajobs.gov/api/Search?'
    # TODO: If position has a white space, replace it with '%20'
    position_query = f'ResultsPerPage=500&PositionTitle={position}'
    final_url = url + position_query
    response = requests.get(final_url, headers=headers)
    
    # Convert to Python Dictionary
    data = response.json()

    # Number of Jobs found with query
    result_count = data['SearchResult']['SearchResultCount']
    print(result_count)

    # Print Position Titles for all Positions where the LocationName == state
    for i in range(result_count):
        #POSITION TITLE
        print(f"Position Title : {data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionTitle']}")

     # Converts JSON back into a string, so that the browser can render it
    json_formatted_string = json.dumps(data)
    print(type(json_formatted_string))
    return json_formatted_string

@jobs_api.route('/<string:state>/<string:position>', methods=['GET'])
def job_state_and_position_query(state = None, position = None):
    url = 'https://data.usajobs.gov/api/Search?'
    location_query = f'LocationName={state}'
    position_query = f'PositionTitle={position}'
    final_url = f'https://data.usajobs.gov/api/Search?ResultsPerPage=500&{location_query}&{position_query}'
    response = requests.get(final_url, headers=headers)
    # Convert to Python Dictionary
    data = response.json()

    # Number of Jobs found with query
    result_count = data['SearchResult']['SearchResultCount']
    print(result_count)

    # Print Position Titles for all Positions where the LocationName == state
    for i in range(result_count):
        if state in data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionLocation'][0]['LocationName']:
            print(f"Position Title : {data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionTitle']}")

    # Converts JSON back into a string, so that the browser can render it
    json_formatted_string = json.dumps(data)
    print(type(json_formatted_string))
    return json_formatted_string
