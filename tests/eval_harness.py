import sys
import os
import unittest

# Ensure src module is visible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.recommender import load_songs, validate_user_prefs, score_song, recommend_songs

class TestAppliedAISystem(unittest.TestCase):

    def setUp(self):
        """Set up test environment and mock dataset."""
        self.songs_path = "data/songs.csv"
        self.songs = load_songs(self.songs_path)
        
        self.valid_profile = {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8
        }
        
        self.invalid_profile = {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 1.5  # Out of range
        }

    def test_01_data_loading(self):
        """Test that CSV dataset loads non-empty song list."""
        self.assertGreater(len(self.songs), 0, "Dataset should contain at least 1 song.")
        self.assertIn("title", self.songs[0])
        self.assertIn("energy", self.songs[0])

    def test_02_guardrail_validation(self):
        """Test guardrails catch invalid inputs correctly."""
        is_valid_ok, _ = validate_user_prefs(self.valid_profile)
        self.assertTrue(is_valid_ok, "Valid profile failed validation check.")

        is_valid_bad, msg = validate_user_prefs(self.invalid_profile)
        self.assertFalse(is_valid_bad, "Guardrail failed to catch out-of-range target_energy.")
        self.assertIn("target_energy must be between 0.0 and 1.0", msg)

    def test_03_score_song_math(self):
        """Test scoring math consistency and reasons formatting."""
        mock_song = {
            "title": "Test Track",
            "artist": "Test Artist",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "tempo_bpm": 120
        }
        score, reasons = score_song(self.valid_profile, mock_song)
        # Expected: Genre (+2.0) + Mood (+1.0) + Energy Alignment (+1.0) = 4.0
        self.assertEqual(score, 4.0)
        self.assertEqual(len(reasons), 3)

    def test_04_recommendation_ranking(self):
        """Test top recommendation ranking and diversity guardrail."""
        recs = recommend_songs(self.valid_profile, self.songs, k=3, apply_diversity_guardrail=True)
        self.assertLessEqual(len(recs), 3)
        if len(recs) > 1:
            self.assertGreaterEqual(recs[0]["score"], recs[1]["score"], "Recommendations are not properly sorted by score.")

def run_evaluation_harness():
    print("\n==================================================")
    print(" 🧪 RUNNING AUTOMATED AI EVALUATION & TEST HARNESS")
    print("==================================================")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAppliedAISystem)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    total = result.testsRun
    failures = len(result.failures) + len(result.errors)
    passed = total - failures
    confidence_score = round(passed / total, 2)
    
    print("\n--------------------------------------------------")
    print(f"📊 SUMMARY: {passed}/{total} tests passed.")
    print(f"🛡️ Reliability Confidence Score: {confidence_score * 100}%")
    print("--------------------------------------------------\n")

if __name__ == "__main__":
    run_evaluation_harness()