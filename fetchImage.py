import random
import os
from io import BytesIO

from PIL import Image

import praw
import requests
import sys
from dotenv import load_dotenv

load_dotenv()
# Grabs 200 hot posts from a random subreddit in the list below.
# Picks a random post and uses that image.
def fetchImage(filepath="memes/", return_in_memory=False):
    client_id = os.environ['praw_client_id']
    client_secret = os.environ['praw_client_secret']
    user_agent = os.environ['USER_AGENT']
    refresh_token = os.environ['REFRESH_TOKEN']

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
        user_agent=user_agent,
    )

    subreddit_list = [
        "MEOW_IRL",
        "memes",
        "dankmemes"
        "superbowl"
        "popular",
        "AdviceAnimals",
        "ComedyCemetery",
        "terriblefacebookmemes",
        "funny",
    ]

    chosen_subreddit = random.choice(subreddit_list)

    # Specify the subreddit and the number of posts to fetch
    subreddit = reddit.subreddit(chosen_subreddit)
    num_posts_to_fetch = 45
    posts_with_images = []

    # Fetch the posts from the subreddit
    posts = subreddit.new(limit=num_posts_to_fetch)
    # Iterate over the posts
    for post in posts:
        if post.url.endswith(('.jpg', '.jpeg', '.png')):
            posts_with_images.append(post)

    post_to_fetch = random.choice(posts_with_images)
    response = requests.get(post_to_fetch.url)
    if response.status_code == 200:
        if return_in_memory:
            img = Image.open(BytesIO(response.content), 'r')
            return img
        # Extract the file extension from the URL
        file_extension = post_to_fetch.url.split('.')[-1]
        print(post_to_fetch.url)
        filename = post_to_fetch.url[18:].replace("/", "").split(".")[0]
        # Save the image to disk
        whole_filepath = f'{filepath}/{chosen_subreddit}-{filename}.{file_extension}'
        with open(whole_filepath, 'wb') as f:
            f.write(response.content)
        print('Image saved successfully!')
    return whole_filepath


if __name__ == '__main__':
    if (len(sys.argv) <= 1):
        print("Add a filepath argument to save images")
        exit(1)
    fileLoc = sys.argv[1]

    fetchImage(fileLoc)