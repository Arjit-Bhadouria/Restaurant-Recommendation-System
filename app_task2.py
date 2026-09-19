import streamlit as st
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Restaurant Recommendation System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# LOAD DATASET
# ==========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("Dataset.csv")

    recommend_df = df[
        [
            "Restaurant Name",
            "City",
            "Cuisines",
            "Average Cost for two",
            "Price range",
            "Aggregate rating",
            "Has Online delivery",
            "Has Table booking",
            "Votes"
        ]
    ].copy()

    recommend_df.dropna(subset=["Cuisines"], inplace=True)

    recommend_df.drop_duplicates(inplace=True)

    recommend_df.reset_index(drop=True, inplace=True)

    return recommend_df


recommend_df = load_data()

# ==========================================================
# TF-IDF MODEL
# ==========================================================

tfidf = TfidfVectorizer(stop_words="english")

tfidf_matrix = tfidf.fit_transform(
    recommend_df["Cuisines"]
)

cosine_sim = cosine_similarity(tfidf_matrix)

restaurant_index = pd.Series(
    recommend_df.index.values,
    index=recommend_df["Restaurant Name"]
)

restaurant_index = restaurant_index[
    ~restaurant_index.index.duplicated(keep="first")
]

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
<style>

html,
body,
[class*="css"]{

    background:#0E1117;
    color:white;

}

section[data-testid="stSidebar"]{

    background:#111827;

}

.hero{

background:linear-gradient(
135deg,
#6C63FF,
#3B82F6
);

padding:35px;

border-radius:25px;

color:white;

box-shadow:0px 8px 25px rgba(0,0,0,0.35);

margin-bottom:30px;

}

.hero h1{

font-size:42px;

font-weight:700;

margin-bottom:15px;

}

.hero p{

font-size:18px;

color:#ECECEC;

}

.card{

background:#1A1F2B;

padding:25px;

border-radius:20px;

border:1px solid #2B3244;

box-shadow:0px 5px 15px rgba(0,0,0,0.25);
}

