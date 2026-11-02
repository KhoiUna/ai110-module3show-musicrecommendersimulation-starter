# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for.

Prompts:

- What kind of recommendations does it generate
- What assumptions does it make about the user
- Is this for real users or classroom exploration

---

## 3. How the Model Works

Think of the recommender as a judge at a talent show who looks at every song in the catalog, one at a time, and gives each one a score out of about 5.5 points. After every song has a score, the judge lines them up from highest to lowest and hands you the top five.

**What it knows about you.** You tell it four things: your favorite genre (like "lofi"), the mood you're in (like "chill"), how energetic you want the music to be on a scale from 0 (very calm) to 1 (very intense), and whether you like acoustic, natural-sounding music or prefer electronic sounds.

**What it looks at in each song.** Every song has a genre, a mood, an energy level and an "acousticness" level. The song's title and artist are only shown to you; they don't affect the score.

**How a song earns points.**

- **Mood match: 2 points.** If the song's mood is exactly the mood you asked for, it gets the biggest single bonus. Mood captures how a song _feels_, which matters most when you're picking music for a moment.
- **Genre match: 1 point.** If the song's genre is your favorite, it gets a smaller bonus. Genre is a useful hint, but it's just a label. A calm ambient song can suit a lofi fan better than an intense song from the "right" genre.
- **Energy closeness: up to 2 points.** This is about how close the song is to your energy level, not whether it is higher or lower. A song exactly at your level gets the full 2 points, and it loses points the further away it is. For example, if you want 0.40 and the song is 0.90, it only gets 1 point. This way a song with the right label but the wrong feel can't sneak to the top.
- **Acoustic fit: up to half a point.** If you like acoustic music, more acoustic songs get a little extra. If you don't, more electronic songs do. This is a small nudge that mostly helps break ties.

**Why it can explain itself.** Every time a song earns points, the system writes down why (for example, "mood match: chill (+2.00)"). Those notes are printed next to each recommendation, so you can always see exactly how a score was built.

**What I changed from the starter idea.** The suggested starting point gave genre 2 points and mood 1 point. I flipped that and made energy count more. In this small catalog almost every song has its own genre, so a big genre bonus basically picks one song instead of describing a taste. When I tested someone who wanted "pop" but in a "chill" mood with low energy, the starter version recommended an intense workout song just because it was pop. With my weights, they got genuinely calm songs instead.

---

## 4. Data

Describe the dataset the model uses.

Prompts:

- How many songs are in the catalog
- What genres or moods are represented
- Did you add or remove data
- Are there parts of musical taste missing in the dataset

---

## 5. Strengths

Where does your system seem to work well

Prompts:

- User types for which it gives reasonable results
- Any patterns you think your scoring captures correctly
- Cases where the recommendations matched your intuition

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

Prompts:

- Features it does not consider
- Genres or moods that are underrepresented
- Cases where the system overfits to one preference
- Ways the scoring might unintentionally favor some users

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

Prompts:

- Which user profiles you tested
- What you looked for in the recommendations
- What surprised you
- Any simple tests or comparisons you ran

No need for numeric metrics unless you created some.

---

## 8. Future Work

Ideas for how you would improve the model next.

Prompts:

- Additional features or preferences
- Better ways to explain recommendations
- Improving diversity among the top results
- Handling more complex user tastes

---

## 9. Personal Reflection

A few sentences about your experience.

Prompts:

- What you learned about recommender systems
- Something unexpected or interesting you discovered
- How this changed the way you think about music recommendation apps
