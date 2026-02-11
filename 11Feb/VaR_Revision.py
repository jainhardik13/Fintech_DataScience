# Assignment to code using python Calculate VaR for 2 Stocks portfolio and compare all all 3 methods Historical VaR, Parametric VaR, Monte Carlo VaR

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime, timedelta

# Configuration
STOCKS = ['AAPL', 'MSFT']  # Two stocks for portfolio
WEIGHTS = [0.5, 0.5]  # Equal weights
INITIAL_INVESTMENT = 1000000  # $1 million portfolio
CONFIDENCE_LEVEL = 0.95  # 95% confidence level
HOLDING_PERIOD = 1  # 1 day holding period
START_DATE = '2023-01-01'
END_DATE = '2025-02-10'  # Adjusted to valid historical date
MONTE_CARLO_SIMULATIONS = 10000

print("="*70)
print("Value at Risk (VaR) Analysis for 2-Stock Portfolio")
print("="*70)
print(f"\nPortfolio Details:")
print(f"Stocks: {STOCKS}")
print(f"Weights: {WEIGHTS}")
print(f"Initial Investment: ${INITIAL_INVESTMENT:,.2f}")
print(f"Confidence Level: {CONFIDENCE_LEVEL*100}%")
print(f"Holding Period: {HOLDING_PERIOD} day(s)")
print(f"Data Period: {START_DATE} to {END_DATE}")
print("="*70)

# Step 1: Download historical stock data
print("\n[Step 1] Downloading historical stock price data...")

try:
    # Download stocks individually for better reliability
    stock_data = {}
    for stock in STOCKS:
        try:
            print(f"  Downloading {stock}...")
            temp_data = yf.download(stock, start=START_DATE, end=END_DATE, progress=False)
            if not temp_data.empty:
                if 'Adj Close' in temp_data.columns:
                    stock_data[stock] = temp_data['Adj Close']
                elif 'Close' in temp_data.columns:
                    stock_data[stock] = temp_data['Close']
                else:
                    stock_data[stock] = temp_data.iloc[:, 0]
                print(f"  ✓ {stock}: {len(stock_data[stock])} days downloaded")
        except Exception as e:
            print(f"  ✗ Failed to download {stock}: {e}")

    if len(stock_data) >= len(STOCKS):
        data = pd.DataFrame(stock_data)
        data = data.dropna()  # Remove any rows with NaN values
        print(f"\n✓ Successfully downloaded data for all {len(STOCKS)} stocks")
        print(f"Total: {len(data)} days of historical data")
        print(f"\nLatest Prices:")
        print(data.tail())
    elif len(stock_data) > 0:
        print(f"\n⚠ Warning: Only {len(stock_data)} of {len(STOCKS)} stocks downloaded")
        raise ValueError(f"Insufficient stocks. Need {len(STOCKS)}, got {len(stock_data)}")
    else:
        raise ValueError("Unable to download any stock data")

