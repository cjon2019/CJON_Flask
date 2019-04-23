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
    final_url = f'https://data.usajobs.gov/api/Search?ResultsPerPage=1000&{location_query}&{position_query}'
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
    location_query = f'ResultsPerPage=1000&LocationName={state}'
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
    position_query = f'ResultsPerPage=1000&PositionTitle={position}'
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
    final_url = f'https://data.usajobs.gov/api/Search?ResultsPerPage=1000&{location_query}&{position_query}'
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

@jobs_api.route('/test',methods=['GET'])
def test():
    final_url = 'https://data.usajobs.gov/api/Search?ResultsPerPage=1000&LocationName=Indiana&PositionTitle=IT'
    response = requests.get(final_url, headers=headers)
    # Convert to Python Dictionary
    data = response.json()

    # Number of Jobs found with query
    result_count = data['SearchResult']['SearchResultCount']
    print('Result Count:' + str(result_count))
    # Creating a List, or Dictionaries
    my_list = [{
        'matched_object_id': 0,
        'position_title' : 'Test Position',
        'job_summary': 'Test Summary',
        'position_location' : 'Test Location',
        'position_start_date' : '01/01/2019',
        'position_end_date' : '12/31/2019',
        'min_range': 0,
        'max_range': 100,
        'rate_interval_code': 'Per Year'
    }]
    state = 'Indiana'
    for i in range(result_count):
        if state in data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionLocation'][0]['LocationName']:
            matched_object_id = data['SearchResult']['SearchResultItems'][i]['MatchedObjectId']
            position_title = data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionTitle']
            job_summary = data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['UserArea']['Details']['JobSummary']
            position_location = data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionLocation'][0]['LocationName']
            position_start_date = data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionStartDate']
            position_end_date = data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionEndDate']
            min_range = 0
            try:
                min_range = data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionRemuneration'][0]['MinimumRange']
            except:
                min_range = 0
                print('No Min Salary data')
            
            max_range = 0
            try:
               max_range = data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionRemuneration'][0]['MaximumRange']
            except:
                max_range = 0
                print('No Max Salary data')
            rate_interval_code = 'NA'
            try:
                rate_interval_code = data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionRemuneration'][0]['RateIntervalCode']
            except:
                print('No Rate of Interval data')
            my_list.append({
                'matched_object_id': matched_object_id,
                'position_title': position_title,
                'job_summary': job_summary,
                'position_location' : position_location,
                'position_start_date' : position_start_date,
                'position_end_date' : position_end_date,
                'min_range': min_range,
                'max_range': max_range,
                'rate_interval_code': rate_interval_code
            })


    print(my_list[1])
    # Converts JSON back into a string, so that the browser can render it
    # json_formatted_string = json.dumps(data)  # data contains all JSON data of the job posting
    json_formatted_string = json.dumps(my_list) # my_list contains only the JSON data that we care about
    print(type(json_formatted_string))          # type == str
    return json_formatted_string