"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import (
    load_songs,
    recommend_songs,
    MOOD_WEIGHT,
    GENRE_WEIGHT,
    ENERGY_WEIGHT,
    ACOUSTIC_WEIGHT,
    print_profile,
    print_recommendations
)


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

    print()
    print_profile(user_prefs)
    print_recommendations(recommendations)


if __name__ == "__main__":
    main()
