import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


def visualize_data_source(embedding_matrix: np.ndarray, output_file_path: str):
    """
    This function prints embeddings in 2D in one color.

    :param embedding_matrix: Vertical stack of embeddings
    :param output_file_path: Path of the output .png file
    """

    print("Visualizing data source...")
    tsne = TSNE(
        n_components=2, perplexity=20, random_state=42, init="random", learning_rate=200
    )
    vis_dims2 = tsne.fit_transform(embedding_matrix)

    x = [x for x, y in vis_dims2]
    y = [y for x, y in vis_dims2]

    plt.scatter(x, y, alpha=0.3)
    plt.title("Language embeddings visualized in 2d using t-SNE")
    plt.savefig(output_file_path)


def visualize_embedding_clusters(
    cluster_labels: np.ndarray,
    matrix: np.ndarray,
    output_file_path: str,
    min_cluster_size: int = 0,
):
    """
    This function plots the clustered embeddings in 2D. Each cluster has a unique random color assigned.

    :param cluster_labels: Mapping of the embeddings to their cluster ids (result of kmeans)
    :param matrix: Vertical stack of embeddings
    :param output_file_path: Path of the outout .png file
    :param min_cluster_size: Amount of participants a cluster must have to be included in the plot
    """

    filtered_clusters = cluster_labels
    filtered_indices = [i for i in range(0, len(filtered_clusters))]

    if min_cluster_size > 0:
        unique_clusters, cluster_counts = np.unique(cluster_labels, return_counts=True)
        filtered_clusters = unique_clusters[cluster_counts >= min_cluster_size]
        filtered_indices = np.where(np.isin(cluster_labels, filtered_clusters))[0]
        print(
            f"Filtering out clusters with less than {min_cluster_size} elements. Remaining clusters: {len(filtered_clusters)}"
        )

    tsne = TSNE(
        n_components=2, perplexity=20, random_state=42, init="random", learning_rate=200
    )
    vis_dims2 = tsne.fit_transform(matrix)

    x = [x for x, y in vis_dims2]
    y = [y for x, y in vis_dims2]

    colors = np.random.rand(len(cluster_labels), 3)

    print("Plotting...")
    for idx in filtered_indices:
        plt.scatter(x[idx], y[idx], color=colors[cluster_labels[idx]], alpha=0.3)

    for cluster in filtered_clusters:
        xs = np.array(x)[cluster_labels == cluster]
        ys = np.array(y)[cluster_labels == cluster]

        x_avg = xs.mean()
        y_avg = ys.mean()

        plt.scatter(x_avg, y_avg, color=colors[cluster], marker="x", s=100)

    plt.title(
        f"{len(filtered_clusters)} clusters visualized in language 2d using t-SNE with more than {min_cluster_size} elements"
    )
    plt.savefig(output_file_path)
