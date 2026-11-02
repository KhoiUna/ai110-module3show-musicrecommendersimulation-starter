# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real platforms like Spotify and YouTube combine **collaborative filtering** (what similar users play) with **content-based filtering** (what a song sounds like). They first score many candidate songs, then rank the list for relevance and variety. This simulation has no data from other users, so it is purely **content-based**. It prioritizes **vibe**, rewarding songs whose features are _closest_ to the user's preferences rather than simply higher or lower. Each song gets a score, and the top-k scores become the recommendations.

**`Song` features used**

- `energy`: main signal, scored by closeness to the user's target
- `acousticness`: organic vs. electronic sound
- `mood`: bonus for an exact match (weighted above genre)
- `genre`: smaller bonus for an exact match
- `title`, `artist`: shown in the output and explanation, not scored

**`UserProfile` fields**

- `favorite_genre`
- `favorite_mood`
- `target_energy` (0–1)
- `likes_acoustic` (True/False)

### Data Flow

```
INPUT                      PROCESS (the loop)                         OUTPUT (the ranking)
─────                      ──────────────────                         ────────────────────
user_prefs  ──┐            for each song in songs:                    sort by score (high → low)
              ├──────────►     score, reasons = score_song(prefs, song)  ──►  keep top k
songs.csv ────┘                collect (song, score, reasons)              print title, score, "Because: ..."
(load_songs)
```

1. **Input:** `load_songs()` reads `data/songs.csv` into a list of dicts and converts the numeric columns to floats. `main.py` supplies the user's taste profile.
2. **Process:** `recommend_songs()` loops over **every** song and calls `score_song()` on each one. `score_song()` judges a single song in isolation and returns its score along with a list of reasons, one for each rule that added points.
3. **Output:** The scored songs are sorted from highest to lowest score and cut to the top `k`. Each recommendation is printed with its score and the reasons behind it.

### Algorithm Recipe (finalized)

| Signal           | Points         | Rule                                                                      |
| ---------------- | -------------- | ------------------------------------------------------------------------- |
| Mood match       | **+2.0**       | `song.mood == favorite_mood`                                              |
| Genre match      | **+1.0**       | `song.genre == favorite_genre`                                            |
| Energy closeness | **0.0 to 2.0** | `2.0 × (1 − abs(song.energy − target_energy))`                            |
| Acoustic fit     | **0.0 to 0.5** | `0.5 × acousticness` if `likes_acoustic`, else `0.5 × (1 − acousticness)` |

The maximum possible score is about **5.5**.

**Why these weights?**

- **Mood counts double compared to genre.** In this catalog, genre labels are nearly unique: 14 genres across 15 songs. A large genre bonus ends up picking a single song instead of describing a taste. Mood groups songs by how they feel across genres. For example, "chill" covers both lofi and ambient songs.
- **Energy can be worth as much as mood.** A song whose energy is 0.5 away from the target loses 1 point. That stops a matching label from hiding a big mismatch in feel.
- **Acoustic fit is a small nudge.** It mostly breaks ties between songs that are otherwise similar.

I tested this against the common starting recipe (+2.0 genre, +1.0 mood, energy × 1.0). For a user who wants "pop / chill / energy 0.30", the starting recipe ranked _Gym Hero_ (intense, energy 0.93) second just because it is pop. The final recipe recommended _Spacewalk Thoughts_, _Library Rain_ and _Midnight Coding_ instead, which are actually calm songs.

### Expected Biases

- **Mood over-prioritization:** Mood is the largest single bonus, so moods with several songs dominate the top results. "chill" has 3 songs, while a "nostalgic" or "angry" listener has only one exact match. Great songs with a neighboring mood (for example, "relaxed" vs. "chill") get no credit.
- **Exact string matching:** "indie pop" does not match "pop", and "relaxed" does not match "chill". The system has no idea which labels are related.
- **Catalog imbalance:** Lofi has 3 songs and most genres have 1. Lofi and chill listeners get many good options, while fans of other genres get one match followed by songs that are only close in energy.
- **Energy as the main signal:** Two songs with the same energy but very different sounds can score the same, because tempo, valence and danceability are ignored.
- **Tie-breaking by CSV order:** Python's sort is stable, so songs with equal scores appear in the order they are listed in the file, not by any merit.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
