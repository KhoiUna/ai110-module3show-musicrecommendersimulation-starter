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


# Taste profiles. Keys match the UserProfile fields in recommender.py.

# Upbeat listener who wants danceable, polished, high-energy pop.
HIGH_ENERGY_POP = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.85,
    "likes_acoustic": False,
}

# Late-night studier who wants calm, acoustic background music.
CHILL_LOFI = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "likes_acoustic": True,
}

# Gym / commute listener who wants loud, driving, electric rock.
DEEP_INTENSE_ROCK = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.92,
    "likes_acoustic": False,
}

USER_PROFILES = {
    "High-Energy Pop": HIGH_ENERGY_POP,
    "Chill Lofi": CHILL_LOFI,
    "Deep Intense Rock": DEEP_INTENSE_ROCK,
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in USER_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print()
        print(f"=== {name} ===")
        print_profile(user_prefs)
        print_recommendations(recommendations)


if __name__ == "__main__":
    main()
