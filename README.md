# 🎬 CineMatch — Movie Recommender App

CineMatch is a modern, high-performance movie recommendation application built with a dual-engine algorithm: a content-based recommender utilizing **TF-IDF Vectorization** (on a local dataset of 45,000+ movies) and a **live metadata engine** integrated with **The Movie Database (TMDB) API**.

The project features a **FastAPI backend** for routing, caching, and algorithms, paired with a gorgeous **Streamlit frontend** styled with a dark cinematic glassmorphism user interface.

---

## 🚀 Key Features

- 🌙 **Cinematic Dark Theme**: Premium glassmorphism layout, clean hover animations, and fully-responsive layout.
- 🤖 **TF-IDF Local Engine**: Computes similarity scores using Cosine Similarity on processed tags (Overview + Genre + Tagline) for instant, content-based matches.
- 🎭 **Genre-based Discovery**: Integrates live TMDB Discover API to fetch matching genre blockbusters dynamically.
- 🔍 **Autocomplete Search**: Integrated keyword search that filters suggestions and provides a matching results grid.
- 📄 **Rich Details Page**: Opens any movie to show posters, backdrops, ratings, release info, genres, and a synopsis.
- ⚡ **Lightning Fast & Cached**: FastAPI implements local in-memory request caching and requests session retry strategies to handle connection resets.
- 🌐 **Clean URL Routing**: Fully synchronized query parameter routing (`?view=details&id=123`) to make details views shareable.

---

## 🛠️ Architecture

```
Browser ──▶ Streamlit (:8501) ──▶ FastAPI (:8000) ──▶ TMDB API
                                       └──▶ TF-IDF Pickles (local)
```

---

## 📁 Repository Structure

```
.
├── app.py                      # Streamlit Frontend (styling, layout, routing)
├── main.py                     # FastAPI Backend (endpoints, TF-IDF calculation, TMDB client)
├── tmdb_api.py                 # TMDB API helper helper script
├── requirements.txt            # Python dependencies
├── .env                        # Private environment variables (API Keys)
├── .gitignore                  # Prevents pushing caches, large raw datasets, and API keys
├── df.pkl                      # Serialized pandas DataFrame with processed movie data
├── indices.pkl                 # Serialized lookup index (Movie title -> DataFrame index)
├── tfidf_matrix.pkl            # Pre-computed sparse TF-IDF feature matrix
├── tfidf.pkl                   # Pre-compiled Scikit-Learn TfidfVectorizer instance
└── movie_recommandation_executed.ipynb  # Initial Jupyter Notebook used to train the model
```

---

## ⚙️ Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/bmaibu/movies-recommendation.git
cd movies-recommendation
```

### 2. Set Up Environment Variables
Create a `.env` file in the root folder and add your TMDB API Key:
```env
TMDB_API_KEY=2484efa411f3e542fa29cdb743469f04
```

### 3. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI Backend
Start the backend server on `http://127.0.0.1:8000`:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 5. Run the Streamlit Frontend
In a new terminal window, start the Streamlit web interface:
```bash
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser!

---

## 🧠 Under the Hood

### The Recommendation Engine
1. **Feature Engineering**: Overviews, genres, and taglines are cleaned (lowercased, non-alphabetical characters removed, stop words stripped) and lemmatized into a consolidated `tags` string block.
2. **Vectorization**: A `TfidfVectorizer` transforms the textual representation into a sparse numerical feature matrix.
3. **Similarity**: When a movie is searched, its feature vector is extracted, and the cosine similarity score is calculated against all other vectors in the matrix:
   $$\text{Cosine Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$
4. **Live Enrichment**: Top TF-IDF recommendations are sent to TMDB in parallel, retrieving official movie posters and details instantly.
