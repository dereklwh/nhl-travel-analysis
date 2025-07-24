import numpy as np
import pandas as pd
import requests

# use requests to get nhl api data
def get_nhl_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # print(data)
        return 'Sucess!'
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
def main():
    base_url = 'https://api-web.nhle.com/v1/'
    end_point = 'roster/VAN/current'
    test_url = base_url + end_point

    print(get_nhl_data(test_url))

if __name__ == '__main__':
    main()
