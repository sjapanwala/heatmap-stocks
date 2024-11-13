# -----------------------------------------
# Author: Saaim Japanwala
# Date: 11/13/2024
# -----------------------------------------


import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
import numpy as np

tickers = ['AAPL', 'GOOGL', 'AMZN', 'TSLA', 'MSFT', 'NVDA', 'META', 'NFLX', 'BA', 'V', 'JPM', 'DIS', 'BAC', 'KO']

data = yf.download(tickers, period='5d')['Adj Close']

if data.shape[0] >= 2:
    data_pct_change = ((data.iloc[-1] - data.iloc[-2]) / data.iloc[-2]) * 100
    columns_per_row = 5
    num_rows = math.ceil(len(data_pct_change) / columns_per_row)
    padded_data = np.append(data_pct_change.values, [np.nan] * (num_rows * columns_per_row - len(data_pct_change)))
    reshaped_data = padded_data.reshape(num_rows, columns_per_row)

    reshaped_df = pd.DataFrame(reshaped_data, columns=[tickers[i] if i < len(tickers) else '' for i in range(columns_per_row)])
    annotations = np.array([[f"{tickers[i]}\n{reshaped_data[row, col]:.2f}%" if not np.isnan(reshaped_data[row, col]) else ""
                             for col, i in enumerate(range(row * columns_per_row, (row + 1) * columns_per_row))]
                            for row in range(num_rows)])
    cmap = sns.diverging_palette(10, 240, as_cmap=True)
    plt.figure(figsize=(8, num_rows * 2))
    sns.heatmap(reshaped_df, annot=annotations, fmt="", cmap=cmap, center=0, cbar_kws={'label': 'Daily % Change'},
                xticklabels=False, yticklabels=False)
    plt.title("Stock Heatmap")
    plt.show()
else:
    print("Not enough data to calculate daily percentage change.")

