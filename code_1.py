import yfinance as yf
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler
from ripser import ripser
import matplotlib.pyplot as plt

# Step 1: Collect Financial Data
def collect_data(ticker, start_date, end_date, filename):
    data = yf.download(ticker, start=start_date, end=end_date)
    data.to_csv(filename)
    print(f"Data saved to {filename}")

collect_data('^GSPC', '2010-01-01', '2020-01-01', 'sp500.csv')

# Step 2: Preprocess Data
def preprocess_data(filename):
    data = pd.read_csv(filename, parse_dates=True, index_col='Date')
    prices = data['Adj Close']
    returns = prices.pct_change().dropna()
    return returns

returns = preprocess_data('sp500.csv')

# Step 3: Create Rolling Windows
def create_rolling_windows(returns, window_size):
    rolling_windows = [returns[i:i + window_size].values for i in range(len(returns) - window_size + 1)]
    return rolling_windows

window_size = 30
rolling_windows = create_rolling_windows(returns, window_size)

# Step 4: Convert to Point Cloud Using Delay Embedding
def delay_embedding(time_series, embedding_dim, delay):
    result = np.array([time_series[i:i + embedding_dim] for i in range(len(time_series) - embedding_dim)])
    return result

embedding_dim = 3
delay = 1
point_clouds = [delay_embedding(window, embedding_dim, delay) for window in rolling_windows]

# Step 5: Compute Distance Matrices
def compute_distance_matrices(point_clouds):
    distance_matrices = []
    for point_cloud in point_clouds:
        scaler = StandardScaler()
        point_cloud = scaler.fit_transform(point_cloud)
        distance_matrix = pdist(point_cloud)
        distance_matrix = squareform(distance_matrix)
        distance_matrices.append(distance_matrix)
    return distance_matrices

distance_matrices = compute_distance_matrices(point_clouds)

# Step 6: Perform Topological Data Analysis
def perform_tda(distance_matrices):
    diagrams = []
    for distance_matrix in distance_matrices:
        result = ripser(distance_matrix, maxdim=1, distance_matrix=True)
        diagrams.append(result['dgms'])
    return diagrams

diagrams = perform_tda(distance_matrices)

# Step 7: Custom Function to Plot Persistence Diagrams
def plot_persistence_diagram(diagram, ax):
    if len(diagram) > 0:
        for dim in range(len(diagram)):
            points = np.array(diagram[dim])
            ax.scatter(points[:, 0], points[:, 1], label=f'Dimension {dim}')
    ax.set_xlabel('Birth')
    ax.set_ylabel('Death')
    ax.set_title('Persistence Diagram')
    ax.legend()
    ax.grid(True)

# Step 8: Plot Results
def plot_results(rolling_windows, diagrams, num_examples=3):
    for i in range(num_examples):
        # Plot Rolling Window Returns
        plt.figure(figsize=(14, 7))
        plt.plot(rolling_windows[i], marker='o')
        plt.xlabel('Days in Window')
        plt.ylabel('Return Percentage')
        plt.title(f'Returns in Rolling Window {i + 1}')
        plt.grid(True)
        plt.show()

        # Plot Persistence Diagram
        plt.figure(figsize=(14, 7))
        ax = plt.gca()
        plot_persistence_diagram(diagrams[i], ax)
        plt.title(f'Persistence Diagram for Rolling Window {i + 1}')
        plt.show()

plot_results(rolling_windows, diagrams)
