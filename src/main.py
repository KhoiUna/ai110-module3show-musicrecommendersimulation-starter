"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Taste profile: a late-night studier who wants calm, acoustic background music.
    # Keys match the UserProfile fields in recommender.py.
    user_prefs = {
        "favorite_genre": "lofi",   # small bonus for an exact genre match
        "favorite_mood": "chill",   # larger bonus for an exact mood match
        "target_energy": 0.40,      # songs closest to 0.40 score highest
        "likes_acoustic": True,     # rewards high acousticness
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
