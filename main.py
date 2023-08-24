#make request to the api and return the response
##TODO : remove pytz, tzdata, six, numpy, python-dateutil,tabulate pandas from requirements.txt
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
def search(query,page=1):
    return make_request('/search', params={'keyw': query, 'page': page})
# get anime details by id
get_anime =lambda id: make_request('/anime-details/%s' %id)

# get streaming links by episode id
get_streaming_links_vidcdn = lambda id: make_request('/vidcdn/watch/%s' %id)


print('Enter Anime Name:')

search_result = search(input())
results = []
for anime in search_result:
    results.append([anime['animeTitle'], anime['status'][-5::]])

df =(DataFrame(results, columns=['Title', 'Status']))
print(tabulate(df,showindex=True, headers=df.columns))
selected_anime = int(input('select Anime:'))



anime_id = search_result[selected_anime]['animeId']
anime_details = get_anime(anime_id)
anime_title = anime_details['animeTitle']
episodes = anime_details['episodesList']
print('Title: %s' %anime_title)
for episode in episodes:
    print('Episode  %s: %s'  %(episode['episodeNum'], episode['episodeId']))
selected_episode = int(input('select Episode:'))
episode_id = episodes[selected_episode-1]['episodeId']
streaming_links = get_streaming_links_vidcdn(episode_id)
stream_link = streaming_links['sources'][0]['file']
Popen('mpv %s' %stream_link,  shell=False)
print(stream_link)
