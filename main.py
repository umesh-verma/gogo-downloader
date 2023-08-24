#make request to the api and return the response
##TODO : remove pytz, tzdata, six, numpy, python-dateutil,tabulate pandas from requirements.txt
##TODO : fix the episode list/selection function

import json
import requests
import os
from dotenv import load_dotenv
from pandas import DataFrame
from tabulate import tabulate
from subprocess import Popen


load_dotenv()
base_uri = os.getenv('BASE_URI')

# make request to the api and return the response as json
def make_request(path, params=None):
    url = base_uri + path
    headers = {'Content-Type': 'application/json'}
    response = requests.request("GET", url, headers=headers, params=params)
    return response.json()
# search for anime
def search_anime(query,page=1):
    print('Enter Anime Name:')
    query = input()
    search_result = make_request('/search', params={'keyw': query, 'page': page})
    results = []
    for anime in search_result:
        results.append([anime['animeTitle'], anime['status'][-5::]])
    return results
    
# get anime details by id
get_anime =lambda id: make_request('/anime-details/%s' %id)

# get streaming links by episode id
get_streaming_links_vidcdn = lambda id: make_request('/vidcdn/watch/%s' %id)

def select_anime(query, page=1):
    anime_id = search_result[selected_anime]['animeId']       
anime_details = get_anime(anime_id)
anime_title = anime_details['animeTitle']
print('Title: %s' %anime_title)
episodes = anime_details['episodesList']
#lambda function to turn episodes into 2d list
episodes = list(map(lambda episode: [episode['episodeNum'], episode['episodeId']], episodes))
episodes = sorted(episodes, key=lambda episode: episode[0])
df =(DataFrame(episodes, columns=['Episode', 'EpisodeId']))
print(tabulate(df,showindex=True, headers=df.columns))


# for episode in episodes:
#     print('Episode  %s: %s'  %(episode['episodeNum'], episode['episodeId']))
selected_episode = int(input('select Episode:'))
#get episode id from the list by selected episode

episode_id = episodes[selected_episode-1]['episodeId']
streaming_links = get_streaming_links_vidcdn(episode_id)
stream_link = streaming_links['sources'][0]['file']
Popen('mpv %s' %stream_link,  shell=False)
print(stream_link)

def main():
    anime = select_anime()

    print('Enter Anime Name:')

    search_result = search(input())
    

    df =(DataFrame(results, columns=['Title', 'Status']))
    print(tabulate(df,showindex=True, headers=df.columns))
    selected_anime = int(input('select Anime:'))

if main == '__main__':
    main()