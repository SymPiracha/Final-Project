import requests
import json
import datetime
import argparse
import os.path as osp

parser = argparse.ArgumentParser(description="Final Project")
parser.add_argument('subreddit', type=str, help='Name of subreddit')

args = parser.parse_args()

def get_posts(sub):
    posts = []
    data = requests.get(f'http://api.reddit.com/r/{sub}/top?limit=100', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15: requests (by u/PristineFactor3'})
    posts.append(data.json()['data']['children'])
    try:
        after = data.json()['data']["children"][-1]["data"]['name']
        for i in range(6):
            data = requests.get(f'http://api.reddit.com/r/{sub}/top?limit=100&after={after}', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15: requests (by u/PristineFactor3'})
            posts.append(data.json()['data']['children'])
            after = data.json()['data']["children"][-1]["data"]['name']

    except IndexError:
        return posts
    return posts

def main():
    date = datetime.datetime.now().strftime('%Y%m%d')
    f1 = open(osp.abspath(osp.join('data', f'final_{args.subreddit}', f'{date}_{args.subreddit}.json')), 'w')
    posts = get_posts(args.subreddit)
    counter = 0
    added_posts = []
    for dic in posts:
        for post in dic: 
            if post["data"]["name"] not in added_posts: 
                json.dump(post['data'], f1)
                f1.write("\n")
                added_posts.append(post["data"]["name"])
                if len(added_posts) == 333:
                    break
        if len(added_posts) == 333:
            break
    f1.close()
    
if __name__ == "__main__":
    main()
