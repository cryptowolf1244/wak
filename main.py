from binance.client import Client
import matplotlib.pyplot as plt
import Functions
import datetime
import pprint

apiKey = 'gcJLtOs6tZYTOBEyIYY0JZBDagmFMkc5SY5T8R792cCUgBn7YCLfG7pOJZG3J36x '
secretKey = 'EYyaqoqRyPxozdDQQmlL7xQiHaqDIxgGAav68UoYAznTAOI6darEG132kavhI3Vh'
client = Client(apiKey, secretKey)

klinesStartDate = datetime.datetime(2021,1,31)
klinesEndDate = datetime.datetime(2022,3,12)

market1 = Functions.get_historical_candles(
    client, 
    "BTCUSDT", 
    "5m", 
    start_time = klinesStartDate.strftime("%d %b,%Y"),
    market = "futures"
)

market2 = Functions.get_historical_candles(
    client, 
    "BTCBUSD", 
    "5m", 
    start_time = klinesStartDate.strftime("%d %b,%Y"),
    market = "futures"
)

((market1["High"]-market2["High"])/market1["High"]*100).plot()
((market1["Low"]-market2["Low"])/market1["Low"]*100).plot()
plt.show()
