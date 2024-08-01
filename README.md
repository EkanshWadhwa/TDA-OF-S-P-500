# TDA-OF-S-P-500
The aim of this project is to leverage Topological Data Analysis (TDA) to explore and identify significant trends and patterns in stock price data. Traditional methods of financial analysis often focus on statistical properties and linear relationships. However, TDA provides a geometric and topological perspective that can reveal insights not immediately apparent through conventional methods.

We conducted a data analysis utilizing The S&P 500 data in Python, specifically examining three rolling windows of 30 days. Subsequently, we coded and applied Topological Data Analysis (TDA) techniques to find trends and patterns.

This code collects historical S&P 500 data using the yfinance library, calculates daily returns, and creates rolling windows of returns. It then uses delay embedding to transform these windows into point clouds, followed by standard scaling and distance matrix computation. Using the ripser library, it performs topological data analysis (TDA) on these distance matrices to generate persistence diagrams. The code counts the topological features in these diagrams across dimensions 0 and 1, plotting the rolling window returns, persistence diagrams, and the number of features detected over time. This process helps visualize the evolving complexity of the financial data.It gives output in form of graphs using matplotlib.

OUTPUT
1.Persistence Diagram: Shows which stock return trends are consistent and last over time, helping to identify key recurring patterns.

2.Number of Features Over Time: Illustrates how the number and complexity of stock return trends change, indicating periods of increased volatility or emerging new trends.

3.Returns in Rolling Window: Provides a visual representation of daily stock return changes within selected periods, helping to observe trends and fluctuations
