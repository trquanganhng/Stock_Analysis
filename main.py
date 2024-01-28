import pandas as pd
import yfinance as yf
import plotly.io as pio
import plotly.graph_objects as go

# Define the tickers for msft and nvda
msft_ticker = 'MSFT'
nvda_ticker = 'NVDA'

# Define the date range for the last quarter
start_date = '2023-10-01'
end_date = '2023-12-31'

# Fetch historical stock price data using yfinance
msft_data = yf.download(msft_ticker, start=start_date, end=end_date)
nvda_data = yf.download(nvda_ticker, start=start_date, end=end_date)

# Calculate daily returns
msft_data['Daily_Return'] = msft_data['Adj Close'].pct_change()
nvda_data['Daily_Return'] = nvda_data['Adj Close'].pct_change()

# Visualize Daily Returns
fig = go.Figure()

fig.add_trace(go.Scatter(x=msft_data.index, y=msft_data['Daily_Return'], mode='lines', name='Microsoft'))
fig.add_trace(go.Scatter(x=nvda_data.index, y=nvda_data['Daily_Return'], mode='lines', name='NVIDIA'))

fig.update_layout(title='Daily Returns for Microsoft and NVIDIA (Last Quarter)',
                  xaxis_title='Date', yaxis_title='Daily Return',
                  legend=dict(x=0.02, y=0.95))

fig.show()

# Compare Cumulative Returns
msft_cumulative_return = (1 + msft_data['Daily_Return']).cumprod() - 1
nvda_cumulative_return = (1 + nvda_data['Daily_Return']).cumprod() - 1

fig = go.Figure()

fig.add_trace(go.Scatter(x=msft_cumulative_return.index, y=msft_cumulative_return, mode='lines', name='Microsoft'))
fig.add_trace(go.Scatter(x=nvda_cumulative_return.index, y=nvda_cumulative_return, mode='lines', name='NVIDIA'))

fig.update_layout(title='Cumulative Returns for Microsoft and NVIDIA (Last Quarter)',
                  xaxis_title='Date', yaxis_title='Cumulative Return',
                  legend=dict(x=0.02, y=0.95))

fig.show()

# Calculate historical volatility (standard deviation of daily returns)
msft_volatility = msft_data['Daily_Return'].std()
nvda_volatility = nvda_data['Daily_Return'].std()

fig1 = go.Figure()
fig1.add_bar(x=['msft', 'nvda'], y=[msft_volatility, nvda_volatility],
             text=[f'{msft_volatility:.4f}', f'{nvda_volatility:.4f}'],
             textposition='auto', marker=dict(color=['blue', 'green']))

fig1.update_layout(title='Volatility Comparison (Last Quarter)',
                   xaxis_title='Stock', yaxis_title='Volatility (Standard Deviation)',
                   bargap=0.5)
fig1.show()

# Calculate and Compare Statistics
msft_mean_return = msft_data['Daily_Return'].mean()
msft_std_return = msft_data['Daily_Return'].std()
msft_sharpe_ratio = msft_mean_return / msft_std_return

nvda_mean_return = nvda_data['Daily_Return'].mean()
nvda_std_return = nvda_data['Daily_Return'].std()
nvda_sharpe_ratio = nvda_mean_return / nvda_std_return

print("Microsoft Mean Daily Return:", msft_mean_return)
print("Microsoft Standard Deviation of Daily Return:", msft_std_return)
print("Microsoft Sharpe Ratio:", msft_sharpe_ratio)

print("NVIDIA Mean Daily Return:", nvda_mean_return)
print("NVIDIA Standard Deviation of Daily Return:", nvda_std_return)
print("NVIDIA Sharpe Ratio:", nvda_sharpe_ratio)

# Correlation Analysis
correlation = msft_data['Daily_Return'].corr(nvda_data['Daily_Return'])
print("Correlation between Microsoft and NVIDIA:", correlation)

market_data = yf.download('^GSPC', start=start_date, end=end_date)

# Calculate daily returns for both stocks and the market
msft_data['Daily_Return'] = msft_data['Adj Close'].pct_change()
nvda_data['Daily_Return'] = nvda_data['Adj Close'].pct_change()
market_data['Daily_Return'] = market_data['Adj Close'].pct_change()

# Calculate Beta for msft and nvda
cov_msft = msft_data['Daily_Return'].cov(market_data['Daily_Return'])
var_market = market_data['Daily_Return'].var()

beta_msft = cov_msft / var_market

cov_nvda = nvda_data['Daily_Return'].cov(market_data['Daily_Return'])
beta_nvda = cov_nvda / var_market

# Compare Beta values
if beta_msft > beta_nvda:
    conclusion = "Microsoft is more volatile (higher Beta) compared to NVIDIA."
else:
    conclusion = "NVIDIA is more volatile (higher Beta) compared to Microsoft."

# Print the conclusion
print("Beta for Microsoft:", beta_msft)
print("Beta for NVIDIA:", beta_nvda)
print(conclusion)