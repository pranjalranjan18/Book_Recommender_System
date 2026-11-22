import streamlit as st
import numpy as np
import pickle
import os

st.set_page_config(
    page_title="Book Recommender System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Helper Functions -----------------
FALLBACK_COVER = "https://images.placeholders.dev/?width=120&height=180&text=No+Cover"

def clean_image_url(url: str) -> str:
    """Ensure image URLs use HTTPS to prevent Mixed Content blocking on Streamlit Cloud."""
    if not isinstance(url, str) or not url.strip():
        return FALLBACK_COVER
    url = url.strip()
    if url.startswith("http://"):
        url = "https://" + url[7:]
    return url

# ----------------- Data Loading (Cached) -----------------
@st.cache_resource(show_spinner="Loading book recommendation model & datasets...")
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    files = {
        'popular_df': 'popular_df.pkl',
        'pt': 'pt.pkl',
        'books': 'books.pkl',
        'similarity_scores': 'similarity_scores.pkl'
    }
    
    loaded = {}
    for key, filename in files.items():
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            st.error(f"❌ Required data file '{filename}' was not found at {filepath}.")
            st.stop()
        with open(filepath, 'rb') as f:
            loaded[key] = pickle.load(f)

    # Pre-build a fast O(1) dictionary for book metadata (title, author, image)
    # to avoid slow 270,000+ row DataFrame scans on every user recommendation.
    books_df = loaded['books'].drop_duplicates(subset=['Book-Title'])
    book_lookup = {}
    for _, row in books_df.iterrows():
        title = str(row['Book-Title'])
        book_lookup[title.lower()] = {
            'title': title,
            'author': str(row.get('Book-Author', 'Unknown Author')),
            'image': clean_image_url(str(row.get('Image-URL-M', '')))
        }

    return loaded['popular_df'], loaded['pt'], loaded['similarity_scores'], book_lookup

popular_df, pt, similarity_scores, book_lookup = load_data()

# ----------------- Custom Styling -----------------
st.markdown("""
    <style>
        /* Header Banner */
        .hero-banner {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            color: #f8fafc;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        .hero-banner h1 {
            color: #38bdf8;
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
        }
        .hero-banner p {
            color: #94a3b8;
            font-size: 1rem;
            margin-top: 6px;
            margin-bottom: 0;
        }

        /* Book Card Styling */
        .book-card {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 12px;
            text-align: center;
            height: 340px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .book-card:hover {
            transform: translateY(-4px);
            border-color: #38bdf8;
        }
        .book-card img {
            width: 100px;
            height: 145px;
            object-fit: cover;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        .book-info {
            margin-top: 8px;
            width: 100%;
        }
        .book-title {
            color: #f8fafc;
            font-size: 13px;
            font-weight: 600;
            line-height: 1.3;
            max-height: 36px;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
        }
        .book-author {
            color: #94a3b8;
            font-size: 12px;
            margin-top: 3px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .book-meta {
            color: #cbd5e1;
            font-size: 11px;
            margin-top: 4px;
        }
        .rating-badge {
            display: inline-block;
            background: #0284c7;
            color: #ffffff;
            font-size: 11px;
            font-weight: bold;
            padding: 2px 6px;
            border-radius: 4px;
            margin-top: 4px;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- App Header -----------------
st.markdown("""
    <div class="hero-banner">
        <h1>📚 Book Recommender System</h1>
        <p>Discover personalized book recommendations powered by collaborative filtering</p>
    </div>
""", unsafe_allow_html=True)

# ----------------- Navigation -----------------
nav_options = ["🏠 Top 50 Popular Books", "✨ Recommend Books", "📞 Contact"]

# Sidebar Navigation
with st.sidebar:
    st.title("🧭 Navigation")
    selected_page = st.radio("Go to:", nav_options, index=0)
    st.markdown("---")
    st.markdown("### 📊 About the App")
    st.markdown(
        """
        - **Model:** Collaborative Filtering (Cosine Similarity)
        - **Catalog:** 700+ popular books & 50 top-rated books
        - **Data:** Verified book ratings and metadata
        """
    )
    st.markdown("---")
    st.caption("Developed with ❤️ by Pranjal Ranjan")

# ----------------- Page 1: Top 50 Books -----------------
if selected_page == "🏠 Top 50 Popular Books":
    st.subheader("📖 Top 50 Most Popular Books")
    st.write("Ranked by average ratings and community popularity.")

    book_titles = list(popular_df['Book-Title'].values)
    book_authors = list(popular_df['Book-Author'].values)
    book_images = [clean_image_url(url) for url in popular_df['Image-URL-M'].values]
    book_votes = list(popular_df['normal_rating'].values)
    book_ratings = list(popular_df['avg_rating'].values)

    num_books = min(50, len(book_titles))
    for i in range(0, num_books, 5):
        cols = st.columns(5)
        for j in range(5):
            idx = i + j
            if idx < num_books:
                with cols[j]:
                    st.markdown(f"""
                        <div class="book-card">
                            <img src="{book_images[idx]}" alt="{book_titles[idx]}" onerror="this.onerror=null;this.src='{FALLBACK_COVER}';">
                            <div class="book-info">
                                <div class="book-title" title="{book_titles[idx]}">{book_titles[idx]}</div>
                                <div class="book-author">by {book_authors[idx]}</div>
                                <div class="book-meta">🗳️ {book_votes[idx]} votes</div>
                                <div class="rating-badge">★ {book_ratings[idx]:.2f} / 10</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

# ----------------- Page 2: Book Recommendations -----------------
elif selected_page == "✨ Recommend Books":
    st.subheader("✨ Get Personalized Recommendations")
    st.write("Choose any book from our curated collection to find 5 books with similar reader preferences.")

    # All available books in the pivot table
    available_books = sorted(list(pt.index))

    # Selection with typeahead search
    selected_book = st.selectbox(
        "📚 Select or search for a book you enjoyed:",
        options=available_books,
        index=0,
        help="Type to search through all 700+ available titles"
    )

    if st.button("🔍 Get Recommendations", type="primary"):
        with st.spinner("Finding similar books..."):
            book_name_lower = selected_book.strip().lower()
            pt_index_lower = [str(title).strip().lower() for title in pt.index]

            if book_name_lower in pt_index_lower:
                index = pt_index_lower.index(book_name_lower)
                # Sort by similarity score in descending order and pick top 5 (excluding the book itself)
                similar_items = sorted(
                    list(enumerate(similarity_scores[index])),
                    key=lambda x: x[1],
                    reverse=True
                )[1:6]

                recommendations = []
                for item in similar_items:
                    target_title = pt.index[item[0]]
                    meta = book_lookup.get(target_title.lower(), {
                        'title': target_title,
                        'author': 'Unknown Author',
                        'image': FALLBACK_COVER
                    })
                    score = item[1]
                    recommendations.append((meta, score))

                st.markdown(f"### 🎯 Books Similar to *{selected_book}*:")
                cols = st.columns(len(recommendations))
                for idx, (meta, score) in enumerate(recommendations):
                    with cols[idx]:
                        img_url = clean_image_url(meta['image'])
                        st.markdown(f"""
                            <div class="book-card">
                                <img src="{img_url}" alt="{meta['title']}" onerror="this.onerror=null;this.src='{FALLBACK_COVER}';">
                                <div class="book-info">
                                    <div class="book-title" title="{meta['title']}">{meta['title']}</div>
                                    <div class="book-author">by {meta['author']}</div>
                                    <div class="rating-badge" style="background:#16a34a;">Match: {score*100:.1f}%</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("❌ Book not found in the recommendation matrix. Please select a title from the list.")

# ----------------- Page 3: Contact -----------------
elif selected_page == "📞 Contact":
    st.subheader("📞 Get in Touch")
    st.write("Have questions, suggestions, or feedback? Feel free to reach out!")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div style="background-color: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 20px; color: #f8fafc;">
                <h4 style="color: #38bdf8; margin-top: 0;">📫 Contact Details</h4>
                <p><b>👤 Owner:</b> Pranjal Ranjan</p>
                <p><b>📧 Email:</b> <a href="mailto:ranjanpranjal04@gmail.com" style="color: #38bdf8;">ranjanpranjal04@gmail.com</a></p>
                <p><b>📱 Phone:</b> +91 8825163201</p>
                <p><b>💻 GitHub:</b> <a href="https://github.com/pranjalranjan18/Book_Recommender_System" target="_blank" style="color: #38bdf8;">github.com/pranjalranjan18/Book_Recommender_System</a></p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="background-color: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 20px; color: #f8fafc;">
                <h4 style="color: #38bdf8; margin-top: 0;">💡 About the Project</h4>
                <p>This project uses item-based collaborative filtering to calculate cosine similarities between books based on user ratings.</p>
                <p>Built with Streamlit and Python for lightning-fast performance and intuitive book discovery.</p>
            </div>
        """, unsafe_allow_html=True)
