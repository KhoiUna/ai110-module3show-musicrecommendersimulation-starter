# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Goal / Task

VibeMatch suggests songs you'll probably like.

You give it a short taste profile. It scores every song in the catalog and returns the top 5.

It doesn't learn from your listening history. It just compares your stated preferences to each song's features.

---

## 3. Data Used

- **Size:** 15 songs in `data/songs.csv`. The starter file had 10, and I added 5 more (hip hop, edm, classical, country, metal).
- **Features per song:** genre, mood, energy, tempo, valence, danceability and acousticness.
- **Features the model actually uses:** genre, mood, energy and acousticness. Tempo, valence and danceability are ignored.
- **Variety:** 12 genres and 11 moods. Most of them appear only once.

**Limits:**

- 15 songs is tiny. Some users get one good match and then filler.
- Lofi has 3 songs and pop has 2, so those fans get better results.
- Energy has a gap. Songs are either calm (0.22–0.42) or loud (0.75–0.98). Only one song sits in the middle (0.55).
- Every loud song is also electronic. There's no energetic acoustic music.
- Each song has a single mood label, chosen by hand.

---

## 4. Algorithm Summary

The model works like a judge at a talent show. It gives every song a score out of 5.5, then sorts them and hands you the top 5.

**You tell it four things:** your favorite genre, your mood, how energetic you want the music (0 = very calm, 1 = very intense), and whether you like acoustic music.

**How a song earns points:**

- **Mood match: +2.** The biggest bonus. Mood is about how a song _feels_.
- **Genre match: +1.** A smaller bonus. Genre is just a label, so it counts less.
- **Energy closeness: up to +2.** A song right at your energy level gets 2 points. It loses points the further away it is. For example, if you want 0.40 and the song is 0.90, it gets 1 point.
- **Acoustic fit: up to +0.5.** Acoustic fans get a little extra for acoustic songs. Everyone else gets a little extra for electronic songs. This mostly breaks ties.

**It explains itself.** Each time a song earns points, the model writes down why (for example, "mood match: chill (+2.00)"). These reasons print next to each recommendation.

**What I changed from the starter idea.** The starter gave genre 2 points and mood 1. I flipped that and made energy count more. Most genres have only one song, so a big genre bonus just picks that one song. With the starter weights, a "chill pop" fan got an intense workout song. With my weights, they get calm songs.

---

## 5. Observed Behavior / Biases

**Medium-energy users get worse results.** The catalog has only one song near 0.55 energy. The energy score also drops slowly: a song 0.40 away from your target still gets 1.2 of 2 points. So for a 0.55-energy user, every song gets about 1.1–2.0 energy points, and energy barely separates them. The mood and genre labels end up picking almost the whole top 5.

**Labels must match exactly.** "indie pop" doesn't count as "pop". If your mood isn't in the catalog (like "sad"), you can never get the 2-point mood bonus.

**Small genres get filler.** A metal or classical fan gets one real match. The other four picks are just songs with similar energy.

**Where it works well:** Profiles that match a well-stocked part of the catalog, like "chill lofi" or "happy pop". Their top picks feel right.

---

## 6. Evaluation Process

I tested three profiles in `src/main.py` and checked whether each top 5 "felt" right for that listener:

| Profile           | Genre / Mood   | Energy | Acoustic | Top 5                                                                              |
| ----------------- | -------------- | ------ | -------- | ---------------------------------------------------------------------------------- |
| High-Energy Pop   | pop / happy    | 0.85   | no       | Sunrise City, Rooftop Lights, Gym Hero, Storm Runner, Crown Talk                   |
| Chill Lofi        | lofi / chill   | 0.40   | yes      | Library Rain, Midnight Coding, Spacewalk Thoughts, Focus Flow, Coffee Shop Stories |
| Deep Intense Rock | rock / intense | 0.92   | no       | Storm Runner, Gym Hero, Neon Horizon, Iron Verdict, Sunrise City                   |

**Comparing pairs:**

- **Pop vs. Lofi:** No songs overlap. Pop gets bright, electronic songs around 0.8 energy. Lofi gets quiet, acoustic songs around 0.3–0.4. That makes sense, since the two profiles disagree on all four preferences.
- **Pop vs. Rock:** They share three songs (Sunrise City, Gym Hero, Storm Runner), because both want loud, non-acoustic music. Mood changes the order. Sunrise City is #1 for Pop (happy) but #5 for Rock. Gym Hero is #2 for Rock (intense) but #3 for Pop.
- **Lofi vs. Rock:** No songs overlap. Their energy targets are at opposite ends (0.40 vs. 0.92). Rock gets heavy songs like Iron Verdict. Lofi gets ambient and jazz.

**Experiment: removing mood.** I commented out the mood check and ran the profiles again. Pop and Lofi reshuffled, and Focus Flow jumped to #1 for Lofi. Rock didn't change. The scores also bunched together. This showed that mood is the strongest signal.

**What surprised me:** "Gym Hero", a pop song, ranks #2 for the rock fan. There's only one rock song, so "intense" plus high energy beats the genre label. Also, Focus Flow is lofi and exactly at the 0.40 energy target, yet it ranks below an ambient song. Its mood is "focused", not "chill", so it misses the mood bonus.

---

## 7. Intended Use and Non-Intended Use

**Intended use:**

- A classroom project for learning how recommenders score and rank items.
- Trying out different profiles and weights to see how the rankings change.

**Not intended for:**

- Real users or a real music app. The catalog is far too small.
- Judging what music is "good". The scores only measure how well a song matches one profile.
- Users whose taste doesn't fit four simple settings, like someone who likes many genres or whose mood changes.

---

## 8. Ideas for Improvement

1. **Add more songs, especially mid-energy ones.** That would fix the energy gap and give small genres more than one match.
2. **Use partial matches for labels.** "indie pop" should count a little toward "pop", and "focused" should count a little toward "chill".
3. **Add variety to the top 5.** Don't let one genre or artist fill every slot. Also use the ignored features (tempo, valence, danceability).

---

## 9. Personal Reflection

**Biggest learning moment.** Removing the mood check. One line of code reshuffled two of my three profiles. I learned that the weights decide the results more than the data does. The size of the catalog matters too: with one rock song, "rock" barely means anything.

**How AI helped, and when I double-checked.** AI helped me write the scoring code, build test profiles, and spot biases like the energy gap. But I still had to check its work. After the mood experiment, the score bars still said "out of 5.5", even though mood points were gone. I also made sure every claim in this card matched the real program output, not just what sounded right.

**What surprised me.** Four simple rules and some addition already feel like real recommendations. The chill lofi list looks like something a real app would make. But it's just label matching. It feels smart because it shows its reasons, not because it understands music.

**What I'd try next.** A bigger catalog, partial credit for close labels (like "focused" and "chill"), and a rule that keeps the top 5 from all being the same type of song.
