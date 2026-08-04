from src.recommender import load_songs, recommend_songs

def display_recommendations(profile_name: str, user_prefs: dict, recommendations: list):
    print(f"\n==================================================")
    print(f" 🎵 RECOMMENDATIONS FOR: {profile_name}")
    print(f" Target: Genre={user_prefs.get('favorite_genre')}, Mood={user_prefs.get('favorite_mood')}, Energy={user_prefs.get('target_energy')}")
    print(f"==================================================")
    
    if not recommendations:
        print("❌ No valid recommendations generated (Guardrail triggered or empty dataset).")
        return

    for idx, item in enumerate(recommendations, 1):
        reasons_str = ", ".join(item['reasons'])
        print(f"{idx}. {item['title']} - {item['artist']} [{item['genre'].upper()}]")
        print(f"   Score: {item['score']} | Match Reasons: {reasons_str}\n")

def main():
    # Load dataset
    songs = load_songs("data/songs.csv")

    # Defined User Profiles for Evaluation
    profiles = {
        "Pop Enthusiast": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8
        },
        "Chill Lofi Listener": {
            "favorite_genre": "lofi",
            "favorite_mood": "relaxed",
            "target_energy": 0.3
        },
        "Adversarial / Invalid Input": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 2.5 # Out of bounds to test guardrail
        }
    }

    for name, prefs in profiles.items():
        recs = recommend_songs(prefs, songs, k=3)
        display_recommendations(name, prefs, recs)

if __name__ == "__main__":
    main()