except Exception as e:
    print(f"\n✗ Error downloading data: {e}")
    print("\nAttempting to use existing CSV files...")

    # Fallback: Try to load from existing CSV files
    csv_path_aapl = "C:/Users/Jainh/OneDrive/Desktop/FinTech/Advance Web Scrapping/AAPL.csv"
    csv_path_msft = "C:/Users/Jainh/OneDrive/Desktop/FinTech/Advance Web Scrapping/MSFT.csv"

    try:
        aapl_data = pd.read_csv(csv_path_aapl, index_col=0, parse_dates=True)
        msft_data = pd.read_csv(csv_path_msft, index_col=0, parse_dates=True)

        # Use 'Close' or 'Adj Close' column
        aapl_close = aapl_data['Adj Close'] if 'Adj Close' in aapl_data.columns else aapl_data['Close']
        msft_close = msft_data['Adj Close'] if 'Adj Close' in msft_data.columns else msft_data['Close']

        data = pd.DataFrame({
            'AAPL': aapl_close,
            'MSFT': msft_close
        })

        # Filter by date range if needed
        if START_DATE:
            data = data[data.index >= START_DATE]
        if END_DATE:
            data = data[data.index <= END_DATE]

        # Remove any NaN values
        data = data.dropna()

        print(f"✓ Loaded {len(data)} days of historical data from CSV files")
        print(f"\nLatest Prices:")
        print(data.tail())

    except Exception as csv_error:
        print(f"✗ Failed to load from CSV: {csv_error}")
        print("\n⚠ Generating sample data for demonstration purposes...")

        # Generate synthetic data as last resort
        dates = pd.date_range(start=START_DATE, end=END_DATE, freq='B')
        np.random.seed(42)
        aapl_prices = 150 * np.exp(np.cumsum(np.random.normal(0.001, 0.02, len(dates))))
        msft_prices = 300 * np.exp(np.cumsum(np.random.normal(0.001, 0.018, len(dates))))

        data = pd.DataFrame({
            'AAPL': aapl_prices,
            'MSFT': msft_prices
        }, index=dates)

        print(f"✓ Generated {len(data)} days of sample data")
        print(f"\nLatest Prices:")
        print(data.tail())

# Step 2: Calculate daily returns
print("\n[Step 2] Calculating daily returns...")
returns = data.pct_change().dropna()
print(f"\nReturns Statistics:")
print(returns.describe())

# Step 3: Calculate portfolio returns
print("\n[Step 3] Calculating portfolio returns...")
portfolio_returns = returns.dot(WEIGHTS)
print(f"\nPortfolio Returns Statistics:")
print(portfolio_returns.describe())
print(f"Mean Daily Return: {portfolio_returns.mean():.4%}")
print(f"Standard Deviation: {portfolio_returns.std():.4%}")

# ============================================================================
# METHOD 1: Historical VaR
# ============================================================================
print("\n" + "="*70)
print("METHOD 1: HISTORICAL VaR")
print("="*70)

def historical_var(returns, confidence_level, initial_investment):
    """
    Calculate VaR using the historical method (non-parametric).
    This method uses actual historical returns distribution.
    """
    # Find the percentile corresponding to the confidence level
    var_percentile = np.percentile(returns, (1 - confidence_level) * 100)
    var_dollar = initial_investment * var_percentile
    return var_percentile, var_dollar

hist_var_pct, hist_var_dollar = historical_var(portfolio_returns, CONFIDENCE_LEVEL, INITIAL_INVESTMENT)

print(f"\nHistorical VaR at {CONFIDENCE_LEVEL*100}% confidence level:")
print(f"  - VaR (percentage): {hist_var_pct:.4%}")
print(f"  - VaR (dollar): ${abs(hist_var_dollar):,.2f}")
print(f"\nInterpretation: There is a {(1-CONFIDENCE_LEVEL)*100}% chance that the portfolio")
print(f"will lose more than ${abs(hist_var_dollar):,.2f} in {HOLDING_PERIOD} day(s).")

# ============================================================================
# METHOD 2: Parametric VaR (Variance-Covariance Method)
# ============================================================================
print("\n" + "="*70)
print("METHOD 2: PARAMETRIC VaR (Variance-Covariance)")
print("="*70)

def parametric_var(returns, confidence_level, initial_investment):
    """
    Calculate VaR using the parametric method.
    Assumes returns follow a normal distribution.
    """
    mean = returns.mean()
    std = returns.std()

    # Z-score for the given confidence level
    z_score = stats.norm.ppf(1 - confidence_level)

    # VaR calculation
    var_percentile = mean + z_score * std
    var_dollar = initial_investment * var_percentile

    return var_percentile, var_dollar, mean, std

param_var_pct, param_var_dollar, mean_return, std_return = parametric_var(
    portfolio_returns, CONFIDENCE_LEVEL, INITIAL_INVESTMENT
)

