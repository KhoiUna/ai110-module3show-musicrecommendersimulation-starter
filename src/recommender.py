import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Column types for data/songs.csv; anything not listed stays a string.
INT_FIELDS = ("id",)
FLOAT_FIELDS = ("energy", "tempo_bpm", "valence",
                "danceability", "acousticness")


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
    """
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
    return []


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
