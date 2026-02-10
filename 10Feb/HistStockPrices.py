import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load your historical price data
data = pd.read_csv(
    r"historical_stock_prices2.csv",
    index_col="Date",
    parse_dates=True
)

# Calculate daily returns
returns = data["Close"].pct_change().dropna()

# Calculate the 95% VaR (1-day)
confidence_level = 0.95
VaR_hist = np.percentile(returns, (1 - confidence_level) * 100)

print(f"Historical VaR (95%): {VaR_hist:.2%}")

# Visualize the returns distribution with VaR marker
plt.hist(returns, bins=50, alpha=0.75, edgecolor="black")
plt.axvline(VaR_hist, color="red", linestyle="--", linewidth=2, label="VaR (95%)")

plt.title("Returns Distribution and Historical VaR")
plt.xlabel("Returns")
plt.ylabel("Frequency")
plt.legend()
plt.grid(alpha=0.3)
plt.show()