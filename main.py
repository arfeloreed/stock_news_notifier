import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla"
PARAMS_STOCK = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": "your_api key from alphavantage",
}
PARAMS_NEWS = {
    "q": COMPANY_NAME,
    "sortBy": "publishedAt",
    "apiKey": "your api_key from newsapi",
    "language": "en",
}
ACCOUNT_SID = "your account sid from twilio"
AUTH_TOKEN = "your auth token from twilio"
MY_TWILIO_NO = "your mobile number from twilio"

client = Client(ACCOUNT_SID, AUTH_TOKEN)

response = requests.get(url="https://www.alphavantage.co/query", params=PARAMS_STOCK)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
closed_list = [data[datum]["4. close"] for datum in data]
two_days_closed_priced = closed_list[:2]

percentage = round((float(two_days_closed_priced[0]) - float(two_days_closed_priced[1]))
                   / float(two_days_closed_priced[0]) * 100)

up_down = None
if percentage < 0:
    up_down = "Down"
else:
    up_down = "Up"

if abs(percentage) >= 3:
    news_response = requests.get(url=f"https://newsapi.org/v2/everything", params=PARAMS_NEWS)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"][:3]
    source = [news_data[num]["source"]["name"] for num in range(len(news_data))]
    headlines = [news_data[num]["title"] for num in range(len(news_data))]
    message = client.messages.create(
        body=f"{STOCK}: {up_down}{percentage}%\n\nSource: {source[0]}\nBrief: {headlines[0]}\n\n"
             f"Source: {source[1]}\nBrief: {headlines[1]}\n\nSource: {source[2]}\nBrief: {headlines[2]}",
        from_=MY_TWILIO_NO,
        to="number you'll send the message to",
    )
    print(message.status)
