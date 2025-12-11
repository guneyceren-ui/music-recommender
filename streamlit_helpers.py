st.write("Secrets kontrol:", st.secrets)
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Spotify API ayarları (güvenli erişim: önce Streamlit secrets, sonra environment)
import os

def get_secret(key, default=None, required=False):
    val = None
    try:
        val = st.secrets.get(key)
    except Exception:
        val = None
    if not val:
        val = os.environ.get(key, default)
    if required and not val:
        st.error(f"⚠️ Missing configuration: `{key}`. Add it in Streamlit Cloud Secrets or set as an environment variable.")
        st.stop()
    return val

CLIENT_ID = get_secret("SPOTIFY_CLIENT_ID", required=True)
CLIENT_SECRET = get_secret("SPOTIFY_CLIENT_SECRET", required=True)
REDIRECT_URI = get_secret("REDIRECT_URI", default="https://music-recommender-ef4nvdpuh9tg8t2ibzrpjz.streamlit.app/", required=True)
SCOPES = get_secret(
    "SCOPES",
    default="user-read-private playlist-read-private playlist-modify-private playlist-modify-public user-library-read",
)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPES,
    )
)

TRACK_FEATURES = ["danceability", "energy", "valence", "tempo", "acousticness", "instrumentalness", "liveness", "speechiness"]

st.title("🎵 Music recommender from Cerry")

# Kullanıcı bilgisi
user = sp.current_user()
st.write(f"Slms, **{user['display_name']}**!")

# Playlistleri çek
playlists = sp.current_user_playlists(limit=20)
playlist_names = [p["name"] for p in playlists["items"]]
selected_playlist = st.selectbox("Playlist seç:", playlist_names)

# Playlist ID
playlist_id = [p["id"] for p in playlists["items"] if p["name"] == selected_playlist][0]

# Playlist şarkılarını çek
tracks = sp.playlist_tracks(playlist_id)
track_ids = [t["track"]["id"] for t in tracks["items"] if t["track"]]
track_names = [t["track"]["name"] for t in tracks["items"] if t["track"]]

# Audio özellikleri
features = sp.audio_features(track_ids)
df = pd.DataFrame(features)[TRACK_FEATURES]
df["name"] = track_names

st.subheader("Playlist Özellikleri")
st.write(df)

# Kullanıcı profil vektörü
user_profile = df[TRACK_FEATURES].mean().values

# Radar Chart
st.subheader("Kullanıcı Profil Radar Chart")
fig_radar, ax_radar = plt.subplots(subplot_kw={'projection': 'polar'})
angles = np.linspace(0, 2*np.pi, len(TRACK_FEATURES), endpoint=False)
values = np.concatenate((user_profile, [user_profile[0]]))
angles = np.concatenate((angles, [angles[0]]))
ax_radar.plot(angles, values, 'o-', linewidth=2)
ax_radar.fill(angles, values, alpha=0.25)
ax_radar.set_xticks(angles[:-1])
ax_radar.set_xticklabels(TRACK_FEATURES)
st.pyplot(fig_radar)

# PCA görselleştirme
pca = PCA(n_components=2)
pca_result = pca.fit_transform(df[TRACK_FEATURES])
df["pca1"], df["pca2"] = pca_result[:,0], pca_result[:,1]

fig, ax = plt.subplots()
sns.scatterplot(x="pca1", y="pca2", data=df, hue="name", palette="viridis", legend=False)
st.subheader("PCA Görselleştirme")
st.pyplot(fig)

# KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df["cluster"] = kmeans.fit_predict(df[TRACK_FEATURES])

# Spotify önerileri (seed olarak ilk 3 şarkı)
seed_tracks = track_ids[:3]
spotify_recs = sp.recommendations(seed_tracks=seed_tracks, limit=20)

# Hibrit öneri: Spotify önerileri + KNN similarity
rec_features = []
for t in spotify_recs["tracks"]:
    f = sp.audio_features(t["id"])[0]
    rec_features.append([f[feat] for feat in TRACK_FEATURES])

rec_df = pd.DataFrame(rec_features, columns=TRACK_FEATURES)
rec_df["name"] = [t["name"] for t in spotify_recs["tracks"]]

# KNN similarity
knn = NearestNeighbors(n_neighbors=5)
knn.fit(df[TRACK_FEATURES])
distances, indices = knn.kneighbors(rec_df[TRACK_FEATURES])

# Parametre ayarı
alpha = st.slider("Spotify ağırlığı (α)", 0.0, 1.0, 0.5)
beta = 1 - alpha

# Skor hesaplama
rec_df["similarity_score"] = 1 / (distances.mean(axis=1) + 1e-5)
rec_df["hybrid_score"] = alpha * np.linspace(1, 0, len(rec_df)) + beta * rec_df["similarity_score"]
rec_df.sort_values("hybrid_score", ascending=False, inplace=True)

st.subheader("Önerilen Şarkılar (Hibrit)")
st.write(rec_df[["name", "hybrid_score"]])

# Playlist'e ekleme
if st.button("Yeni Playlist Oluştur ve Önerileri Ekle"):
    new_playlist = sp.user_playlist_create(user["id"], "Hibrit Öneriler", public=False)
    track_uris = [spotify_recs["tracks"][i]["uri"] for i in range(len(rec_df))]
    sp.playlist_add_items(new_playlist["id"], track_uris)
    st.success("✅ Yeni playlist oluşturuldu ve öneriler eklendi!")