print(f"\nParametric VaR at {CONFIDENCE_LEVEL*100}% confidence level:")
print(f"  - Mean Return: {mean_return:.4%}")
print(f"  - Standard Deviation: {std_return:.4%}")
print(f"  - Z-Score: {stats.norm.ppf(1 - CONFIDENCE_LEVEL):.4f}")
print(f"  - VaR (percentage): {param_var_pct:.4%}")
print(f"  - VaR (dollar): ${abs(param_var_dollar):,.2f}")
print(f"\nInterpretation: Assuming normal distribution, there is a {(1-CONFIDENCE_LEVEL)*100}% chance")
print(f"that the portfolio will lose more than ${abs(param_var_dollar):,.2f} in {HOLDING_PERIOD} day(s).")

# ============================================================================
# METHOD 3: Monte Carlo VaR
# ============================================================================
print("\n" + "="*70)
print("METHOD 3: MONTE CARLO VaR")
print("="*70)

def monte_carlo_var(returns, confidence_level, initial_investment, num_simulations=10000):
    """
    Calculate VaR using Monte Carlo simulation.
    Simulates future returns based on historical mean and covariance.
    """
    mean = returns.mean()
    std = returns.std()

    # Simulate returns
    np.random.seed(42)  # For reproducibility
    simulated_returns = np.random.normal(mean, std, num_simulations)

    # Calculate VaR
    var_percentile = np.percentile(simulated_returns, (1 - confidence_level) * 100)
    var_dollar = initial_investment * var_percentile

    return var_percentile, var_dollar, simulated_returns

mc_var_pct, mc_var_dollar, simulated_returns = monte_carlo_var(
    portfolio_returns, CONFIDENCE_LEVEL, INITIAL_INVESTMENT, MONTE_CARLO_SIMULATIONS
)

print(f"\nMonte Carlo VaR at {CONFIDENCE_LEVEL*100}% confidence level:")
print(f"  - Number of Simulations: {MONTE_CARLO_SIMULATIONS:,}")
print(f"  - VaR (percentage): {mc_var_pct:.4%}")
print(f"  - VaR (dollar): ${abs(mc_var_dollar):,.2f}")
print(f"\nInterpretation: Based on {MONTE_CARLO_SIMULATIONS:,} simulations, there is a {(1-CONFIDENCE_LEVEL)*100}% chance")
print(f"that the portfolio will lose more than ${abs(mc_var_dollar):,.2f} in {HOLDING_PERIOD} day(s).")

# ============================================================================
# COMPARISON OF ALL THREE METHODS
# ============================================================================
print("\n" + "="*70)
print("COMPARISON OF ALL THREE VAR METHODS")
print("="*70)

comparison_df = pd.DataFrame({
    'Method': ['Historical VaR', 'Parametric VaR', 'Monte Carlo VaR'],
    'VaR (%)': [hist_var_pct, param_var_pct, mc_var_pct],
    'VaR ($)': [hist_var_dollar, param_var_dollar, mc_var_dollar],
    'Absolute VaR ($)': [abs(hist_var_dollar), abs(param_var_dollar), abs(mc_var_dollar)]
})

print("\n", comparison_df.to_string(index=False))

print("\n\nKey Differences:")
print("-" * 70)
print("1. Historical VaR:")
print("   + Uses actual historical data distribution")
print("   + No assumptions about distribution shape")
print("   - Limited by historical data available")
print("   - May not capture future extreme events")

print("\n2. Parametric VaR:")
print("   + Fast and easy to calculate")
print("   + Based on statistical theory")
print("   - Assumes normal distribution (may underestimate tail risk)")
print("   - May not work well for non-normal returns")

print("\n3. Monte Carlo VaR:")
print("   + Flexible and can handle complex portfolios")
print("   + Can incorporate various distributions")
print("   - Computationally intensive")
print("   - Results depend on assumptions and number of simulations")

