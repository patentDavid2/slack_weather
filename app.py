from weather_info_parser import WeatherInfoParser
from slack_sdk.rtm_v2 import RTMClient
from slack_sdk import WebClient
from dotenv import load_dotenv
import os


load_dotenv()


# 채팅의 마지막 두 글자가 날씨로 끝나는지 확인
# httpx 모듈을 사용해서 네이버에 채팅글을 검색
# 요청에 대한 응답에서 필요한 데이터를 추출
# 추출한 데이터를 슬랙에 표시


rtm = RTMClient(token=os.getenv('slack_token'))
web_client = WebClient(token=os.getenv('slack_token'))
weather_info_parser = WeatherInfoParser()

@rtm.on("message")
def handle(client: RTMClient, event: dict):
    keyword: str = event['text']
    if keyword.endswith('날씨'):
        weather_info = weather_info_parser.getWeatherInfo(keyword=keyword)

        channel_id = event['channel']

        client.web_client.chat_postMessage(
            channel=channel_id,
            blocks=[
                {'type':'divider'},
                {
                    'type':'section',
                    'text': {
                        'type':'plain_text',
                        'text':f'{weather_info.area}'
                    }
                },
                {'type':'divider'},
                {
                    'type':'section',
                    'text':{
                        'type':'plain_text',
                        'text':f"""{weather_info.weather_today}
현재기온:{weather_info.temperature_now}
최고기온:{weather_info.temperature_high}
최저기온:{weather_info.temperature_low}
"""
                    }
                },
            ],
        )

        weather_info_parser.getScreenshot(keyword=keyword)

        web_client.files_upload_v2(
            channel=channel_id,
            file='info.png',
            title='날씨 정보',
        )

rtm.start()