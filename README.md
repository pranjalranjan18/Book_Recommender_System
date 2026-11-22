# 📚 Book Recommender System

A responsive, high-performance **Book Recommender Web App** built with **Streamlit** and powered by an **item-based collaborative filtering model**.

The application recommends books based on reader preference patterns (cosine similarity of user-rating vectors) and showcases the Top 50 most popular books calculated from average ratings and total vote volume.

---

### 🌐 Live Demo & Deployment
- **App Platform:** Streamlit Community Cloud
- **Repository:** [https://github.com/pranjalranjan18/Book_Recommender_System](https://github.com/pranjalranjan18/Book_Recommender_System)

---

### ✨ Key Features
- **Smart Recommendations:** Recommends 5 books similar to any title chosen from a catalog of 700+ popular books.
- **Top 50 Popular Books:** Browse the top 50 books with verified average ratings and vote counts.
- **Instant Response with Caching:** Leverages Streamlit resource caching (`@st.cache_resource`) for fast and smooth navigation.
- **Secure Image Display:** Automatically handles HTTPS image URLs and includes fallback placeholders for broken or missing covers.
- **Adaptive UI:** Clean dark-themed cards designed to look great across desktops, tablets, and mobile devices.

---

### 🧠 How It Works
1. **Popularity-Based Filtering:** The Top 50 books are computed by filtering books with significant vote thresholds and ranking them by average rating.
2. **Collaborative Filtering:**
   - Ratings are filtered to genuine readers (readers with > 200 ratings) and books with >= 50 ratings.
   - A pivot table of `Books × Users` is constructed.
   - **Cosine similarity** measures the angular distance between book rating vectors to identify the closest matching titles.

---

### 🗂️ Project Structure
```text
Book_Recommender_System/
├── .streamlit/
│   └── config.toml           # Streamlit server & theme configuration
├── app.py                    # Streamlit web application
├── app.png                   # App screenshot
├── popular_df.pkl            # Top 50 popular books metadata & stats
├── pt.pkl                    # User-book rating pivot table
├── books.pkl                 # Cleaned book metadata (titles, authors, images)
├── similarity_scores.pkl     # Precomputed cosine similarity matrix
├── requirements.txt          # Python dependencies
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
```

---

### 🚀 Streamlit Cloud Deployment Guide

When deploying this project to **Streamlit Community Cloud** (share.streamlit.io):

1. Go to [share.streamlit.io](https://share.streamlit.io/) and click **New app**.
2. Select your repository: `pranjalranjan18/Book_Recommender_System`.
3. Set **Branch** to `main` and **Main file path** to `app.py`.
4. Click **Advanced settings...**:
   - In the **Python version** dropdown, select **3.11** or **3.12** *(important: the similarity matrix was serialized with NumPy 2.x which works best on Python 3.11+)*.
5. Click **Deploy!**

---

### 💻 Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pranjalranjan18/Book_Recommender_System.git
   cd Book_Recommender_System
   ```

2. **Create and activate a virtual environment (Python 3.11 or 3.12 recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

---

### 👤 Author & Contact
- **Project Owner:** Pranjal Ranjan
- **Email:** [ranjanpranjal04@gmail.com](mailto:ranjanpranjal04@gmail.com)
- **Phone:** +91 8825163201
- **GitHub:** [@pranjalranjan18](https://github.com/pranjalranjan18)

