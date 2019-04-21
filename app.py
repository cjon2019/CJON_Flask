
import requests

headers = {
    'Host': 'data.usajobs.gov',
    'User-Agent': 'nicholas.coxe@gmail.com',
    'Authorization-Key': 'wN/n6HZljpJ4go21Ct/KB+RCGj1KtIKG3mQSKCZGPe4='
}

location_query = 'LocationName=Indiana'
position_query = 'PositionTitle=It%20Software%20Developer'
# response = requests.get(f'https://data.usajobs.gov/api/Search?{position_query}', headers=headers)
response = requests.get(
    f'https://data.usajobs.gov/api/Search?{location_query}&{position_query}', headers=headers)
data = response.json()

result_count = data['SearchResult']['SearchResultCount']
print(result_count)
location = data['SearchResult']['SearchResultItems'][0]['MatchedObjectDescriptor']['PositionLocation'][0]['LocationName']
job_title = data['SearchResult']['SearchResultItems'][0]['MatchedObjectDescriptor']['PositionTitle']

state = 'Indiana'


def print_all_json_data():
    for i in range(result_count):
        if state in data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionLocation'][0]['LocationName']:
            # POSITION TITLE
            print(
                f"Position Title : {data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionTitle']}")
            # LOCATIONS
            print(
                f"Location : {data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionLocation'][0]['LocationName']}")
            # START DATES
            print(
                f"Start Date : {data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionStartDate']}")
            # END DATES
            print(
                f"End Date : {data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionEndDate']}")
            # JOB SUMMARY
            print(
                f"Job Summary : {data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['UserArea']['Details']['JobSummary']}")
            # TOTAL OPENINGS
            try:
                print(
                    f"Total Openings : {data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['UserArea']['Details']['TotalOpenings']}")
            except:
                print(f"Total Openings : Nothing to display.")
            # Minimum SALARY
            try:
                print(
                    f"Minimum Salary : {data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionRemuneration'][0]['MinimumRange']}")
            except:
                print(f"Salary Info : Nothing to display.")
            # MAX SALARY
            try:
                print(
                    f"Maximum Salary : {data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionRemuneration'][0]['MaximumRange']}")
            except:
                print(f"Salary Info : Nothing to display.")
            # Rate
            try:
                print(
                    f"Rate : {data['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']['PositionRemuneration'][0]['RateIntervalCode']}")
            except:
                print(f"Salary Info : Nothing to display.")


print_all_json_data()
