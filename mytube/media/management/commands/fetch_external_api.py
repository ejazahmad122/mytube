import os
from django.core.management.base import BaseCommand
import requests
from account.models import User
from media.models import Video


class Command(BaseCommand):
    help = "add videos from youtube api to local data base"

    def handle(self, *args, **options):
        """This handle function add videos from external api into local data base
        """
        try:

            url = "https://youtube138.p.rapidapi.com/search/"

            querystring = {"q": "mobile", "hl": "en", "gl": "US"}

            headers = {
                "X-RapidAPI-Key": str(os.getenv('X_RapidAPI_Key')),
                "X-RapidAPI-Host": str(os.getenv('X_RapidAPI_Host'))
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring
            ).json()

            user = User.objects.get(email='admin@gmail.com')
            for item in response['contents']:
                video_id = item['video']['videoId']
                title = item['video']['title']
                description = item['video']['descriptionSnippet']
                video_url = f'https://youtu.be/{video_id}'
                thumbnail = item['video']['thumbnails'][0]['url']
                keywords = item['video']['title']
                channel_name = item['video']['author']['title']

                response = Video.objects.create(title=title, description=description,
                                                video_url=video_url, thumbnail=thumbnail, keywords=keywords, user_id=user, channel_name=channel_name)
        except:
            print("something went wrong while adding videos from external api !!")
