import math
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate the Euclidean distance between two points
def calculate_distance(point1, point2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))

# Function to perform K-means clustering
def k_means_clustering(data_points, num_clusters, max_iterations=100):
    centroids = data_points[:num_clusters]

    for iteration in range(max_iterations):
        labels = []
        for point in data_points:
            closest_centroid = min(
                range(num_clusters), 
                key=lambda i: calculate_distance(point, centroids[i])
            )
            labels.append(closest_centroid)

        new_centroids = []
        for i in range(num_clusters):
            cluster_points = [data_points[j] for j in range(len(data_points)) if labels[j] == i]

            if cluster_points:
                new_centroid = [sum(point[dim] for point in cluster_points) / len(cluster_points)
                                for dim in range(len(data_points[0]))]
                new_centroids.append(new_centroid)
            else:
                new_centroids.append(centroids[i])

        # Display clusters and points in each iteration
        print(f"\nIteration {iteration + 1} clusters:")
        for i in range(num_clusters):
            cluster_points = [data_points[j] for j in range(len(data_points)) if labels[j] == i]
            print(f"Cluster {i + 1}: {cluster_points}")

        if new_centroids == centroids:
            print("\nConverged! Stopping iterations.")
            break

        centroids = new_centroids

    return labels, centroids

# Plotting function
def plot_clusters(data_points, labels, centroids, num_clusters):
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']  # Add more if necessary
    plt.figure(figsize=(8, 6))

    for i in range(num_clusters):
        cluster_points = [data_points[j] for j in range(len(data_points)) if labels[j] == i]
        cluster_points_x = [point[0] for point in cluster_points]
        cluster_points_y = [point[1] for point in cluster_points]
        plt.scatter(cluster_points_x, cluster_points_y, color=colors[i % len(colors)], label=f'Cluster {i + 1}')

    centroid_x = [centroid[0] for centroid in centroids]
    centroid_y = [centroid[1] for centroid in centroids]
    plt.scatter(centroid_x, centroid_y, color='k', marker='x', s=100, label='Centroids')

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.title('K-means Clustering')
    plt.show()

# Read data from a CSV file
csv_file = "your_data.csv"  # Replace with your CSV file path
df = pd.read_csv(csv_file)

# Convert DataFrame to a list of lists (assuming numerical data)
data_points = df.values.tolist()

# Get the number of clusters from the user
num_clusters = int(input("Enter the number of clusters (k): "))

# Run the K-means clustering algorithm
labels, centroids = k_means_clustering(data_points, num_clusters)

# Output the final clusters and centroids
print("\nFinal clusters:")
for i in range(num_clusters):
    cluster_points = [data_points[j] for j in range(len(data_points)) if labels[j] == i]
    print(f"Cluster {i + 1}: {cluster_points}")

print("\nFinal centroids:")
print(centroids)

# Plot the clusters and centroids
plot_clusters(data_points, labels, centroids, num_clusters)