.metric{

background:linear-gradient(135deg,#1A1F2B,#222B3B);

padding:20px;

border-radius:18px;

border:1px solid rgba(255,255,255,0.08);

text-align:center;

transition:0.3s;

box-shadow:0px 4px 12px rgba(0,0,0,0.25);

}

.metric:hover{

transform:translateY(-6px);

box-shadow:0px 8px 25px rgba(108,99,255,0.35);

}

.metric h1{

color:#6C63FF;

font-size:34px;

margin:0;

}

.metric h2{

font-size:30px;

margin-bottom:5px;

}

.metric h3{

color:#BBBBBB;

margin-bottom:10px;

font-size:18px;

}

.stButton>button{

background:linear-gradient(
90deg,
#6C63FF,
#3B82F6
);

color:white;

font-weight:bold;

border:none;

border-radius:12px;

height:50px;

width:100%;

}

.stButton>button:hover{

background:linear-gradient(
90deg,
#5848FF,
#2563EB
);


}

.recommend-card{

background:linear-gradient(135deg,#1B1F2B,#222A38);

padding:22px;

border-radius:20px;

border:1px solid rgba(255,255,255,0.08);

margin-bottom:18px;

transition:0.3s;

box-shadow:0 5px 18px rgba(0,0,0,.35);

}

.recommend-card:hover{

transform:translateY(-6px);

box-shadow:0 12px 30px rgba(108,99,255,.35);

}

.rating-badge{

display:inline-block;

padding:6px 12px;

border-radius:30px;

background:#2ECC71;

color:white;

font-weight:bold;

margin-top:8px;

margin-bottom:12px;

}

.progress{

width:100%;

height:10px;

background:#2A2E39;

border-radius:30px;

overflow:hidden;

margin-top:8px;

}

.progress-fill{

height:10px;

background:linear-gradient(90deg,#6C63FF,#3B82F6);

border-radius:30px;

}

.tag{

display:inline-block;

padding:5px 12px;

border-radius:20px;

margin-right:8px;

margin-top:10px;

background:#30384A;

color:white;

font-size:13px;

}
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.image(
        "https://img.icons8.com/color/96/restaurant.png",
        width=70,
    )

    st.title("Restaurant Recommender")

    st.markdown("---")

    st.markdown("## 📖 About")

    st.write(
        """
This project recommends restaurants
using:

• TF-IDF

• Cosine Similarity

• Content-Based Filtering
"""
    )

    st.markdown("---")

    st.markdown("## 📊 Dataset")

    st.metric(
        "Restaurants",
        len(recommend_df)
    )

    st.metric(
        "Cities",
        recommend_df["City"].nunique()
    )

    st.metric(
        "Cuisines",
        recommend_df["Cuisines"].nunique()
    )
    st.markdown("---")
st.success("✅ Portfolio Project")

# ==========================================================
# HERO SECTION
# ==========================================================
st.markdown(
"""
<div class="hero">

<h1>🍽 Restaurant Recommendation System</h1>

<p>

🚀 Discover restaurants based on cuisine similarity.

<br><br>

<b>TF-IDF</b> •
<b>Cosine Similarity</b> •
<b>Content-Based Filtering</b>

</p>

</div>
""",
unsafe_allow_html=True
)

# ==========================================================
# RECOMMENDATION FUNCTION
# ==========================================================

def recommend_restaurants(restaurant_name, top_n=5):

    if restaurant_name not in restaurant_index.index:
        return None

    idx = int(restaurant_index[restaurant_name])

    similarity_scores = list(
        enumerate(cosine_sim[idx])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    similarity_scores = similarity_scores[
        1:top_n+1
    ]

    restaurant_indices = [
        i[0]
        for i in similarity_scores
    ]

    recommendations = recommend_df.iloc[
        restaurant_indices
    ].copy()

    recommendations["Similarity"] = [
        round(score[1] * 100, 1)
        for score in similarity_scores
    ]

    return recommendations

# ==========================================================
# DASHBOARD STATS
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric">
        <h2>🍽</h2>
        <h3>Restaurants</h3>
        <h1>{len(recommend_df)}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric">
        <h2>🌍</h2>
        <h3>Cities</h3>
        <h1>{recommend_df["City"].nunique()}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric">
        <h2>🍜</h2>
        <h3>Cuisines</h3>
        <h1>{recommend_df["Cuisines"].nunique()}</h1>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric">
        <h2>🤖</h2>
        <h3>ML Model</h3>
        <h1>TF-IDF</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# MAIN LAYOUT
# ==========================================================

left, right = st.columns([1, 2])

# ==========================================================
# LEFT PANEL
# ==========================================================

with left:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🔍 Search Restaurant")

    restaurant = st.selectbox(
        "Select Restaurant",
        sorted(recommend_df["Restaurant Name"].unique())
    )

    recommend = st.button(
        "🍽 Recommend Restaurants",
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================================
# RIGHT PANEL
# ==========================================================

with right:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🍴 Recommendations")

    if recommend:

        with st.spinner("🔍 Finding the best restaurants for you..."):

            recommendations = recommend_restaurants(restaurant)

        if recommendations is None:

            st.error("❌ Restaurant not found.")

        else:

            st.success(
                f"Top Recommendations for **{restaurant}**"
            )

            for _, row in recommendations.iterrows():

                similarity = row["Similarity"]

                st.markdown(
                    f"""
<div class="recommend-card">

<h2>🍽 {row['Restaurant Name']}</h2>

<span class="rating-badge">
⭐ {row['Aggregate rating']}
</span>

<p>📍 <b>City:</b> {row['City']}</p>

<p>🍜 <b>Cuisine:</b> {row['Cuisines']}</p>

<p>💰 <b>Average Cost:</b> ₹{row['Average Cost for two']}</p>

<br>

<b>Similarity Score</b>

<div class="progress">
    <div class="progress-fill"
         style="width:{similarity}%;"></div>
</div>

<p style="margin-top:10px;">
<b>{similarity:.1f}% Match</b>
</p>

<hr style="border:1px solid #2E3440; margin:15px 0;">

<p style="color:#2ECC71; font-weight:bold;">
🤖 AI Recommended
</p>

<span class="tag">Content Based</span>
<span class="tag">TF-IDF</span>
<span class="tag">Cosine Similarity</span>

</div>

<br>
""",
                    unsafe_allow_html=True
                )

    else:

        st.info(
            "👈 Select a restaurant and click **Recommend Restaurants**."
        )

    st.markdown("</div>", unsafe_allow_html=True)
# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
    """
<div style="text-align:center; color:gray; padding:20px;">

🍽️ <b>Restaurant Recommendation System</b><br><br>

Built with ❤️ using

<b>Python • Streamlit • TF-IDF • Cosine Similarity</b>

</div>
""",
    unsafe_allow_html=True
)