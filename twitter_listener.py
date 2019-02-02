import os
import sys
import tweepy
import logging
from tweepy import StreamListener
import json
from datetime import datetime
import discord

logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=logging.INFO, stream=sys.stdout)


class TweetsListener(StreamListener):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    def on_data(self, data):
        resp = json.loads(data)
        subbed_channels = list()
        for ch in [460113527697309696, 396353984287342593]:  # TODO: make subbed channels list config dependant
            subbed_channels.append(self.bot.get_channel(ch))
        self.bot.loop.create_task(send_tweet(resp, subbed_channels))


async def send_tweet(resp, subbed_channels):
    if resp.get("created_at") \
            and not resp.get("retweeted_status") \
            and not resp.get("quoted_status") \
            and not resp.get("in_reply_to_status_id") \
            and not resp.get("in_reply_to_user_id"):
        print("Posted", resp)
        twitter_url = "https://twitter.com/"

        if resp.get("truncated"):
            text_range = resp.get("extended_tweet").get("display_text_range")
            tweet_text = resp.get("extended_tweet").get("full_text")[:text_range[1]]
        else:
            text_range = resp.get("display_text_range")
            tweet_text = resp.get("text")[:text_range[1]] if text_range else resp.get("text")
        user = resp.get("user")

        url = twitter_url + "{0}/status/{1}".format(user.get("screen_name"), resp.get("id_str"))
        embed = discord.Embed(title="Link to Tweet",
                              description=tweet_text,
                              timestamp=datetime.utcfromtimestamp(int(resp.get("timestamp_ms")) / 1000),
                              url=url)
        embed.set_author(name="@{screen_name}".format(**user),
                         url=twitter_url + user.get("screen_name"),
                         icon_url=user.get("profile_image_url_https"))
        embed.set_thumbnail(url=user.get("profile_image_url_https"))
        if resp.get("entities").get("media"):
            embed.set_image(url=resp.get("entities").get("media")[0].get("media_url_https"))
        for channel in subbed_channels:
            await channel.send(embed=embed)
        logging.info("Posted new tweet from {name} (@{screen_name})".format(**user))


def setup_twitter(bot):
    logging.info("Setting up Twitter Listener...")
    auth = tweepy.OAuthHandler(os.environ.get("TWITTER_API_KEY"), os.environ.get("TWITTER_API_SECRET"))
    auth.set_access_token(os.environ.get("TWITTER_TOKEN"), os.environ.get("TWITTER_TOKEN_SECRET"))
    api = tweepy.API(auth)
    stream = tweepy.Stream(auth=api.auth, listener=TweetsListener(bot))
    stream.filter(follow=["1549889018", "840052593690890240"], is_async=True)
