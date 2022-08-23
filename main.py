import requests
from twilio.rest import Client

STOCK_NAME = "META"
COMPANY_NAME = "Meta Platforms, Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

news_api = "NEWS_API"
alpha_api = "ALPHAVANTAGE_API"

TWILIO_SID = "TWILIO_SID"
TWILIO_AUTH_TOKEN = "TWILIO_AUTH_TOKEN"


stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey" : alpha_api
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status
data = response.json()


data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_close = yesterday_data["4. close"]


#get yesterday and day before yesterday's closing price
day_before_yesterday_data = data_list[1]
day_before_yesterday_close = day_before_yesterday_data["4. close"]


difference = abs(float(yesterday_close) - float(day_before_yesterday_close))


diff_percent = (difference / float(yesterday_close)) * 100
print(diff_percent)

# get news from if there's 2% increase
if diff_percent > 2:
    news_params = {
        "apiKey" : news_api,
        "qInTitle": STOCK_NAME,
    }


    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    
    three_articles = articles[:3]
    print(three_articles)

    #get first 3 article using list comprehension
    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article ['description']}" for article in three_articles] 

    # sends three article seperately
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    
    for article in formatted_articles:

        message = client.messages.create(
                body=formatted_articles,
                from_="TWILIO_PHONE_NUMBER",
                to='YOUR_PHONE_NUMBER'
            )

    print(message.sid)
