# 🎧 Song Recommender from Cerry

A Streamlit-powered music recommendation app that analyzes your Spotify playlists and suggests songs based on audio features using machine learning and Spotify's API.

## Features

- 🔐 Spotify OAuth authentication
- 🎵 Playlist analysis with audio feature extraction
- 🤖 Hybrid recommendation engine (Spotify API + KNN similarity)
- 📊 Visualizations: Radar charts, PCA scatter plots, clustering
- 🎚️ DJ Mode with tempo filtering
- 🎯 Customizable feature weights
- ➕ Create new playlists directly from recommendations

## Requirements

- Python 3.10+
- Spotify Developer account (free)
- Spotify API credentials

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/music-recommender.git
cd music-recommender
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Spotify Credentials

#### Option A: Local Development (.streamlit/secrets.toml)

1. Get credentials from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create `.streamlit/secrets.toml`:

```toml
SPOTIFY_CLIENT_ID = "your-client-id"
SPOTIFY_CLIENT_SECRET = "your-client-secret"
REDIRECT_URI = "http://localhost:8501"
SCOPES = "user-read-private playlist-read-private playlist-modify-private playlist-modify-public user-library-read"
```

3. Register redirect URI in Spotify Dashboard:
   - Go to your app settings
   - Add `http://localhost:8501` to Redirect URIs

#### Option B: Streamlit Cloud (Recommended for Production)

1. Push code to GitHub (`.streamlit/secrets.toml` excluded via `.gitignore`)
2. Deploy on [Streamlit Community Cloud](https://share.streamlit.io)
3. Add secrets via the Streamlit Cloud dashboard:
   - Settings → Secrets → Add each credential

## Running Locally

```bash
streamlit run streamlit_helpers.py
```

The app will open at `http://localhost:8501`

## Deployment

### Streamlit Community Cloud (Free)

1. Push to GitHub
2. Go to https://share.streamlit.io
3. Click "New app" → Select repo, branch, and `streamlit_helpers.py`
4. Add secrets in app settings (don't commit `.streamlit/secrets.toml`)

### Custom Domain

For `https://yourdomain.com`:
- Use a paid Streamlit Cloud plan, or
- Self-host on Heroku, Railway, AWS, etc.
- Update `REDIRECT_URI` and register new URI in Spotify Dashboard

## Project Structure

```
music-recommender/
├── streamlit_helpers.py       # Main Streamlit app
├── requirements.txt           # Python dependencies
├── .gitignore                 # Excludes secrets, venv, etc.
├── .streamlit/
│   └── secrets.toml          # Local secrets (not committed)
└── README.md                 # This file
```

## File Explanations

- **streamlit_helpers.py**: Main app using Streamlit + Spotipy for UI and Spotify API integration
- **requirements.txt**: All dependencies with pinned versions for reproducibility
- **.gitignore**: Prevents accidental commits of secrets and local files

## Dependencies

- `streamlit`: UI framework
- `spotipy`: Spotify API client
- `scikit-learn`: Machine learning (KNN, PCA, KMeans)
- `matplotlib`, `seaborn`: Data visualization
- `pandas`, `numpy`: Data manipulation

See `requirements.txt` for exact versions.

## Usage

1. **Connect to Spotify** → Click "Spotify ile Giriş Yap" button
2. **Choose data source** → Select from your playlists, enter a URL, or use "Today's Top Hits"
3. **Load tracks** → Click "📥 Spotify'dan Veriyi Yükle"
4. **Select songs** → Check the songs you've been listening to
5. **Get recommendations** → Click "🎵 Önerileri Göster"
6. **Create playlist** → Enter a name and save recommendations to Spotify

## Troubleshooting

### "INVALID_CLIENT: Invalid redirect URI"
- Ensure your `REDIRECT_URI` in `.streamlit/secrets.toml` matches exactly what's registered in Spotify Dashboard
- No trailing spaces allowed

### "ModuleNotFoundError"
- Activate your virtual environment: `.venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`

### Secrets not found locally
- Create `.streamlit/secrets.toml` with your credentials
- File must be in `.streamlit/` folder (not root)

## Security

- **Never commit `.streamlit/secrets.toml` to GitHub** (`.gitignore` prevents this)
- Rotate credentials periodically
- Use environment variables or Streamlit Cloud secrets for production

## License

MIT

## Author

Cerry

---

**Happy recommending! 🎵**
