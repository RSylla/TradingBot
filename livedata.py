import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt

API_KEY = None
SYMBOL = "TSLA"
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={SYMBOL}&interval=60min&outputsize=full&apikey={API_KEY}&datatype=csv"
df = pd.read_csv(url)

date = df["timestamp"]
open = df["open"]
close = df["close"]
high = df["high"]
low = df["low"]
volume = df["volume"]
kc = ta.kc(high, low, close, 10)

plt.plot(date, kc)
plt.show()

