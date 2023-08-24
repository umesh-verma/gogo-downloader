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
def search_anime(page=1):
    print('Enter Anime Name:')
    query = input()
    search_result = make_request('/search', params={'keyw': query, 'page': page})
    results = []
    for anime in search_result:
        results.append([anime['animeTitle'], anime['status'][-5::], anime['animeId']])
    return results
    
# get anime details by id
def get_anime_episodes(id): 
    anime_details = make_request('/anime-details/%s' %id)
    episodes = anime_details['episodesList']
    episodes = list(map(lambda episode: [episode['episodeNum'], episode['episodeId']], episodes))
    return episodes

# get streaming links by episode id
def get_streaming_links_vidcdn(id):
    return make_request('/vidcdn/watch/%s' %id)
    

def select_anime():
    page = 1
    results = search_anime(page)
    df =(DataFrame(results, columns=['Title', 'Status', 'AnimeId']))
    print(tabulate(df,showindex=True, headers=df.columns))
    selected_anime = int(input('select Anime:'))
    anime_id = results[selected_anime][2]
    return anime_id

def select_episode(anime):
    episodes = get_anime_episodes(anime)
    episodes = sorted(episodes, key=lambda episode: float(episode[0]))
    df =(DataFrame(episodes, columns=['Episode', 'EpisodeId']))
    print(tabulate(df,showindex=True, headers=df.columns))
    selected_episode = int(input('select Episode:'))
    episode_id = episodes[selected_episode-1][1]
    return episode_id

def get_streaming_link(episode):
    vid_cdn_link = get_streaming_links_vidcdn(episode)
    stream_link = vid_cdn_link['sources'][0]['file']
    return stream_link
           
# anime_details = get_anime(anime_id)
# anime_title = anime_details['animeTitle']
# print('Title: %s' %anime_title)

#lambda function to turn episodes into 2d list

# episodes = sorted(episodes, key=lambda episode: episode[0])



# for episode in episodes:
#     print('Episode  %s: %s'  %(episode['episodeNum'], episode['episodeId']))
# selected_episode = int(input('select Episode:'))
#get episode id from the list by selected episode

# episode_id = episodes[selected_episode-1]['episodeId']
# streaming_links = get_streaming_links_vidcdn(episode_id)
# stream_link = streaming_links['sources'][0]['file']
# Popen('mpv %s' %stream_link,  shell=False)
# print(stream_link)

def main():
    anime = select_anime()
    episode = select_episode(anime)
    streaming_link = get_streaming_link(episode)
    Popen('mpv %s' %streaming_link,  shell=False)
    

main()