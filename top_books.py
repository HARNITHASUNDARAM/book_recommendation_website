import pandas as pd
import streamlit as st

# Set page config for a book-lover theme
st.set_page_config(
    page_title="Book Lover's Paradise",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for a beautiful theme
st.markdown("""
    <style>
    .main {
        background-color: #f6f1ee;
    }
    .stApp {
        background-image: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
        color: #2d3142;
    }
    .title {
        font-family: 'Georgia', serif;
        color: #2d3142;
        text-align: center;
    }
    .subtitle {
        font-family: 'Georgia', serif;
        color: #b83b5e;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">📚 Book Lover\'s Paradise 📚</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="subtitle">Find your next read, matched to your mood!</h3>', unsafe_allow_html=True)

# Load the dataset
data = pd.read_csv("books_data.csv")
data['average_rating'] = pd.to_numeric(data['average_rating'], errors='coerce')

# Show top 5 books
st.subheader("🌟 Top 5 Books by Average Rating")
top_books = data.sort_values(by='average_rating', ascending=False).head(5)
st.table(top_books[['title', 'authors', 'average_rating']])

# Mood-based recommendation
st.subheader("📖 Get Book Recommendations by Mood")

moods = {
    "Happy": ["joy", "fun", "adventure", "humor", "uplifting"],
    "Sad": ["comfort", "hope", "inspirational", "healing", "heartwarming"],
    "Adventurous": ["adventure", "action", "thriller", "explore", "quest"],
    "Romantic": ["romance", "love", "passion", "relationship", "heart"],
    "Thoughtful": ["philosophy", "deep", "reflective", "thought-provoking", "life"],
    "Scared": ["horror", "mystery", "suspense", "dark", "chilling"],
    "Curious": ["science", "history", "mystery", "curiosity", "discovery"]
}

mood = st.selectbox("Select your mood:", list(moods.keys()))

if st.button("Suggest Books"):
    keywords = moods[mood]
    # Search for books with keywords in title or description (if available)
    mask = data['title'].str.lower().str.contains('|'.join(keywords), na=False)
    if 'description' in data.columns:
        mask = mask | data['description'].str.lower().str.contains('|'.join(keywords), na=False)
    mood_books = data[mask].sort_values(by='average_rating', ascending=False).head(5)
    if not mood_books.empty:
        st.success(f"Here are some {mood.lower()} books for you:")
        st.table(mood_books[['title', 'authors', 'average_rating']])
    else:
        st.warning("Sorry, no books found for this mood. Try another mood!")

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#b83b5e;'>Made with ❤️ for book lovers</div>",
    unsafe_allow_html=True
)