import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Literal
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from ast import literal_eval
from collections import Counter

from common.event_extraction.helpers import measure_vector_distance
from common.event_extraction.visualization import visualize_embedding_clusters


def convert_embeddings_to_vstack(df: pd.DataFrame) -> np.ndarray:
    """
    This function stacks the embedding vectors in a data frame vertically. This can be used
    as a processing step, before applying the clustering algorithm.

    :param df: The data frame that should contain an "embdding" column
    """

    print("Converting embeddings to matrix...")
    df["embedding"] = df["embedding"].apply(literal_eval).apply(np.array)
    matrix = np.vstack(df["embedding"].values)
    return matrix


def cluster_embeddings_kmeans(
    vstack: np.ndarray, n_clusters: int, visualize: bool = False
):
    """
    This function clusters a given list of embeddings using k-means.

    :param vstack: Vertical stack of embeddings
    :param n_clusters: Number of clusters for k-means to establish
    :param visualize: Set this to true if the clustered embeddings should be visualized
    """

    print("Started clustering...")
    kmeans = KMeans(n_clusters=n_clusters, init="k-means++", random_state=42)
    kmeans.fit(vstack)
    cluster_labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_

    if visualize:
        visualize_embedding_clusters(
            cluster_labels, vstack, n_clusters, min_cluster_size=60
        )

    return (cluster_labels, cluster_centers)


def maximize_silhouette_avg(
    embedding_vstack: np.ndarray,
    n_tries_to_increase: int,
    visualize_best: bool = False,
) -> int:
    """
    This function implements an iterative silhouette score maximization procedure.
    This can be used to determine the best amount of clusters for a good dataset coverage of few-shot examples.

    :param embedding_vstack: The vertically stacked embeddings for which to find the best amount of clusters
    :param n_tries_to_increase: Number of iterations the procedure runs without finding an improved number of clusters
    :param visualize_best: Set this to true if the clusters with the highest silhouette score should be plotted
    """

    max_silhouette_score = 0
    best_n_clusters = 0
    best_cluster_labels = None
    no_improvement_counter = 0

    for n_clusters in range(2, len(embedding_vstack)):
        if no_improvement_counter >= n_tries_to_increase:
            break

        print(f"Clustering with {n_clusters} clusters")
        cluster_labels, _ = cluster_embeddings_kmeans(embedding_vstack, n_clusters)

        print(f"Calculating silhouette score for {n_clusters} clusters")
        silhouette_avg = silhouette_score(embedding_vstack, cluster_labels)

        if silhouette_avg > max_silhouette_score:
            no_improvement_counter = 0
            max_silhouette_score = silhouette_avg
            best_n_clusters = n_clusters
            best_cluster_labels = cluster_labels
            print(f"New best silhouette score found! - {max_silhouette_score}\n")
        else:
            no_improvement_counter += 1
            print(f"Best silhouette score remains at {max_silhouette_score}\n")

    print(
        f"""
        Result of silhouette score maximization:
        Best number of clusters: {best_n_clusters}
        Best silhouette score: {max_silhouette_score}\n
    """
    )

    if visualize_best:
        print("Visualizing best clusters...")
        visualize_embedding_clusters(
            best_cluster_labels, embedding_vstack, best_n_clusters
        )

    return best_n_clusters


def choose_representatives(
    embeddings: pd.DataFrame,
    embedded_column_name: str,
    relevant_column_names: list[str],
    data_source: pd.DataFrame,
    cluster_labels: np.ndarray,
    cluster_centers: np.ndarray,
    write_to_file: bool = False,
    output_dir_path: str | None = None,
):
    """
    This function is used to choose representatives from calculated clusters. It uses text values,
    whose embbedings are nearest to the clusters centroids.

    :param embeddings: A data frame that contains text values and their corresponding embeddings
    :param embedded_column_name: Name of the embedded column (main provenence description)
    :param relevant_column_names: Names of other columns that are relevent in the event extraction
    :param data_source: The raw data source
    :param cluster_labels: A mapping of the embeddings to their cluster ids (result of kmeans)
    :param cluster_centers: Centroids of the clusters (result of kmeans)
    :param wirte_to_file: Set this to true if the chosen representatives should written to a csv file
    :param output_dir_path: The path of the directory, containing the output csv file
    """

    print("Started choosing representatives...")

    # Sort the labels based on the cluster size in descending order
    label_counts = Counter(cluster_labels)
    sorted_labels = sorted(
        label_counts.keys(), key=lambda x: label_counts[x], reverse=True
    )

    # Find representatives for each cluster
    cluster_labels_to_nearest_center = {}
    for cl_idx, cluster_center in enumerate(cluster_centers):
        nearest_distance = float("inf")
        nearest_index = -1

        cluster_participants = np.where(cluster_labels == cl_idx)[0]

        for cp in cluster_participants:
            current_distance = measure_vector_distance(
                embeddings.iloc[cp]["embedding"], cluster_center
            )
            if current_distance < nearest_distance:
                nearest_distance = current_distance
                nearest_index = cp

        cluster_labels_to_nearest_center[cl_idx] = nearest_index

    # Collect additional columns for the representatives
    rep_nearest_center_df_data = []
    for cluster_label in sorted_labels:
        representative_idx = cluster_labels_to_nearest_center[cluster_label]
        nearest_center_hao_val = embeddings.iloc[representative_idx][
            embedded_column_name
        ]
        nearest_center_row = data_source[
            data_source[embedded_column_name] == nearest_center_hao_val
        ].iloc[0]
        rep_nearest_center_df_data.append(
            {
                "cluster": cluster_label,
                "cluster_size": label_counts[cluster_label],
                **{key: nearest_center_row[key] for key in relevant_column_names},
            }
        )

    # Output
    nearest_center_df = pd.DataFrame(rep_nearest_center_df_data)
    if write_to_file and output_dir_path is not None:
        nearest_center_df.to_csv(
            os.path.join(output_dir_path, "cluster_representatives.csv")
        )
    return nearest_center_df
