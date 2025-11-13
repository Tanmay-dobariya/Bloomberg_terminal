from requests import get
from datetime import date,timedelta
from twilio.rest import Client
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def load_env_or_raise(name:str):
  value = getenv(name)

  if not value:
    raise ValueError(f"{name} env var is not available")

  return value

STOCK_NAME = load_env_or_raise("STOCK_NAME")
COMPANY_NAME = load_env_or_raise("COMPANY_NAME")

STOCKS_API_KEY = load_env_or_raise("STOCKS_API_KEY")
NEWS_API_KEY = load_env_or_raise("NEWS_API_KEY")

STOCK_ENDPOINT = load_env_or_raise("STOCK_ENDPOINT")
NEWS_ENDPOINT = load_env_or_raise("NEWS_ENDPOINT")

ACCOUNT_SID = load_env_or_raise("ACCOUNT_SID")
TWILIO_AUTH_TOKEN = load_env_or_raise("TWILIO_AUTH_TOKEN")
FROM = load_env_or_raise("FROM")
TO = load_env_or_raise("TO")

if not all([STOCK_NAME, COMPANY_NAME, STOCKS_API_KEY, NEWS_API_KEY, STOCK_ENDPOINT, NEWS_ENDPOINT, ACCOUNT_SID, TWILIO_AUTH_TOKEN, FROM, TO]):
  raise ValueError("Missing one or more required environment variables")

stock_endpoint_params = {
  "function" : "TIME_SERIES_DAILY",
  "symbol" : STOCK_NAME,
  "apikey" : STOCKS_API_KEY
}

stocks_response = get(url=STOCK_ENDPOINT, params=stock_endpoint_params)
got_noticeable_difference = False

if stocks_response.status_code == 200:
  response = stocks_response.json()

  today = date.today()
  yesterday = str(today - timedelta(days=1))
  day_before_yesterday = str(today - timedelta(days=2))

  try:
    key_of_data = 'Time Series (Daily)'
    yesterday_data = response[key_of_data][yesterday]
    day_before_yesterday_data = response[key_of_data][day_before_yesterday]
  except KeyError as ke:
    raise ke

  try:
    key_of_price = '4. close'
    yesterday_price = int(float(yesterday_data[key_of_price]))
    day_before_yesterday_price = int(float(day_before_yesterday_data[key_of_price]))
  except KeyError as ke:
    raise ke
  
  positive_difference = yesterday_price - day_before_yesterday_price
  percentage_difference = int(float(positive_difference/day_before_yesterday_price * 100))

  got_noticeable_difference = True if percentage_difference >= 3 or percentage_difference <= -3 else False

else:
  stocks_response.raise_for_status()

news_endpoint_params = {
  "q": COMPANY_NAME,
  "pageSize": 3,
  "apiKey": NEWS_API_KEY
}

news_articles = []
if got_noticeable_difference:
  news_response = get(url=NEWS_ENDPOINT, params=news_endpoint_params)
  
  if news_response.status_code == 200:
    response = news_response.json()
    
    try:
      key_of_articles = 'articles'
      news_articles = response[key_of_articles]
    except KeyError as ke:
      raise ke
  else:
    news_response.raise_for_status()

try: 
  news_data_to_send = [{"headline": item['title'], "description": item['description']} for item in news_articles]
except KeyError as ke:
  raise ke

client = Client(ACCOUNT_SID, TWILIO_AUTH_TOKEN)

for news in news_data_to_send:
  message= client.messages.create(
    body=f"""
    Headline: {news['headline']}
    Description: {news['description']}
    """,
    from_= FROM,
    to= TO
)

