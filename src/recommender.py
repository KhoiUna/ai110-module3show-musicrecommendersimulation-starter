import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Column types for data/songs.csv; anything not listed stays a string.
INT_FIELDS = ("id",)
FLOAT_FIELDS = ("energy", "tempo_bpm", "valence",
                "danceability", "acousticness")

# Algorithm Recipe weights (see README "Algorithm Recipe"). Max score = 5.5.
MOOD_WEIGHT = 2.0      # exact mood match
GENRE_WEIGHT = 1.0     # exact genre match
ENERGY_WEIGHT = 2.0    # scaled by closeness: 1 - |song energy - target|
ACOUSTIC_WEIGHT = 0.5  # scaled by acousticness (or its inverse)


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py

    Returns one dict per row, keyed by the CSV header. Numeric columns are
    converted (id -> int, audio features -> float) so they can be used in
    scoring math; text columns are stripped of surrounding whitespace.
    """
    print(f"Loading songs from {csv_path}...")
    songs: List[Dict] = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            line_num = reader.line_num  # actual file line, for error messages
            # DictReader stores fields beyond the header under the key None.
            if None in row:
                raise ValueError(
                    f"{csv_path}, line {line_num}: more values than header columns")
            # Skip whitespace-only / all-empty rows (e.g. ",,,,").
            if not any((value or "").strip() for value in row.values()):
                continue
            song: Dict = {key.strip(): (value or "").strip()
                          for key, value in row.items()}
            try:
                for field in INT_FIELDS:
                    song[field] = int(song[field])
                for field in FLOAT_FIELDS:
                    song[field] = float(song[field])
            except (KeyError, ValueError) as e:
                raise ValueError(
                    f"{csv_path}, line {line_num}: bad or missing value ({e})") from e
            songs.append(song)
    print(f"Loaded {len(songs)} songs.")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Judges one song in isolation using the Algorithm Recipe:
      +2.0                       if mood matches favorite_mood
      +1.0                       if genre matches favorite_genre
      +2.0 * (1 - |energy diff|) energy closeness to target_energy
      +0.5 * acousticness        if likes_acoustic, else 0.5 * (1 - acousticness)

    Returns (score, reasons), with one reason per rule that added points.
    """
    score = 0.0
    reasons: List[str] = []

    # Mood: exact label match (case/whitespace-insensitive).
    if song["mood"].strip().lower() == user_prefs["favorite_mood"].strip().lower():
        score += MOOD_WEIGHT
        reasons.append(f"mood match: {song['mood']} (+{MOOD_WEIGHT:.2f})")

    # Genre: exact label match (case/whitespace-insensitive).
    if song["genre"].strip().lower() == user_prefs["favorite_genre"].strip().lower():
        score += GENRE_WEIGHT
        reasons.append(f"genre match: {song['genre']} (+{GENRE_WEIGHT:.2f})")

    # Energy: closer to the target earns more; clamp so it never goes negative.
    target = float(user_prefs["target_energy"])
    energy_gap = abs(song["energy"] - target)
    energy_points = ENERGY_WEIGHT * max(0.0, 1.0 - energy_gap)
    score += energy_points
    reasons.append(
        f"energy {song['energy']:.2f} vs target {target:.2f} (+{energy_points:.2f})")

    # Acoustic: reward acoustic songs for acoustic fans, electronic otherwise.
    if user_prefs["likes_acoustic"]:
        acoustic_points = ACOUSTIC_WEIGHT * song["acousticness"]
        label = "acoustic"
    else:
        acoustic_points = ACOUSTIC_WEIGHT * (1.0 - song["acousticness"])
        label = "non-acoustic"
    if acoustic_points > 0:
        score += acoustic_points
        reasons.append(
            f"{label} fit: acousticness {song['acousticness']:.2f} (+{acoustic_points:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Uses score_song() as a judge for every song in the catalog, sorts the
    whole list from highest to lowest score, and returns the top k as
    (song_dict, score, explanation) tuples. Ties keep their catalog order
    because Python's sort is stable (reverse=True preserves this).
    """
    if k <= 0:
        return []  # also guards against negative k slicing off the tail

    # Judge every song exactly once: (song, score, reasons).
    judged = [(song, *score_song(user_prefs, song)) for song in songs]

    # Rank the entire catalog by score, highest first.
    ranked = sorted(judged, key=lambda item: item[1], reverse=True)

    # Keep the top k and turn each reasons list into a readable explanation.
    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]
