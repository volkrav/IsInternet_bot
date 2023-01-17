import os
from dotenv import load_dotenv

load_dotenv()

urls = [url for url in os.environ.get('URLS').split(',') if url != '']
bot_token = os.environ.get('TOKEN')
chat_id = os.environ.get('CHAT_ID')
port = os.environ.get('PORT')
port = os.environ.get('PORT')

API_link = f'https://api.telegram.org/bot' + '5522301142:AAFpmTT9UiFrqcYibr1F7Mied5CTIRqBWF0'

PING = True
