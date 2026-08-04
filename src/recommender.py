import csv
import math
import logging
from typing import List, Dict, Tuple, Any

# Configure logging for guardrails and observability
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def load_songs(filepath: str) -> List[Dict[str, Any]]:
    """Loads song dataset from CSV and parses numeric features."""
    songs = []
    try:
        with open(filepath, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                songs.append({
                    "title": row.get("title", "Unknown"),
                    "artist": row.get("artist", "Unknown"),
                    "genre": row.get("genre", "").lower(),
                    "mood": row.get("mood", "").lower(),
                    "energy": float(row.get("energy", 0.5)),
                    "tempo_bpm": float(row.get("tempo_bpm", 120))
                })
        logging.info(f"Successfully loaded {len(songs)} songs from {filepath}")
    except Exception as e:
        logging.error(f"Failed to load songs from {filepath}: {str(e)}")
        raise e
    return songs

def validate_user_prefs(user_prefs: Dict[str, Any]) -> Tuple[bool, str]:
    """Guardrail function to validate user preferences before running inference."""
    if not isinstance(user_prefs, dict):
        return False, "User preferences must be a dictionary."
    
    required_keys = ["favorite_genre", "favorite_mood", "target_energy"]
    for key in required_keys:
        if key not in user_prefs:
            return False, f"Missing required preference key: {key}"
            
    if not (0.0 <= user_prefs["target_energy"] <= 1.0):
        return False, f"target_energy must be between 0.0 and 1.0. Got {user_prefs['target_energy']}"
        
    return True, "Valid user preferences."

def score_song(user_prefs: Dict[str, Any], song: Dict[str, Any]) -> Tuple[float, List[str]]:
    """Calculates weighted similarity score between user profile and a song."""
    score = 0.0
    reasons = []

    # 1. Genre Match (+2.0 pts)
    if song["genre"] == user_prefs["favorite_genre"].lower():
        score += 2.0
        reasons.append("Genre Match (+2.0)")

    # 2. Mood Match (+1.0 pt)
    if song["mood"] == user_prefs["favorite_mood"].lower():
        score += 1.0
        reasons.append("Mood Match (+1.0)")

    # 3. Energy Gap Penalty / Reward (Max +1.0 pt)
    energy_diff = abs(song["energy"] - user_prefs["target_energy"])
    energy_score = max(0.0, 1.0 - energy_diff)
    score += energy_score
    reasons.append(f"Energy Alignment (+{energy_score:.2f})")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict[str, Any], songs: List[Dict[str, Any]], k: int = 5, apply_diversity_guardrail: bool = True) -> List[Dict[str, Any]]:
    """Ranks songs and applies a diversity penalty guardrail to prevent single-artist flood."""
    is_valid, msg = validate_user_prefs(user_prefs)
    if not is_valid:
        logging.warning(f"Guardrail trigger: {msg}")
        return []

    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append({
            "title": song["title"],
            "artist": song["artist"],
            "genre": song["genre"],
            "mood": song["mood"],
            "energy": song["energy"],
            "score": score,
            "reasons": reasons
        })

    # Sort primarily by score descending
    scored_songs.sort(key=lambda x: x["score"], reverse=True)

    if not apply_diversity_guardrail:
        return scored_songs[:k]

    # Diversity Guardrail: Limit max 2 songs per artist in top K
    diversified = []
    artist_counts = {}
    for s in scored_songs:
        artist = s["artist"]
        if artist_counts.get(artist, 0) < 2:
            diversified.append(s)
            artist_counts[artist] = artist_counts.get(artist, 0) + 1
        if len(diversified) == k:
            break

    return diversified