from bs4 import BeautifulSoup
import os
import json
import requests

class Scraper():
    def __init__(self) -> None:
        self.hashtags = []
        self.profiles = []
        self.get_hashtags()  


    def get_hashtags(self):
            url = 'https://trends24.in/united-states/'
            self.parse_hashtags(url)
            
   
    def parse_hashtags(self, url: str) -> None:
        # retrieve twitter trending hashtags
        HEADERS = ({'User-Agent':
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                    'Accept-Language': 'en-US, en;q=0.5'})
        
        webpage = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")

        hashtags_set = soup.find_all('ol', class_="trend-card__list")[1]
        hashtags_set = hashtags_set.find_all('a', href=True)

        # parse href from a tag
        for a in hashtags_set:
            self.hashtags.append(a.contents[0])


    def collect_profiles(self, number_of_profiles: int = 50) -> None:
        hashtag = self.hashtags[0]

        # find profiles using trending hashtags
        for hashtag in self.hashtags:
            os.system(f'snscrape --jsonl --max-results 50 twitter-hashtag "{hashtag}" > text-query-tweets.json')
            
            if len(self.profiles) < number_of_profiles:
                with open('text-query-tweets.json', 'r') as f:
                    
                    try:
                        # json contains multiple dicts, so read them individually to avoid trouble
                        for line in f.readlines():
                            prof_data = json.loads(line)
                            prof_data = prof_data['user']

                            followers_count = prof_data['followersCount']
                            is_protected = prof_data['protected']

                            # append profile to our influencers list
                            if followers_count > 1000 and is_protected == False:
                                prof_info = {'username': prof_data['username'],
                                    'displayed_name': prof_data['displayname'],
                                    'description': prof_data['description'],
                                    'followers': prof_data['followersCount'],
                                    'following': prof_data['friendsCount'],
                                    'posts_count': prof_data['statusesCount'],
                                    'birthday': None,
                                    'joined_twitter': prof_data['created'],
                                    'website': prof_data['linkUrl']}
                                
                                # Check if profile has already been added
                                if len(self.profiles) > 0:
                                    status = True
                                    for profile in self.profiles:
                                        # if username has already been added, change status to false
                                        if profile['username'] == prof_info['username']:
                                            status = False
                                    if status == True:
                                        self.profiles.append(prof_info)
                                else:
                                    # append profile
                                    self.profiles.append(prof_info)
                                
                                # we want only 50 profiles, so break loop
                                if len(self.profiles) == number_of_profiles:
                                    break
                                
                    except KeyError:
                        continue
            else:
                break

    
    def get_profiles_posts(self, username: str, number_posts: int = 50) -> 'list[dict]':
        posts = []
        os.system(f'snscrape --jsonl --max-results {number_posts * 5} twitter-user {username} > posts.json')

        with open('posts.json', 'r') as f:
            # get every post data
            for line in f.readlines():
                if len(posts) < number_posts:
                    post_raw_data = json.loads(line)

                    # check if post is a retweet of a reply
                    if post_raw_data['retweetedTweet'] == None and post_raw_data['inReplyToTweetId'] == None:
                        posts.append({'favorites': post_raw_data['likeCount'],
                            'retweets': post_raw_data['retweetCount'],
                            'replies': post_raw_data['replyCount'],
                            'date': post_raw_data['date']})
                    else:
                        continue
                else:
                    break
        return posts


    def store_profiles(self) -> None:
        self.database.insert_many_profiles(self.profiles)
