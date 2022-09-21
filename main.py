import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "E6ETHC5TH0QNYXOU"
STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}
# GET STOCK DATA
stock_data = requests.get(STOCK_ENDPOINT, STOCK_PARAMS)
stock_data.raise_for_status()
stock_data_dict = stock_data.json()["Time Series (Daily)"]

# GET PAST 2 DAYS
count = 0
for i in stock_data_dict.keys():
    count += 1
    if count > 2:
        break
    elif count == 1:
        key1 = i
    elif count == 2:
        key2 = i

# GET YESTERDAY AND DAY BEFORE CLOSING PRICE
day_1_close = float(stock_data_dict[key1]["4. close"])
day_2_close = float(stock_data_dict[key2]["4. close"])

# GET FIVE PERCENT OF DAY BEFORE YESTERDAY
five_perc = (5/100) * (day_2_close)

# CHECK PERCENTAGE CHANGE
stock_changed = False
if day_1_close - day_2_close >= five_perc:
    stock_changed = True
    change = (day_1_close - day_2_close) / 100 * day_2_close
    symbol = "🔺"
elif day_2_close - day_1_close >= five_perc:
    stock_changed = True
    change = (day_2_close - day_1_close) / 100 * day_1_close
    symbol = "🔻"

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
# FROM KEY1
NEWS_API_KEY = "9b13e797e7e345f08e0d38ad0674c8ff"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_PARAMS = {
    "q": COMPANY_NAME,
    "from": key1,
    "sortBy": "publishedAt",
    "apikey": NEWS_API_KEY
}

# GET NEWS DATA
news_data = requests.get(NEWS_ENDPOINT, params=NEWS_PARAMS)
news_data.raise_for_status()
article_list = news_data.json()["articles"]


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

# TWILIO SETUP
twilio_sid = "ACcfe7faae480aa9f01c0980a1c64b0a61"
auth_token = "2b38c9ba9b43177657fd9f942a02728f"
twilio_phone_number = "+12564809013"
my_number = "+19732622841"
client = Client(twilio_sid, auth_token)
try:
    if stock_changed:
        message = client.messages \
                    .create(
            body=f"{STOCK}: {symbol}{change}%\n\n"
                 f"Headline: {article_list[0]['title']}\n\n"
                 f"Brief: {article_list[0]['content']}\n\n"
                 f"Headline: {article_list[1]['title']}\n\n"
                 f"Brief: {article_list[1]['content']}\n\n"
                 f"Headline: {article_list[2]['title']}\n\n"
                 f"Brief: {article_list[2]['content']}\n\n",
            from_=twilio_phone_number,
            to=my_number
        )
except NameError:
    print(message.sid)
    print(message.status)


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

