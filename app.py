"""
🎬 CineMatch — Movie Recommender Streamlit Frontend
Calls the FastAPI backend for all data. Dark cinematic theme with glassmorphism cards.
"""

import requests
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
API_BASE = "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch – Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# DARK CINEMATIC CSS (glassmorphism + hover animations)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global reset ── */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #0f0c29 100%);
        min-height: 100vh;
    }
    .block-container { padding: 1.5rem 2.5rem 3rem; max-width: 1500px; }

    /* ── Hero header ── */
    .hero {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem;
        background: linear-gradient(180deg, rgba(233,69,96,0.08) 0%, transparent 100%);
        border-radius: 24px;
        margin-bottom: 1.5rem;
    }
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #e94560 0%, #f5a623 50%, #e94560 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -1px;
        margin: 0;
    }
    .hero-sub {
        color: #6666aa;
        font-size: 0.95rem;
        font-weight: 400;
        margin-top: 0.35rem;
    }

    /* ── Inputs ── */
    div[data-testid="stTextInput"] input,
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border: 1.5px solid rgba(233, 69, 96, 0.4) !important;
        border-radius: 14px !important;
        color: #000000 !important;
        font-size: 1rem !important;
        padding: 0.7rem 1.2rem !important;
        transition: all 0.3s ease;
    }
    div[data-testid="stTextInput"] input:focus,
    .stTextInput input:focus {
        border-color: #e94560 !important;
        box-shadow: 0 0 0 3px rgba(233, 69, 96, 0.25) !important;
        background-color: rgba(255, 255, 255, 0.12) !important;
    }
    div[data-testid="stTextInput"] input::placeholder,
    .stTextInput input::placeholder {
        color: #8888aa !important;
        opacity: 1 !important;
    }
    div[data-testid="stTextInput"] [data-testid="InputInstructions"],
    .stTextInput [data-testid="InputInstructions"] {
        top: 55% !important;
        transform: translateY(-50%) !important;
        margin: 0 !important;
        line-height: 1 !important;
    }

    /* ── Selectboxes ── */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1.5px solid rgba(233,69,96,0.3) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    [data-baseweb="select"] { background: transparent !important; }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #e94560, #c0392b) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.55rem 1.4rem !important;
        cursor: pointer !important;
        transition: all 0.25s ease !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #ff6b8a, #e94560) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(233,69,96,0.35) !important;
    }
    .stButton > button[kind="secondary"] {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: rgba(15,12,41,0.95) !important;
        border-right: 1px solid rgba(233,69,96,0.2) !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ccccee !important;
    }

    /* ── Slider ── */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background: #e94560 !important;
    }

    /* ── Movie poster card ── */
    .movie-card {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        overflow: hidden;
        transition: transform 0.32s cubic-bezier(0.25,0.8,0.25,1),
                    box-shadow 0.32s ease,
                    border-color 0.32s ease;
        display: flex;
        flex-direction: column;
        height: 100%;
        min-height: 480px;
    }
    .movie-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 24px 55px rgba(233,69,96,0.28);
        border-color: rgba(233,69,96,0.5);
    }
    .movie-card img {
        width: 100%;
        aspect-ratio: 2/3;
        object-fit: cover;
        display: block;
    }
    .card-body {
        padding: 0.75rem 0.85rem 0.9rem;
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }
    .card-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: #f0f0ff;
        margin: 0 0 0.25rem;
        line-height: 1.2;
        height: 2.4em;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    .card-meta {
        font-size: 0.72rem;
        color: #7777aa;
        margin: 0 0 0.4rem;
        height: 1.2em;
    }
    .rating-badge {
        display: inline-flex;
        align-items: center;
        gap: 3px;
        background: rgba(233,69,96,0.15);
        border: 1px solid rgba(233,69,96,0.35);
        border-radius: 7px;
        padding: 2px 8px;
        font-size: 0.72rem;
        font-weight: 600;
        color: #ff8fa3;
        margin-top: auto;
        margin-bottom: 0.6rem;
        width: fit-content;
    }
    .no-poster {
        width: 100%;
        aspect-ratio: 2/3;
        background: linear-gradient(135deg, #1a1a3e, #0f0c29);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        color: #333366;
    }

    /* ── Open button inside card ── */
    .open-btn {
        display: block;
        width: 100%;
        margin-top: auto;
        padding: 0.38rem 0;
        background: linear-gradient(135deg, rgba(233,69,96,0.18), rgba(233,69,96,0.08));
        border: 1px solid rgba(233,69,96,0.35);
        border-radius: 9px;
        color: #ff8fa3 !important;
        font-size: 0.75rem;
        font-weight: 600;
        text-align: center;
        text-decoration: none !important;
        transition: all 0.2s;
        letter-spacing: 0.3px;
    }
    .open-btn:hover {
        background: rgba(233,69,96,0.28) !important;
        border-color: #e94560 !important;
        color: #fff !important;
    }

    /* ── Details hero card ── */
    .details-hero {
        display: flex;
        gap: 2rem;
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(233,69,96,0.25);
        border-radius: 24px;
        padding: 1.8rem;
        margin-bottom: 2rem;
        align-items: flex-start;
    }
    .details-poster {
        width: 200px;
        min-width: 200px;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    }
    .details-poster img { width: 100%; display: block; }
    .details-info h1 {
        font-size: 2rem;
        font-weight: 800;
        color: #fff;
        margin: 0 0 0.5rem;
        line-height: 1.15;
    }
    .details-info p {
        color: #8888aa;
        font-size: 0.88rem;
        margin: 0.3rem 0;
        line-height: 1.5;
    }
    .details-info .overview {
        color: #aaaacc;
        font-size: 0.9rem;
        line-height: 1.65;
        margin-top: 0.8rem;
        max-width: 720px;
    }
    .genre-chip {
        display: inline-block;
        background: rgba(233,69,96,0.13);
        border: 1px solid rgba(233,69,96,0.3);
        border-radius: 50px;
        padding: 3px 12px;
        font-size: 0.75rem;
        color: #ff8fa3;
        margin: 0 4px 4px 0;
    }
    .genre-row { margin: 0.6rem 0; }

    /* ── Section label ── */
    .section-label {
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
        margin: 1.5rem 0 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-label span { color: #e94560; }

    /* ── Stats pills ── */
    .stats-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.7rem;
        margin: 1rem 0 0.5rem;
    }
    .stat-pill {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 50px;
        padding: 0.35rem 1rem;
        font-size: 0.78rem;
        color: #8888aa;
    }
    .stat-pill b { color: #e94560; }

    /* ── Category tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 14px !important;
        padding: 4px !important;
        gap: 4px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        color: #7777aa !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 1.1rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #e94560, #c0392b) !important;
        color: white !important;
    }

    /* ── Backdrop image ── */
    .backdrop-img {
        width: 100%;
        border-radius: 16px;
        overflow: hidden;
        margin: 1rem 0;
    }
    .backdrop-img img { width: 100%; display: block; }

    /* ── Divider ── */
    hr { border-color: rgba(255,255,255,0.06) !important; }

    /* ── Info/warning/error ── */
    .stAlert { border-radius: 12px !important; }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #e94560 !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0f0c29; }
    ::-webkit-scrollbar-thumb { background: #e94560; border-radius: 10px; }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE + ROUTING
# ─────────────────────────────────────────────────────────────────────────────
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

# Sync with URL query params
qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except Exception:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# API HELPERS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=30, show_spinner=False)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """
    Supports BOTH API shapes:
      1) raw TMDB: {"results":[{id,title,poster_path,...}]}
      2) list cards: [{tmdb_id,title,poster_url,...}]
    Returns: suggestions[(label,tmdb_id)], cards[{tmdb_id,title,poster_url}]
    """
    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        raw_items = []
        for m in data.get("results") or []:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                "release_date": m.get("release_date", ""),
                "vote_average": m.get("vote_average", 0),
            })
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            if not title or not tmdb_id:
                continue
            raw_items.append({
                "tmdb_id": int(tmdb_id),
                "title": title,
                "poster_url": m.get("poster_url"),
                "release_date": m.get("release_date", ""),
                "vote_average": m.get("vote_average", 0),
            })
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [
        {
            "tmdb_id": x["tmdb_id"],
            "title": x["title"],
            "poster_url": x["poster_url"],
            "vote_average": x.get("vote_average", 0),
            "release_date": x.get("release_date", ""),
        }
        for x in final_list[:limit]
    ]
    return suggestions, cards


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append({
                "tmdb_id": tmdb["tmdb_id"],
                "title": tmdb.get("title") or x.get("title") or "Untitled",
                "poster_url": tmdb.get("poster_url"),
                "vote_average": tmdb.get("vote_average", 0),
                "release_date": tmdb.get("release_date", ""),
            })
    return cards


# ─────────────────────────────────────────────────────────────────────────────
# POSTER GRID (aligned HTML cards)
# ─────────────────────────────────────────────────────────────────────────────
def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")
            rating = m.get("vote_average") or 0
            year = (m.get("release_date") or "")[:4]

            with colset[c]:
                # Poster HTML
                if poster:
                    poster_html = f'<img src="{poster}" alt="{title} poster" onerror="this.src=\'https://via.placeholder.com/500x750/1a1a2e/e94560?text=No+Poster\'"/>'
                else:
                    poster_html = "<div class='no-poster'>🎬</div>"

                # Rating badge
                rating_val = f"⭐ {rating:.1f}" if rating else "⭐ N/A"
                rating_html = f"<div class='rating-badge'>{rating_val}</div>"

                # Render complete card including the link-button in HTML
                # This guarantees perfect vertical align and zero Streamlit warnings
                st.markdown(
                    f"""
                    <div class="movie-card">
                        {poster_html}
                        <div class="card-body">
                            <div class="card-title" title="{title}">{title}</div>
                            <div class="card-meta">📅 {year if year else 'N/A'}</div>
                            {rating_html}
                            <a class="open-btn" href="?view=details&id={tmdb_id}" target="_self">▶ Open</a>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<div style='margin-bottom:0.6rem'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎬 CineMatch")
    if st.button("🏠 Home", use_container_width=True):
        goto_home()

    st.markdown("---")
    st.markdown("### Home Feed")
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
        label_visibility="collapsed",
    )
    grid_cols = st.slider("Grid columns", 3, 8, 5)

    st.markdown("---")
    st.markdown(
        "<div style='color:#444466;font-size:0.75rem'>Powered by TMDB + TF-IDF</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# HERO HEADER (shown on every view)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <p class="hero-title">🎬 CineMatch</p>
        <p class="hero-sub">Discover movies you'll love — TF-IDF recommendations + TMDB live data</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# VIEW: HOME
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.view == "home":

    # ── Search bar ──
    col_input, col_btn = st.columns([6, 1])
    with col_input:
        typed = st.text_input(
            "Search",
            placeholder="🔍  Type a movie title… e.g. avenger, batman, love",
            label_visibility="collapsed",
        )
    with col_btn:
        clear = st.button("✕ Clear", use_container_width=True)
        if clear:
            typed = ""

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Stats pills ──
    st.markdown(
        """
        <div class="stats-row">
            <div class="stat-pill">🤖 TF-IDF content-based filtering</div>
            <div class="stat-pill">🌐 Live TMDB data</div>
            <div class="stat-pill">🎭 Genre-based discovery</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ════════════════════════════════
    # SEARCH MODE
    # ════════════════════════════════
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters.")
        else:
            with st.spinner(f"Searching for **{typed}**…"):
                data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                # Autocomplete dropdown
                if suggestions:
                    st.markdown(
                        '<div class="section-label">💡 Suggestions</div>',
                        unsafe_allow_html=True,
                    )
                    labels = ["— Select a movie to view details —"] + [
                        s[0] for s in suggestions
                    ]
                    selected = st.selectbox(
                        "Suggestions", labels, index=0, label_visibility="collapsed"
                    )
                    if selected != "— Select a movie to view details —":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try another keyword.")

                # Matching results grid
                if cards:
                    st.markdown(
                        f'<div class="section-label">🔎 Results for <span>"{typed}"</span></div>',
                        unsafe_allow_html=True,
                    )
                    poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    # ════════════════════════════════
    # HOME FEED MODE (tabs by category)
    # ════════════════════════════════
    cat_label = home_category.replace("_", " ").title()
    st.markdown(
        f'<div class="section-label">🏠 <span>{cat_label}</span></div>',
        unsafe_allow_html=True,
    )

    with st.spinner(f"Loading {cat_label}…"):
        home_cards, err = api_get_json(
            "/home", params={"category": home_category, "limit": grid_cols * 4}
        )

    if err or not home_cards:
        st.error(
            f"Could not load home feed: {err or 'Unknown error'}.\n\n"
            "**Make sure the FastAPI server is running:**\n```\nuvicorn main:app --reload\n```"
        )
    else:
        poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# ─────────────────────────────────────────────────────────────────────────────
# VIEW: DETAILS
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id

    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # Back button
    back_col, _ = st.columns([1, 6])
    with back_col:
        if st.button("← Back", use_container_width=True):
            goto_home()

    # ── Fetch movie details ──
    with st.spinner("Loading movie details…"):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")

    if err or not data:
        st.error(
            f"Could not load details: {err or 'Unknown error'}.\n\n"
            "Make sure the FastAPI server is running: `uvicorn main:app --reload`"
        )
        st.stop()

    # ── Details hero card ──
    genres_html = "".join(
        f"<span class='genre-chip'>{g['name']}</span>"
        for g in data.get("genres", [])
    )
    release_year = (data.get("release_date") or "")[:4]
    vote = data.get("vote_average") or ""
    vote_str = f"⭐ {vote:.1f}/10" if isinstance(vote, (int, float)) and vote else ""

    st.markdown(
        f"""
        <div class="details-hero">
            <div class="details-poster">
                {"<img src='" + data['poster_url'] + "' alt='poster'/>" if data.get('poster_url') else "<div class='no-poster' style='width:200px;height:300px'>🎬</div>"}
            </div>
            <div class="details-info">
                <h1>{data.get('title', 'Unknown Title')}</h1>
                <p>📅 {release_year or 'Unknown year'} &nbsp;|&nbsp; {vote_str}</p>
                <div class="genre-row">{genres_html or "<span style='color:#555577'>No genres</span>"}</div>
                <p class="overview">{data.get('overview') or 'No overview available.'}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Backdrop ──
    if data.get("backdrop_url"):
        st.markdown(
            f"<div class='backdrop-img'><img src='{data['backdrop_url']}' alt='backdrop'/></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Recommendations ──
    title = (data.get("title") or "").strip()
    if title:
        st.markdown(
            '<div class="section-label">✨ <span>Recommendations</span></div>',
            unsafe_allow_html=True,
        )

        with st.spinner("Finding similar movies…"):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
            )

        if not err2 and bundle:
            tfidf_cards = to_cards_from_tfidf_items(
                bundle.get("tfidf_recommendations")
            )
            genre_cards = bundle.get("genre_recommendations", [])

            # Tabs for TF-IDF vs Genre
            tab1, tab2 = st.tabs(["🔎  Similar Movies (TF-IDF)", "🎭  More Like This (Genre)"])

            with tab1:
                if tfidf_cards:
                    poster_grid(tfidf_cards, cols=grid_cols, key_prefix="details_tfidf")
                else:
                    st.info("No TF-IDF matches found for this title in the local dataset.")

            with tab2:
                if genre_cards:
                    poster_grid(genre_cards, cols=grid_cols, key_prefix="details_genre")
                else:
                    st.info("No genre recommendations available.")

        else:
            # Fallback: genre only
            st.info("TF-IDF unavailable. Showing genre recommendations.")
            with st.spinner("Loading genre recommendations…"):
                genre_only, err3 = api_get_json(
                    "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
                )
            if not err3 and genre_only:
                poster_grid(genre_only, cols=grid_cols, key_prefix="details_genre_fallback")
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")
