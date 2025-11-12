from re import S
from requests import get
from datetime import date,timedelta

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = "T9FUJGTN5VH2EMUZ"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
params = {
  "function" : "TIME_SERIES_DAILY",
  "symbol" : STOCK_NAME,
  "apikey" : API_KEY
}

stocks_response = get(url=STOCK_ENDPOINT, params=params)

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
  
  yesterday_price = int(float(yesterday_data['4. close']))
  day_before_yesterday_price = int(float(day_before_yesterday_data['4. close']))

  positive_difference = abs(yesterday_price - day_before_yesterday_price)
  percentage_difference = int(float(positive_difference/day_before_yesterday_price * 100))
else:
  stocks_response.raise_for_status()

## STEP 2: https://newsapi.org/ 
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation


## STEP 3: Use twilio.com/docs/sms/quickstart/python
#to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

#TODO 9. - Send each article as a separate message via Twilio. 



#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

