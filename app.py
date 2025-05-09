import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Load preprocessed data
# Make sure this file contains scaled features + 'Cluster'
df = pd.read_csv("clean_clustered_songs.csv")

def plot_radar_comparison(features, input_vals, match_vals, input_label, match_label):
    # Ensure input is numpy array
    input_vals = np.array(input_vals).flatten()
    match_vals = np.array(match_vals).flatten()
    features = np.array(features)

    # Safety check
    if len(input_vals) != len(features) or len(match_vals) != len(features):
        raise ValueError(f"Feature length mismatch:\n"
                         f"- Features: {len(features)}\n"
                         f"- Input values: {len(input_vals)}\n"
                         f"- Match values: {len(match_vals)}")

    # Close the loop for radar plot
    input_stats = np.append(input_vals, input_vals[0])
    match_stats = np.append(match_vals, match_vals[0])
    labels = np.append(features, features[0])
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)

    # Create radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, input_stats, 'o-', label=input_label, linewidth=2)
    ax.fill(angles, input_stats, alpha=0.25)

    ax.plot(angles, match_stats, 'o-', label=match_label, linewidth=2, color='orange')
    ax.fill(angles, match_stats, alpha=0.25, color='orange')

    ax.set_thetagrids(angles * 180 / np.pi, labels)
    ax.set_title("Feature Comparison", size=15)
    ax.grid(True)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    return fig

# Recommender function
def recommend_songs(song_name, df, features, track_col="Track", num_recommendations=5):
    song_row = df[df[track_col] == song_name]
    if song_row.empty:
        return pd.DataFrame(), pd.DataFrame()

    song_cluster = song_row["Cluster"].values[0]
    same_cluster = df[df["Cluster"] == song_cluster].reset_index(drop=True)

    if song_name not in same_cluster[track_col].values:
        return pd.DataFrame(), pd.DataFrame()

    song_index = same_cluster[same_cluster[track_col] == song_name].index[0]
    similarity = cosine_similarity(same_cluster[features], same_cluster[features])
    similar_indices = similarity[song_index].argsort()[::-1][1:num_recommendations+1]
    
    recommendations = same_cluster.iloc[similar_indices][[track_col, "Artist", "Year"] + features]
    return recommendations, song_row[features]

# Define features used in clustering
features = ['Danceability', 'Energy', 'Speechiness', 'Acousticness',
            'Instrumentalness', 'Liveness', 'Valence', 'Loudness',
            'Tempo', 'Duration_min']

# Streamlit UI
st.title("🎵 Song Recommender")
st.write("Get recommendations based on your favorite track's audio features.")

# Song selection
song_list = sorted(df["Track"].unique())
selected_song = st.selectbox("Choose a song:", song_list)

if st.button("Recommend"):
    recs, input_features = recommend_songs(selected_song, df, features)

    if recs.empty:
        st.error("Song not found or no matches.")
    else:
        st.success(f"Songs similar to '{selected_song}':")
        st.table(recs[["Track", "Artist", "Year"]].reset_index(drop=True))

        # Side-by-side comparison
        st.markdown("### 🔍 Feature Comparison with Top Match")
        top_match_features = recs.iloc[0][features]

        comparison_df = pd.DataFrame({
            "Feature": features,
            selected_song: input_features.values.flatten(),
            recs.iloc[0]["Track"]: top_match_features.values.flatten()
        })

        st.dataframe(comparison_df.set_index("Feature").round(3))


        # Plot radar chart
        input_vector = input_features.values.flatten()
        match_vector = recs.iloc[0][features].values.flatten()

        scaler = MinMaxScaler()
        combined = np.vstack([input_vector, match_vector])
        normalized = scaler.fit_transform(combined)

        input_norm = normalized[0]
        match_norm = normalized[1]

        # Plot radar chart
        fig = plot_radar_comparison(
            features,
            input_norm,
            match_norm,
            input_label=selected_song,
            match_label=recs.iloc[0]["Track"]
        )

        st.pyplot(fig)
        st.caption("Note: Feature values have been normalized between 0 and 1 for visual comparison.")