# ============================================================================
# VISUALIZATION
# ============================================================================
print("\n[Creating Visualizations...]")

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Plot 1: Portfolio Returns Distribution
ax1 = axes[0, 0]
ax1.hist(portfolio_returns, bins=50, alpha=0.7, edgecolor='black')
ax1.axvline(hist_var_pct, color='r', linestyle='--', linewidth=2, label=f'Historical VaR: {hist_var_pct:.4%}')
ax1.axvline(param_var_pct, color='g', linestyle='--', linewidth=2, label=f'Parametric VaR: {param_var_pct:.4%}')
ax1.axvline(mc_var_pct, color='b', linestyle='--', linewidth=2, label=f'Monte Carlo VaR: {mc_var_pct:.4%}')
ax1.set_xlabel('Daily Returns')
ax1.set_ylabel('Frequency')
ax1.set_title('Portfolio Returns Distribution with VaR Levels')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Monte Carlo Simulated Returns
ax2 = axes[0, 1]
ax2.hist(simulated_returns, bins=50, alpha=0.7, color='blue', edgecolor='black')
ax2.axvline(mc_var_pct, color='r', linestyle='--', linewidth=2, label=f'VaR: {mc_var_pct:.4%}')
ax2.set_xlabel('Simulated Returns')
ax2.set_ylabel('Frequency')
ax2.set_title(f'Monte Carlo Simulated Returns ({MONTE_CARLO_SIMULATIONS:,} simulations)')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: VaR Comparison (Dollar Values)
ax3 = axes[1, 0]
methods = ['Historical', 'Parametric', 'Monte Carlo']
var_values = [abs(hist_var_dollar), abs(param_var_dollar), abs(mc_var_dollar)]
colors = ['red', 'green', 'blue']
bars = ax3.bar(methods, var_values, color=colors, alpha=0.7, edgecolor='black')
ax3.set_ylabel('VaR (USD)')
ax3.set_title(f'VaR Comparison at {CONFIDENCE_LEVEL*100}% Confidence Level')
ax3.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar, value in zip(bars, var_values):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'${value:,.0f}',
             ha='center', va='bottom', fontweight='bold')

# Plot 4: Cumulative Returns
ax4 = axes[1, 1]
cumulative_returns = (1 + portfolio_returns).cumprod()
ax4.plot(cumulative_returns.index, cumulative_returns.values, linewidth=2)
ax4.set_xlabel('Date')
ax4.set_ylabel('Cumulative Return')
ax4.set_title('Portfolio Cumulative Returns Over Time')
ax4.grid(True, alpha=0.3)
ax4.axhline(y=1, color='r', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('C:/Users/Jainh/OneDrive/Desktop/FinTech/11Feb/VaR_Analysis.png', dpi=300, bbox_inches='tight')
print("Visualization saved as 'VaR_Analysis.png'")

# ============================================================================
# ADDITIONAL ANALYSIS: Conditional VaR (CVaR / Expected Shortfall)
# ============================================================================
print("\n" + "="*70)
print("BONUS: CONDITIONAL VAR (CVaR / Expected Shortfall)")
print("="*70)

# CVaR is the expected loss given that the loss exceeds VaR
cvar_historical = portfolio_returns[portfolio_returns <= hist_var_pct].mean()
cvar_historical_dollar = INITIAL_INVESTMENT * cvar_historical

print(f"\nConditional VaR (Expected Shortfall) at {CONFIDENCE_LEVEL*100}% confidence:")
print(f"  - CVaR (percentage): {cvar_historical:.4%}")
print(f"  - CVaR (dollar): ${abs(cvar_historical_dollar):,.2f}")
print(f"\nInterpretation: Given that losses exceed the VaR threshold,")
print(f"the expected loss is ${abs(cvar_historical_dollar):,.2f}.")

print("\n" + "="*70)
print("ANALYSIS COMPLETE!")
print("="*70)

plt.show()
