import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

def fetch_stock_data(ticker, start_date, end_date):
    #Fetch historical stock price data using yfinance.
    return yf.download(ticker, start=start_date, end=end_date)

def calculate_daily_returns(data):
    #Calculate daily returns.
    data['Daily_Return'] = data['Adj Close'].pct_change()
    return data

def visualize_daily_returns(data, name):
    #Visualize daily returns.
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Daily_Return'], mode='lines', name=name))
    fig.update_layout(title=f'Daily Returns for {name} (Last Quarter)', xaxis_title='Date', yaxis_title='Daily Return')
    fig.show()

def calculate_cumulative_returns(data):
    #Calculate cumulative returns.
    return (1 + data['Daily_Return']).cumprod() - 1

def visualize_cumulative_returns(data, name):
    #Visualize cumulative returns.
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data, mode='lines', name=name))
    fig.update_layout(title=f'Cumulative Returns for {name} (Last Quarter)', xaxis_title='Date', yaxis_title='Cumulative Return')
    fig.show()

def calculate_volatility(data):
    #Calculate historical volatility (standard deviation of daily returns).
    return data['Daily_Return'].std()

def visualize_volatility(names, volatilities):
    #Visualize volatility comparison.
    fig = go.Figure()
    fig.add_bar(x=names, y=volatilities, text=volatilities, textposition='auto')
    fig.update_layout(title='Volatility Comparison (Last Quarter)', xaxis_title='Stock', yaxis_title='Volatility (Standard Deviation)', bargap=0.5)
    fig.show()

def compare_statistics(mean_returns, std_returns):
    #Compare statistics (mean return, standard deviation).
    for name, mean_return, std_return in zip(mean_returns.index, mean_returns, std_returns):
        print(f"{name}:")
        print(f"Mean Daily Return: {mean_return:.6f}")
        print(f"Standard Deviation of Daily Return: {std_return:.6f}\n")

def calculate_correlation(data1, data2):
    #Calculate correlation between two datasets.
    return data1['Daily_Return'].corr(data2['Daily_Return'])

def calculate_beta(data, market_data):
    #Calculate beta value.
    cov = data['Daily_Return'].cov(market_data['Daily_Return'])
    var_market = market_data['Daily_Return'].var()
    return cov / var_market

def compare_beta_values(names, betas):
    #Compare beta values with the market.
    for name, beta in zip(names, betas):
        print(f"Beta for {name}: {beta:.6f}")

def main():
    try:
        # User input for stock tickers and date range
        stock_tickers = input("Enter stock tickers separated by comma (e.g., MSFT, NVDA): ").split(',')
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        # Fetch stock data
        stock_data = {}
        for code in stock_tickers:
            stock_data[code] = fetch_stock_data(code, start_date, end_date)

        # Calculate and visualize daily returns
        for code, data in stock_data.items():
            data = calculate_daily_returns(data)
            visualize_daily_returns(data, code)

        # Calculate and visualize cumulative returns
        for code, data in stock_data.items():
            cumulative_return = calculate_cumulative_returns(data)
            visualize_cumulative_returns(cumulative_return, code)

        # Calculate volatility
        volatilities = {code: calculate_volatility(data) for code, data in stock_data.items()}
        visualize_volatility(list(volatilities.keys()), list(volatilities.values()))

        # Calculate and compare statistics
        mean_returns = pd.Series({code: data['Daily_Return'].mean() for code, data in stock_data.items()})
        std_returns = pd.Series({code: data['Daily_Return'].std() for code, data in stock_data.items()})
        compare_statistics(mean_returns, std_returns)

        # Calculate correlation
        correlations = {}
        for code1, data1 in stock_data.items():
            for code2, data2 in stock_data.items():
                if code1 != code2:
                    correlation = calculate_correlation(data1, data2)
                    correlations[f"{code1}-{code2}"] = correlation
        print("Correlation between stocks:")
        for pair, corr in correlations.items():
            print(f"{pair}: {corr:.6f}")

        # Calculate beta values
        market_ticker = input("Enter market index ticker (e.g., ^GSPC for S&P 500): ")
        market_data = fetch_stock_data(market_ticker, start_date, end_date)
        market_data = calculate_daily_returns(market_data)
        betas = {code: calculate_beta(data, market_data) for code, data in stock_data.items()}
        compare_beta_values(list(betas.keys()), list(betas.values()))

    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()