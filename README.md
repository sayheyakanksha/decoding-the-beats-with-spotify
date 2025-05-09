# 🎵 Decoding the Beats with Spotify

A Streamlit-powered music recommender system that compares songs using audio features from Spotify data. Select a favorite song to get smart, feature-based recommendations.

## Live Demo

Try the app here: [Streamlit App - Song Recommender](https://decoding-the-beats-with-spotify.streamlit.app/)

## Overview

This project was created by **Akanksha** for the course **I513: Usable AI** (Spring 2025).  
The work explores classic hit songs using a [Kaggle dataset](https://www.kaggle.com/datasets/thebumpkin/10400-classic-hits-10-genres-1923-to-2023/data) containing 15,150 tracks spanning from 1923 to 2023, enriched with Spotify audio features.

The project combines:
- **Exploratory data analysis** to uncover long-term trends
- **Predictive modeling** to understand song popularity drivers
- **Clustering techniques** to segment songs based on audio similarity

The result is an interpretable, content-based song recommender app built in Streamlit. This web app analyzes song similarities based on Spotify’s audio feature set and clustering. It lets users:
- Select a known song
- Discover similar tracks from the same feature cluster
- Compare key audio attributes visually

It’s designed for music lovers, data nerds, and anyone curious about what makes songs feel alike.

## Dataset
The app loads a cleaned CSV file:  
`clean_clustered_songs.csv`  
This file should contain:
- Scaled Spotify features
- A `Cluster` column indicating precomputed groupings
- Metadata such as `Track`, `Artist`, `Year`

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/decoding-the-beats-with-spotify.git
cd decoding-the-beats-with-spotify```
```

### 2. Install dependencies

I recommend using a virtual environment:
```
pip install -r requirements.txt
```

### 3. Add the data file

Make sure clean_clustered_songs.csv is in the root directory.

### 4.  Run the app
```
streamlit run app.py
```

## License

This project is licensed under the MIT License.

